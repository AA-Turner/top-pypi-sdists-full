r'''
# `aws_kendra_data_source`

Refer to the Terraform Registry for docs: [`aws_kendra_data_source`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source).
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


class KendraDataSource(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSource",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source aws_kendra_data_source}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        index_id: builtins.str,
        name: builtins.str,
        type: builtins.str,
        configuration: typing.Optional[typing.Union["KendraDataSourceConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_document_enrichment_configuration: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        language_code: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["KendraDataSourceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source aws_kendra_data_source} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param index_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#index_id KendraDataSource#index_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#name KendraDataSource#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#type KendraDataSource#type}.
        :param configuration: configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#configuration KendraDataSource#configuration}
        :param custom_document_enrichment_configuration: custom_document_enrichment_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#custom_document_enrichment_configuration KendraDataSource#custom_document_enrichment_configuration}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#description KendraDataSource#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#id KendraDataSource#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param language_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#language_code KendraDataSource#language_code}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#role_arn KendraDataSource#role_arn}.
        :param schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#schedule KendraDataSource#schedule}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#tags KendraDataSource#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#tags_all KendraDataSource#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#timeouts KendraDataSource#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0868e6a50aa75c9778b140853bc37464140b7c943903155cb455d2b5ea814ce)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = KendraDataSourceConfig(
            index_id=index_id,
            name=name,
            type=type,
            configuration=configuration,
            custom_document_enrichment_configuration=custom_document_enrichment_configuration,
            description=description,
            id=id,
            language_code=language_code,
            role_arn=role_arn,
            schedule=schedule,
            tags=tags,
            tags_all=tags_all,
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
        '''Generates CDKTF code for importing a KendraDataSource resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the KendraDataSource to import.
        :param import_from_id: The id of the existing KendraDataSource that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the KendraDataSource to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4749708cc69fa59aeada6558eae753cf3dba6d6da3084c9737cbc5e44761f7c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConfiguration")
    def put_configuration(
        self,
        *,
        s3_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationS3Configuration", typing.Dict[builtins.str, typing.Any]]] = None,
        template_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationTemplateConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        web_crawler_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationWebCrawlerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param s3_configuration: s3_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#s3_configuration KendraDataSource#s3_configuration}
        :param template_configuration: template_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#template_configuration KendraDataSource#template_configuration}
        :param web_crawler_configuration: web_crawler_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#web_crawler_configuration KendraDataSource#web_crawler_configuration}
        '''
        value = KendraDataSourceConfiguration(
            s3_configuration=s3_configuration,
            template_configuration=template_configuration,
            web_crawler_configuration=web_crawler_configuration,
        )

        return typing.cast(None, jsii.invoke(self, "putConfiguration", [value]))

    @jsii.member(jsii_name="putCustomDocumentEnrichmentConfiguration")
    def put_custom_document_enrichment_configuration(
        self,
        *,
        inline_configurations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        post_extraction_hook_configuration: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        pre_extraction_hook_configuration: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param inline_configurations: inline_configurations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#inline_configurations KendraDataSource#inline_configurations}
        :param post_extraction_hook_configuration: post_extraction_hook_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#post_extraction_hook_configuration KendraDataSource#post_extraction_hook_configuration}
        :param pre_extraction_hook_configuration: pre_extraction_hook_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#pre_extraction_hook_configuration KendraDataSource#pre_extraction_hook_configuration}
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#role_arn KendraDataSource#role_arn}.
        '''
        value = KendraDataSourceCustomDocumentEnrichmentConfiguration(
            inline_configurations=inline_configurations,
            post_extraction_hook_configuration=post_extraction_hook_configuration,
            pre_extraction_hook_configuration=pre_extraction_hook_configuration,
            role_arn=role_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putCustomDocumentEnrichmentConfiguration", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#create KendraDataSource#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#delete KendraDataSource#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#update KendraDataSource#update}.
        '''
        value = KendraDataSourceTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetConfiguration")
    def reset_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfiguration", []))

    @jsii.member(jsii_name="resetCustomDocumentEnrichmentConfiguration")
    def reset_custom_document_enrichment_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomDocumentEnrichmentConfiguration", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLanguageCode")
    def reset_language_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLanguageCode", []))

    @jsii.member(jsii_name="resetRoleArn")
    def reset_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoleArn", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

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
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(self) -> "KendraDataSourceConfigurationOutputReference":
        return typing.cast("KendraDataSourceConfigurationOutputReference", jsii.get(self, "configuration"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="customDocumentEnrichmentConfiguration")
    def custom_document_enrichment_configuration(
        self,
    ) -> "KendraDataSourceCustomDocumentEnrichmentConfigurationOutputReference":
        return typing.cast("KendraDataSourceCustomDocumentEnrichmentConfigurationOutputReference", jsii.get(self, "customDocumentEnrichmentConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorMessage"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "KendraDataSourceTimeoutsOutputReference":
        return typing.cast("KendraDataSourceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="configurationInput")
    def configuration_input(self) -> typing.Optional["KendraDataSourceConfiguration"]:
        return typing.cast(typing.Optional["KendraDataSourceConfiguration"], jsii.get(self, "configurationInput"))

    @builtins.property
    @jsii.member(jsii_name="customDocumentEnrichmentConfigurationInput")
    def custom_document_enrichment_configuration_input(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfiguration"]:
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfiguration"], jsii.get(self, "customDocumentEnrichmentConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="indexIdInput")
    def index_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indexIdInput"))

    @builtins.property
    @jsii.member(jsii_name="languageCodeInput")
    def language_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KendraDataSourceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KendraDataSourceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80f66c02dcfc71d4b8c6f80c4cbaab7866343e34c08b0b840d0b315202a74380)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b761ff8ce7117e1d9de3724bacca66b365848eb881b71af2e7a695ac7b3537f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indexId")
    def index_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "indexId"))

    @index_id.setter
    def index_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f81e628d377c17c3a2a9656f1c6d72c41eaf63d561a6582e9ba12b2f7c1dc66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indexId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="languageCode")
    def language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageCode"))

    @language_code.setter
    def language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4991bef97708c5db1f901868d2c34ecdb68a1b3ec3b51f403dc7dcff50173f50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8992e002682220bad2465902f4e9eac3e56e6baff3911a607c467e4519aa049)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6b652a40312f570933f456f5fc8e041d7396b917f417cadb37e0c5d4ddcdd77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c80cd0b88394d0e4354d318499d5fdca53c7009a9f791a21b61703cf84e1a58c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a1ecb4bb26fb4459498261f089a0376cdf1ae51c8ca1e655cc2c68ee10003a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e32c70600e928e033506f0b19d70dfa4064fee64cf5e321776d93fd3c606cc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74b25b31608114fdeab498e7f656549c55df80c059e51e86bac586610d3d38bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "index_id": "indexId",
        "name": "name",
        "type": "type",
        "configuration": "configuration",
        "custom_document_enrichment_configuration": "customDocumentEnrichmentConfiguration",
        "description": "description",
        "id": "id",
        "language_code": "languageCode",
        "role_arn": "roleArn",
        "schedule": "schedule",
        "tags": "tags",
        "tags_all": "tagsAll",
        "timeouts": "timeouts",
    },
)
class KendraDataSourceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        index_id: builtins.str,
        name: builtins.str,
        type: builtins.str,
        configuration: typing.Optional[typing.Union["KendraDataSourceConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_document_enrichment_configuration: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        language_code: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["KendraDataSourceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param index_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#index_id KendraDataSource#index_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#name KendraDataSource#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#type KendraDataSource#type}.
        :param configuration: configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#configuration KendraDataSource#configuration}
        :param custom_document_enrichment_configuration: custom_document_enrichment_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#custom_document_enrichment_configuration KendraDataSource#custom_document_enrichment_configuration}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#description KendraDataSource#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#id KendraDataSource#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param language_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#language_code KendraDataSource#language_code}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#role_arn KendraDataSource#role_arn}.
        :param schedule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#schedule KendraDataSource#schedule}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#tags KendraDataSource#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#tags_all KendraDataSource#tags_all}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#timeouts KendraDataSource#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(configuration, dict):
            configuration = KendraDataSourceConfiguration(**configuration)
        if isinstance(custom_document_enrichment_configuration, dict):
            custom_document_enrichment_configuration = KendraDataSourceCustomDocumentEnrichmentConfiguration(**custom_document_enrichment_configuration)
        if isinstance(timeouts, dict):
            timeouts = KendraDataSourceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98b50ce043c30ecca7c0443b3b48788fa87b35b794045d0376891068efa8e21e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument index_id", value=index_id, expected_type=type_hints["index_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument custom_document_enrichment_configuration", value=custom_document_enrichment_configuration, expected_type=type_hints["custom_document_enrichment_configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument language_code", value=language_code, expected_type=type_hints["language_code"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "index_id": index_id,
            "name": name,
            "type": type,
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
        if configuration is not None:
            self._values["configuration"] = configuration
        if custom_document_enrichment_configuration is not None:
            self._values["custom_document_enrichment_configuration"] = custom_document_enrichment_configuration
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if language_code is not None:
            self._values["language_code"] = language_code
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if schedule is not None:
            self._values["schedule"] = schedule
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
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
    def index_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#index_id KendraDataSource#index_id}.'''
        result = self._values.get("index_id")
        assert result is not None, "Required property 'index_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#name KendraDataSource#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#type KendraDataSource#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration(self) -> typing.Optional["KendraDataSourceConfiguration"]:
        '''configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#configuration KendraDataSource#configuration}
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional["KendraDataSourceConfiguration"], result)

    @builtins.property
    def custom_document_enrichment_configuration(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfiguration"]:
        '''custom_document_enrichment_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#custom_document_enrichment_configuration KendraDataSource#custom_document_enrichment_configuration}
        '''
        result = self._values.get("custom_document_enrichment_configuration")
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfiguration"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#description KendraDataSource#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#id KendraDataSource#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def language_code(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#language_code KendraDataSource#language_code}.'''
        result = self._values.get("language_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#role_arn KendraDataSource#role_arn}.'''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#schedule KendraDataSource#schedule}.'''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#tags KendraDataSource#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#tags_all KendraDataSource#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["KendraDataSourceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#timeouts KendraDataSource#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["KendraDataSourceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "s3_configuration": "s3Configuration",
        "template_configuration": "templateConfiguration",
        "web_crawler_configuration": "webCrawlerConfiguration",
    },
)
class KendraDataSourceConfiguration:
    def __init__(
        self,
        *,
        s3_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationS3Configuration", typing.Dict[builtins.str, typing.Any]]] = None,
        template_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationTemplateConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        web_crawler_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationWebCrawlerConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param s3_configuration: s3_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#s3_configuration KendraDataSource#s3_configuration}
        :param template_configuration: template_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#template_configuration KendraDataSource#template_configuration}
        :param web_crawler_configuration: web_crawler_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#web_crawler_configuration KendraDataSource#web_crawler_configuration}
        '''
        if isinstance(s3_configuration, dict):
            s3_configuration = KendraDataSourceConfigurationS3Configuration(**s3_configuration)
        if isinstance(template_configuration, dict):
            template_configuration = KendraDataSourceConfigurationTemplateConfiguration(**template_configuration)
        if isinstance(web_crawler_configuration, dict):
            web_crawler_configuration = KendraDataSourceConfigurationWebCrawlerConfiguration(**web_crawler_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da020ac3544d5069a3d99af94f62ad680776778c483f14ab0b4350e15a32633e)
            check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
            check_type(argname="argument template_configuration", value=template_configuration, expected_type=type_hints["template_configuration"])
            check_type(argname="argument web_crawler_configuration", value=web_crawler_configuration, expected_type=type_hints["web_crawler_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if s3_configuration is not None:
            self._values["s3_configuration"] = s3_configuration
        if template_configuration is not None:
            self._values["template_configuration"] = template_configuration
        if web_crawler_configuration is not None:
            self._values["web_crawler_configuration"] = web_crawler_configuration

    @builtins.property
    def s3_configuration(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationS3Configuration"]:
        '''s3_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#s3_configuration KendraDataSource#s3_configuration}
        '''
        result = self._values.get("s3_configuration")
        return typing.cast(typing.Optional["KendraDataSourceConfigurationS3Configuration"], result)

    @builtins.property
    def template_configuration(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationTemplateConfiguration"]:
        '''template_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#template_configuration KendraDataSource#template_configuration}
        '''
        result = self._values.get("template_configuration")
        return typing.cast(typing.Optional["KendraDataSourceConfigurationTemplateConfiguration"], result)

    @builtins.property
    def web_crawler_configuration(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationWebCrawlerConfiguration"]:
        '''web_crawler_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#web_crawler_configuration KendraDataSource#web_crawler_configuration}
        '''
        result = self._values.get("web_crawler_configuration")
        return typing.cast(typing.Optional["KendraDataSourceConfigurationWebCrawlerConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__241e186b3b8534a7742360c8b9d5ee3df68d0733bd3d1f0fd7fe8c098ce899c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putS3Configuration")
    def put_s3_configuration(
        self,
        *,
        bucket_name: builtins.str,
        access_control_list_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        documents_metadata_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#bucket_name KendraDataSource#bucket_name}.
        :param access_control_list_configuration: access_control_list_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#access_control_list_configuration KendraDataSource#access_control_list_configuration}
        :param documents_metadata_configuration: documents_metadata_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#documents_metadata_configuration KendraDataSource#documents_metadata_configuration}
        :param exclusion_patterns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#exclusion_patterns KendraDataSource#exclusion_patterns}.
        :param inclusion_patterns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#inclusion_patterns KendraDataSource#inclusion_patterns}.
        :param inclusion_prefixes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#inclusion_prefixes KendraDataSource#inclusion_prefixes}.
        '''
        value = KendraDataSourceConfigurationS3Configuration(
            bucket_name=bucket_name,
            access_control_list_configuration=access_control_list_configuration,
            documents_metadata_configuration=documents_metadata_configuration,
            exclusion_patterns=exclusion_patterns,
            inclusion_patterns=inclusion_patterns,
            inclusion_prefixes=inclusion_prefixes,
        )

        return typing.cast(None, jsii.invoke(self, "putS3Configuration", [value]))

    @jsii.member(jsii_name="putTemplateConfiguration")
    def put_template_configuration(self, *, template: builtins.str) -> None:
        '''
        :param template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#template KendraDataSource#template}.
        '''
        value = KendraDataSourceConfigurationTemplateConfiguration(template=template)

        return typing.cast(None, jsii.invoke(self, "putTemplateConfiguration", [value]))

    @jsii.member(jsii_name="putWebCrawlerConfiguration")
    def put_web_crawler_configuration(
        self,
        *,
        urls: typing.Union["KendraDataSourceConfigurationWebCrawlerConfigurationUrls", typing.Dict[builtins.str, typing.Any]],
        authentication_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        crawl_depth: typing.Optional[jsii.Number] = None,
        max_content_size_per_page_in_mega_bytes: typing.Optional[jsii.Number] = None,
        max_links_per_page: typing.Optional[jsii.Number] = None,
        max_urls_per_minute_crawl_rate: typing.Optional[jsii.Number] = None,
        proxy_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        url_exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        url_inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param urls: urls block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#urls KendraDataSource#urls}
        :param authentication_configuration: authentication_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#authentication_configuration KendraDataSource#authentication_configuration}
        :param crawl_depth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#crawl_depth KendraDataSource#crawl_depth}.
        :param max_content_size_per_page_in_mega_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#max_content_size_per_page_in_mega_bytes KendraDataSource#max_content_size_per_page_in_mega_bytes}.
        :param max_links_per_page: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#max_links_per_page KendraDataSource#max_links_per_page}.
        :param max_urls_per_minute_crawl_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#max_urls_per_minute_crawl_rate KendraDataSource#max_urls_per_minute_crawl_rate}.
        :param proxy_configuration: proxy_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#proxy_configuration KendraDataSource#proxy_configuration}
        :param url_exclusion_patterns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#url_exclusion_patterns KendraDataSource#url_exclusion_patterns}.
        :param url_inclusion_patterns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#url_inclusion_patterns KendraDataSource#url_inclusion_patterns}.
        '''
        value = KendraDataSourceConfigurationWebCrawlerConfiguration(
            urls=urls,
            authentication_configuration=authentication_configuration,
            crawl_depth=crawl_depth,
            max_content_size_per_page_in_mega_bytes=max_content_size_per_page_in_mega_bytes,
            max_links_per_page=max_links_per_page,
            max_urls_per_minute_crawl_rate=max_urls_per_minute_crawl_rate,
            proxy_configuration=proxy_configuration,
            url_exclusion_patterns=url_exclusion_patterns,
            url_inclusion_patterns=url_inclusion_patterns,
        )

        return typing.cast(None, jsii.invoke(self, "putWebCrawlerConfiguration", [value]))

    @jsii.member(jsii_name="resetS3Configuration")
    def reset_s3_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Configuration", []))

    @jsii.member(jsii_name="resetTemplateConfiguration")
    def reset_template_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemplateConfiguration", []))

    @jsii.member(jsii_name="resetWebCrawlerConfiguration")
    def reset_web_crawler_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebCrawlerConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="s3Configuration")
    def s3_configuration(
        self,
    ) -> "KendraDataSourceConfigurationS3ConfigurationOutputReference":
        return typing.cast("KendraDataSourceConfigurationS3ConfigurationOutputReference", jsii.get(self, "s3Configuration"))

    @builtins.property
    @jsii.member(jsii_name="templateConfiguration")
    def template_configuration(
        self,
    ) -> "KendraDataSourceConfigurationTemplateConfigurationOutputReference":
        return typing.cast("KendraDataSourceConfigurationTemplateConfigurationOutputReference", jsii.get(self, "templateConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="webCrawlerConfiguration")
    def web_crawler_configuration(
        self,
    ) -> "KendraDataSourceConfigurationWebCrawlerConfigurationOutputReference":
        return typing.cast("KendraDataSourceConfigurationWebCrawlerConfigurationOutputReference", jsii.get(self, "webCrawlerConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="s3ConfigurationInput")
    def s3_configuration_input(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationS3Configuration"]:
        return typing.cast(typing.Optional["KendraDataSourceConfigurationS3Configuration"], jsii.get(self, "s3ConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="templateConfigurationInput")
    def template_configuration_input(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationTemplateConfiguration"]:
        return typing.cast(typing.Optional["KendraDataSourceConfigurationTemplateConfiguration"], jsii.get(self, "templateConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="webCrawlerConfigurationInput")
    def web_crawler_configuration_input(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationWebCrawlerConfiguration"]:
        return typing.cast(typing.Optional["KendraDataSourceConfigurationWebCrawlerConfiguration"], jsii.get(self, "webCrawlerConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[KendraDataSourceConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4311bff8737b9d246927116d372c9c7273ff30433533f9094c48e3cfc5fdd1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfigurationS3Configuration",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "access_control_list_configuration": "accessControlListConfiguration",
        "documents_metadata_configuration": "documentsMetadataConfiguration",
        "exclusion_patterns": "exclusionPatterns",
        "inclusion_patterns": "inclusionPatterns",
        "inclusion_prefixes": "inclusionPrefixes",
    },
)
class KendraDataSourceConfigurationS3Configuration:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        access_control_list_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        documents_metadata_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param bucket_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#bucket_name KendraDataSource#bucket_name}.
        :param access_control_list_configuration: access_control_list_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#access_control_list_configuration KendraDataSource#access_control_list_configuration}
        :param documents_metadata_configuration: documents_metadata_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#documents_metadata_configuration KendraDataSource#documents_metadata_configuration}
        :param exclusion_patterns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#exclusion_patterns KendraDataSource#exclusion_patterns}.
        :param inclusion_patterns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#inclusion_patterns KendraDataSource#inclusion_patterns}.
        :param inclusion_prefixes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#inclusion_prefixes KendraDataSource#inclusion_prefixes}.
        '''
        if isinstance(access_control_list_configuration, dict):
            access_control_list_configuration = KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration(**access_control_list_configuration)
        if isinstance(documents_metadata_configuration, dict):
            documents_metadata_configuration = KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration(**documents_metadata_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14868cd02eeb81315a1452dbb2230f703ffb303beee7f6dea34f0e4950d1bdc9)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument access_control_list_configuration", value=access_control_list_configuration, expected_type=type_hints["access_control_list_configuration"])
            check_type(argname="argument documents_metadata_configuration", value=documents_metadata_configuration, expected_type=type_hints["documents_metadata_configuration"])
            check_type(argname="argument exclusion_patterns", value=exclusion_patterns, expected_type=type_hints["exclusion_patterns"])
            check_type(argname="argument inclusion_patterns", value=inclusion_patterns, expected_type=type_hints["inclusion_patterns"])
            check_type(argname="argument inclusion_prefixes", value=inclusion_prefixes, expected_type=type_hints["inclusion_prefixes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
        }
        if access_control_list_configuration is not None:
            self._values["access_control_list_configuration"] = access_control_list_configuration
        if documents_metadata_configuration is not None:
            self._values["documents_metadata_configuration"] = documents_metadata_configuration
        if exclusion_patterns is not None:
            self._values["exclusion_patterns"] = exclusion_patterns
        if inclusion_patterns is not None:
            self._values["inclusion_patterns"] = inclusion_patterns
        if inclusion_prefixes is not None:
            self._values["inclusion_prefixes"] = inclusion_prefixes

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#bucket_name KendraDataSource#bucket_name}.'''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_control_list_configuration(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration"]:
        '''access_control_list_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#access_control_list_configuration KendraDataSource#access_control_list_configuration}
        '''
        result = self._values.get("access_control_list_configuration")
        return typing.cast(typing.Optional["KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration"], result)

    @builtins.property
    def documents_metadata_configuration(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration"]:
        '''documents_metadata_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#documents_metadata_configuration KendraDataSource#documents_metadata_configuration}
        '''
        result = self._values.get("documents_metadata_configuration")
        return typing.cast(typing.Optional["KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration"], result)

    @builtins.property
    def exclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#exclusion_patterns KendraDataSource#exclusion_patterns}.'''
        result = self._values.get("exclusion_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def inclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#inclusion_patterns KendraDataSource#inclusion_patterns}.'''
        result = self._values.get("inclusion_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def inclusion_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#inclusion_prefixes KendraDataSource#inclusion_prefixes}.'''
        result = self._values.get("inclusion_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfigurationS3Configuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration",
    jsii_struct_bases=[],
    name_mapping={"key_path": "keyPath"},
)
class KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration:
    def __init__(self, *, key_path: typing.Optional[builtins.str] = None) -> None:
        '''
        :param key_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#key_path KendraDataSource#key_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4979ded08423165f07b4fac0135b7243b37c177ee085c085b0cbd14d951d2a0)
            check_type(argname="argument key_path", value=key_path, expected_type=type_hints["key_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key_path is not None:
            self._values["key_path"] = key_path

    @builtins.property
    def key_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#key_path KendraDataSource#key_path}.'''
        result = self._values.get("key_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceConfigurationS3ConfigurationAccessControlListConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfigurationS3ConfigurationAccessControlListConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__614760797d286f9faca7cd9acb7d05cf7b4848991d4b556e3bb4e5119ec23502)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKeyPath")
    def reset_key_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyPath", []))

    @builtins.property
    @jsii.member(jsii_name="keyPathInput")
    def key_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyPathInput"))

    @builtins.property
    @jsii.member(jsii_name="keyPath")
    def key_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyPath"))

    @key_path.setter
    def key_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29b709c0d0e487026f35e83212d211b2fdca801d377ab02c5cced5e43fe205b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdb552a83ea311fd523e3cf949be8368818a8fd77bd4e4588810f5277e10c8ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration",
    jsii_struct_bases=[],
    name_mapping={"s3_prefix": "s3Prefix"},
)
class KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration:
    def __init__(self, *, s3_prefix: typing.Optional[builtins.str] = None) -> None:
        '''
        :param s3_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#s3_prefix KendraDataSource#s3_prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__391b8de9e37dc26f022c7ea29fbc52bb9f49e195921d578c1b7e6ff9808ea721)
            check_type(argname="argument s3_prefix", value=s3_prefix, expected_type=type_hints["s3_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if s3_prefix is not None:
            self._values["s3_prefix"] = s3_prefix

    @builtins.property
    def s3_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#s3_prefix KendraDataSource#s3_prefix}.'''
        result = self._values.get("s3_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b03198f904a9024307998f362df69f4434009d5641d8382f27d987f8dd53739b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetS3Prefix")
    def reset_s3_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Prefix", []))

    @builtins.property
    @jsii.member(jsii_name="s3PrefixInput")
    def s3_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3PrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="s3Prefix")
    def s3_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Prefix"))

    @s3_prefix.setter
    def s3_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d31ce1de2f7b43fc01b41672ea482c3fe109db1b5271d5c85f30dfeb51ee4289)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Prefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cfd41d5dcc686a454df4b15410ca222e67060c7314049f2b3ed082581b3d258)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraDataSourceConfigurationS3ConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfigurationS3ConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__377447184ec21ba4c210523c0a1c686b7baee7827b6f6dd513568d0e20584417)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccessControlListConfiguration")
    def put_access_control_list_configuration(
        self,
        *,
        key_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#key_path KendraDataSource#key_path}.
        '''
        value = KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration(
            key_path=key_path
        )

        return typing.cast(None, jsii.invoke(self, "putAccessControlListConfiguration", [value]))

    @jsii.member(jsii_name="putDocumentsMetadataConfiguration")
    def put_documents_metadata_configuration(
        self,
        *,
        s3_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param s3_prefix: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#s3_prefix KendraDataSource#s3_prefix}.
        '''
        value = KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration(
            s3_prefix=s3_prefix
        )

        return typing.cast(None, jsii.invoke(self, "putDocumentsMetadataConfiguration", [value]))

    @jsii.member(jsii_name="resetAccessControlListConfiguration")
    def reset_access_control_list_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessControlListConfiguration", []))

    @jsii.member(jsii_name="resetDocumentsMetadataConfiguration")
    def reset_documents_metadata_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentsMetadataConfiguration", []))

    @jsii.member(jsii_name="resetExclusionPatterns")
    def reset_exclusion_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusionPatterns", []))

    @jsii.member(jsii_name="resetInclusionPatterns")
    def reset_inclusion_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInclusionPatterns", []))

    @jsii.member(jsii_name="resetInclusionPrefixes")
    def reset_inclusion_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInclusionPrefixes", []))

    @builtins.property
    @jsii.member(jsii_name="accessControlListConfiguration")
    def access_control_list_configuration(
        self,
    ) -> KendraDataSourceConfigurationS3ConfigurationAccessControlListConfigurationOutputReference:
        return typing.cast(KendraDataSourceConfigurationS3ConfigurationAccessControlListConfigurationOutputReference, jsii.get(self, "accessControlListConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="documentsMetadataConfiguration")
    def documents_metadata_configuration(
        self,
    ) -> KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfigurationOutputReference:
        return typing.cast(KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfigurationOutputReference, jsii.get(self, "documentsMetadataConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="accessControlListConfigurationInput")
    def access_control_list_configuration_input(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration], jsii.get(self, "accessControlListConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="documentsMetadataConfigurationInput")
    def documents_metadata_configuration_input(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration], jsii.get(self, "documentsMetadataConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusionPatternsInput")
    def exclusion_patterns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exclusionPatternsInput"))

    @builtins.property
    @jsii.member(jsii_name="inclusionPatternsInput")
    def inclusion_patterns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inclusionPatternsInput"))

    @builtins.property
    @jsii.member(jsii_name="inclusionPrefixesInput")
    def inclusion_prefixes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inclusionPrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3748ea74b6f06b558d82844efa64856e3352faf8e7201a883b7468d523fbf530)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exclusionPatterns")
    def exclusion_patterns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exclusionPatterns"))

    @exclusion_patterns.setter
    def exclusion_patterns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4208575c850a22cca7179f36e0dfad50d2259488e96353c44143df21572a930)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exclusionPatterns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inclusionPatterns")
    def inclusion_patterns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inclusionPatterns"))

    @inclusion_patterns.setter
    def inclusion_patterns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2476be289959f8a90676ab002971f7cc12e682050da4cb6c1c5fa1d762d6c91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inclusionPatterns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inclusionPrefixes")
    def inclusion_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inclusionPrefixes"))

    @inclusion_prefixes.setter
    def inclusion_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29a81581054c31afa916306202bd11079e87290f5c9173cfb617b524a779f669)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inclusionPrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationS3Configuration]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationS3Configuration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceConfigurationS3Configuration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64edd1ec0de6e73858c8cab8afaadd693cd4eb3f3e254d6b31d3700d994a7ac6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfigurationTemplateConfiguration",
    jsii_struct_bases=[],
    name_mapping={"template": "template"},
)
class KendraDataSourceConfigurationTemplateConfiguration:
    def __init__(self, *, template: builtins.str) -> None:
        '''
        :param template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#template KendraDataSource#template}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b7392cb25fe33a11273e79f1f32764e66f13ebe2825af22e47ed504c91135f6)
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "template": template,
        }

    @builtins.property
    def template(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#template KendraDataSource#template}.'''
        result = self._values.get("template")
        assert result is not None, "Required property 'template' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfigurationTemplateConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceConfigurationTemplateConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfigurationTemplateConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e1485943b33a83388e3377e8f5bebd27b914bdf242ca5ae5cca91b82f6823b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="templateInput")
    def template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateInput"))

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "template"))

    @template.setter
    def template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6120eb83bd4e82ae0343e27483417fc1bd02af3a8968a7f145105cc7071e77a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "template", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationTemplateConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationTemplateConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceConfigurationTemplateConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d0ab67d7d9922dec19c702d45967324787442e52218144a4d14a0f14d05180f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "urls": "urls",
        "authentication_configuration": "authenticationConfiguration",
        "crawl_depth": "crawlDepth",
        "max_content_size_per_page_in_mega_bytes": "maxContentSizePerPageInMegaBytes",
        "max_links_per_page": "maxLinksPerPage",
        "max_urls_per_minute_crawl_rate": "maxUrlsPerMinuteCrawlRate",
        "proxy_configuration": "proxyConfiguration",
        "url_exclusion_patterns": "urlExclusionPatterns",
        "url_inclusion_patterns": "urlInclusionPatterns",
    },
)
class KendraDataSourceConfigurationWebCrawlerConfiguration:
    def __init__(
        self,
        *,
        urls: typing.Union["KendraDataSourceConfigurationWebCrawlerConfigurationUrls", typing.Dict[builtins.str, typing.Any]],
        authentication_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        crawl_depth: typing.Optional[jsii.Number] = None,
        max_content_size_per_page_in_mega_bytes: typing.Optional[jsii.Number] = None,
        max_links_per_page: typing.Optional[jsii.Number] = None,
        max_urls_per_minute_crawl_rate: typing.Optional[jsii.Number] = None,
        proxy_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        url_exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        url_inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param urls: urls block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#urls KendraDataSource#urls}
        :param authentication_configuration: authentication_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#authentication_configuration KendraDataSource#authentication_configuration}
        :param crawl_depth: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#crawl_depth KendraDataSource#crawl_depth}.
        :param max_content_size_per_page_in_mega_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#max_content_size_per_page_in_mega_bytes KendraDataSource#max_content_size_per_page_in_mega_bytes}.
        :param max_links_per_page: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#max_links_per_page KendraDataSource#max_links_per_page}.
        :param max_urls_per_minute_crawl_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#max_urls_per_minute_crawl_rate KendraDataSource#max_urls_per_minute_crawl_rate}.
        :param proxy_configuration: proxy_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#proxy_configuration KendraDataSource#proxy_configuration}
        :param url_exclusion_patterns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#url_exclusion_patterns KendraDataSource#url_exclusion_patterns}.
        :param url_inclusion_patterns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#url_inclusion_patterns KendraDataSource#url_inclusion_patterns}.
        '''
        if isinstance(urls, dict):
            urls = KendraDataSourceConfigurationWebCrawlerConfigurationUrls(**urls)
        if isinstance(authentication_configuration, dict):
            authentication_configuration = KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration(**authentication_configuration)
        if isinstance(proxy_configuration, dict):
            proxy_configuration = KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration(**proxy_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60573d69b390b309ce053e2c5381898b17a162170e75c93b81af9c47f0d95779)
            check_type(argname="argument urls", value=urls, expected_type=type_hints["urls"])
            check_type(argname="argument authentication_configuration", value=authentication_configuration, expected_type=type_hints["authentication_configuration"])
            check_type(argname="argument crawl_depth", value=crawl_depth, expected_type=type_hints["crawl_depth"])
            check_type(argname="argument max_content_size_per_page_in_mega_bytes", value=max_content_size_per_page_in_mega_bytes, expected_type=type_hints["max_content_size_per_page_in_mega_bytes"])
            check_type(argname="argument max_links_per_page", value=max_links_per_page, expected_type=type_hints["max_links_per_page"])
            check_type(argname="argument max_urls_per_minute_crawl_rate", value=max_urls_per_minute_crawl_rate, expected_type=type_hints["max_urls_per_minute_crawl_rate"])
            check_type(argname="argument proxy_configuration", value=proxy_configuration, expected_type=type_hints["proxy_configuration"])
            check_type(argname="argument url_exclusion_patterns", value=url_exclusion_patterns, expected_type=type_hints["url_exclusion_patterns"])
            check_type(argname="argument url_inclusion_patterns", value=url_inclusion_patterns, expected_type=type_hints["url_inclusion_patterns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "urls": urls,
        }
        if authentication_configuration is not None:
            self._values["authentication_configuration"] = authentication_configuration
        if crawl_depth is not None:
            self._values["crawl_depth"] = crawl_depth
        if max_content_size_per_page_in_mega_bytes is not None:
            self._values["max_content_size_per_page_in_mega_bytes"] = max_content_size_per_page_in_mega_bytes
        if max_links_per_page is not None:
            self._values["max_links_per_page"] = max_links_per_page
        if max_urls_per_minute_crawl_rate is not None:
            self._values["max_urls_per_minute_crawl_rate"] = max_urls_per_minute_crawl_rate
        if proxy_configuration is not None:
            self._values["proxy_configuration"] = proxy_configuration
        if url_exclusion_patterns is not None:
            self._values["url_exclusion_patterns"] = url_exclusion_patterns
        if url_inclusion_patterns is not None:
            self._values["url_inclusion_patterns"] = url_inclusion_patterns

    @builtins.property
    def urls(self) -> "KendraDataSourceConfigurationWebCrawlerConfigurationUrls":
        '''urls block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#urls KendraDataSource#urls}
        '''
        result = self._values.get("urls")
        assert result is not None, "Required property 'urls' is missing"
        return typing.cast("KendraDataSourceConfigurationWebCrawlerConfigurationUrls", result)

    @builtins.property
    def authentication_configuration(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration"]:
        '''authentication_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#authentication_configuration KendraDataSource#authentication_configuration}
        '''
        result = self._values.get("authentication_configuration")
        return typing.cast(typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration"], result)

    @builtins.property
    def crawl_depth(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#crawl_depth KendraDataSource#crawl_depth}.'''
        result = self._values.get("crawl_depth")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_content_size_per_page_in_mega_bytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#max_content_size_per_page_in_mega_bytes KendraDataSource#max_content_size_per_page_in_mega_bytes}.'''
        result = self._values.get("max_content_size_per_page_in_mega_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_links_per_page(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#max_links_per_page KendraDataSource#max_links_per_page}.'''
        result = self._values.get("max_links_per_page")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_urls_per_minute_crawl_rate(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#max_urls_per_minute_crawl_rate KendraDataSource#max_urls_per_minute_crawl_rate}.'''
        result = self._values.get("max_urls_per_minute_crawl_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def proxy_configuration(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration"]:
        '''proxy_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#proxy_configuration KendraDataSource#proxy_configuration}
        '''
        result = self._values.get("proxy_configuration")
        return typing.cast(typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration"], result)

    @builtins.property
    def url_exclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#url_exclusion_patterns KendraDataSource#url_exclusion_patterns}.'''
        result = self._values.get("url_exclusion_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def url_inclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#url_inclusion_patterns KendraDataSource#url_inclusion_patterns}.'''
        result = self._values.get("url_inclusion_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfigurationWebCrawlerConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration",
    jsii_struct_bases=[],
    name_mapping={"basic_authentication": "basicAuthentication"},
)
class KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration:
    def __init__(
        self,
        *,
        basic_authentication: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param basic_authentication: basic_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#basic_authentication KendraDataSource#basic_authentication}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cdf295e3ad7c3a330ba9f26f891c3505ec1471c7e4e86cca952b9b62139c7e1)
            check_type(argname="argument basic_authentication", value=basic_authentication, expected_type=type_hints["basic_authentication"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if basic_authentication is not None:
            self._values["basic_authentication"] = basic_authentication

    @builtins.property
    def basic_authentication(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication"]]]:
        '''basic_authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#basic_authentication KendraDataSource#basic_authentication}
        '''
        result = self._values.get("basic_authentication")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication",
    jsii_struct_bases=[],
    name_mapping={"credentials": "credentials", "host": "host", "port": "port"},
)
class KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication:
    def __init__(
        self,
        *,
        credentials: builtins.str,
        host: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''
        :param credentials: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#credentials KendraDataSource#credentials}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#host KendraDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#port KendraDataSource#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1398dc54280b1c95a6e8534f6a1e890e2a03c2d58eebb25eff2cc8f01c19064a)
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "credentials": credentials,
            "host": host,
            "port": port,
        }

    @builtins.property
    def credentials(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#credentials KendraDataSource#credentials}.'''
        result = self._values.get("credentials")
        assert result is not None, "Required property 'credentials' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#host KendraDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#port KendraDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthenticationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthenticationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54bc2073c331179d82ff8254f066936865a5c6503a3b4e015ba543917edb1510)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthenticationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1be841a7113343c1dc224bcbb70b3c48b21bd72107faa7f5da6cd317b178e59b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthenticationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b245d76c9b5a20c8f84e2c058e97e2eb6fe510e7988a5ef34596e5bf72942a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0225f44047e80c74f74cee2d5813845614bcbf25e9641188cee7776cc3f2992b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a08ff2eb5147a6b8e5e41eccdda4c785122f25e6d9ccb9db90e37993328885a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87d75b13e7369f97184d61f5f4e5c878d0f69c4621638235322b69649b96392b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68a7f0e8eb461f2d4d43a3a0d23ebef4d5779c74c0951eb1e4326c10482f66ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="credentialsInput")
    def credentials_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="credentials")
    def credentials(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentials"))

    @credentials.setter
    def credentials(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44a23ec6693b16cacfe1f8fc9b23cf62a1e048e6c2bc0bbc565444e9c49e79ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f99e84855aadcb0a2a678ff890fc5aff76168dc8b73ac5543bac46c01ac0b39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a753f8f61edf17d4ad1445d90994cb6ba1c1a4caf99221acffbbe7512ea5e168)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f24385f654eb14b3622585bb6f2c1e0094840a0b336d61bd1c6eb7979825a54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f0e9dcf376a03d6b5a400fb936843cab19c41b314b5c4bd0db2d2be42f8ba2a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBasicAuthentication")
    def put_basic_authentication(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d09a3dbd00798bcdaca270bce551560167a37c668476118d8c4d1c29d866e990)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBasicAuthentication", [value]))

    @jsii.member(jsii_name="resetBasicAuthentication")
    def reset_basic_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBasicAuthentication", []))

    @builtins.property
    @jsii.member(jsii_name="basicAuthentication")
    def basic_authentication(
        self,
    ) -> KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthenticationList:
        return typing.cast(KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthenticationList, jsii.get(self, "basicAuthentication"))

    @builtins.property
    @jsii.member(jsii_name="basicAuthenticationInput")
    def basic_authentication_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication]]], jsii.get(self, "basicAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50429eb6ab7f266d71186b3b52970fa9485a738e9b1b77642ead041a6e8de2f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraDataSourceConfigurationWebCrawlerConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a61d658d7133ecff148c87596b592a3e18891a4edd6aad3e509ff4c3b015f711)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthenticationConfiguration")
    def put_authentication_configuration(
        self,
        *,
        basic_authentication: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param basic_authentication: basic_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#basic_authentication KendraDataSource#basic_authentication}
        '''
        value = KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration(
            basic_authentication=basic_authentication
        )

        return typing.cast(None, jsii.invoke(self, "putAuthenticationConfiguration", [value]))

    @jsii.member(jsii_name="putProxyConfiguration")
    def put_proxy_configuration(
        self,
        *,
        host: builtins.str,
        port: jsii.Number,
        credentials: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#host KendraDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#port KendraDataSource#port}.
        :param credentials: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#credentials KendraDataSource#credentials}.
        '''
        value = KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration(
            host=host, port=port, credentials=credentials
        )

        return typing.cast(None, jsii.invoke(self, "putProxyConfiguration", [value]))

    @jsii.member(jsii_name="putUrls")
    def put_urls(
        self,
        *,
        seed_url_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        site_maps_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param seed_url_configuration: seed_url_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#seed_url_configuration KendraDataSource#seed_url_configuration}
        :param site_maps_configuration: site_maps_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#site_maps_configuration KendraDataSource#site_maps_configuration}
        '''
        value = KendraDataSourceConfigurationWebCrawlerConfigurationUrls(
            seed_url_configuration=seed_url_configuration,
            site_maps_configuration=site_maps_configuration,
        )

        return typing.cast(None, jsii.invoke(self, "putUrls", [value]))

    @jsii.member(jsii_name="resetAuthenticationConfiguration")
    def reset_authentication_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationConfiguration", []))

    @jsii.member(jsii_name="resetCrawlDepth")
    def reset_crawl_depth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrawlDepth", []))

    @jsii.member(jsii_name="resetMaxContentSizePerPageInMegaBytes")
    def reset_max_content_size_per_page_in_mega_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxContentSizePerPageInMegaBytes", []))

    @jsii.member(jsii_name="resetMaxLinksPerPage")
    def reset_max_links_per_page(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxLinksPerPage", []))

    @jsii.member(jsii_name="resetMaxUrlsPerMinuteCrawlRate")
    def reset_max_urls_per_minute_crawl_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxUrlsPerMinuteCrawlRate", []))

    @jsii.member(jsii_name="resetProxyConfiguration")
    def reset_proxy_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyConfiguration", []))

    @jsii.member(jsii_name="resetUrlExclusionPatterns")
    def reset_url_exclusion_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlExclusionPatterns", []))

    @jsii.member(jsii_name="resetUrlInclusionPatterns")
    def reset_url_inclusion_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlInclusionPatterns", []))

    @builtins.property
    @jsii.member(jsii_name="authenticationConfiguration")
    def authentication_configuration(
        self,
    ) -> KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationOutputReference:
        return typing.cast(KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationOutputReference, jsii.get(self, "authenticationConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="proxyConfiguration")
    def proxy_configuration(
        self,
    ) -> "KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfigurationOutputReference":
        return typing.cast("KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfigurationOutputReference", jsii.get(self, "proxyConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="urls")
    def urls(
        self,
    ) -> "KendraDataSourceConfigurationWebCrawlerConfigurationUrlsOutputReference":
        return typing.cast("KendraDataSourceConfigurationWebCrawlerConfigurationUrlsOutputReference", jsii.get(self, "urls"))

    @builtins.property
    @jsii.member(jsii_name="authenticationConfigurationInput")
    def authentication_configuration_input(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration], jsii.get(self, "authenticationConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="crawlDepthInput")
    def crawl_depth_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "crawlDepthInput"))

    @builtins.property
    @jsii.member(jsii_name="maxContentSizePerPageInMegaBytesInput")
    def max_content_size_per_page_in_mega_bytes_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxContentSizePerPageInMegaBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="maxLinksPerPageInput")
    def max_links_per_page_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxLinksPerPageInput"))

    @builtins.property
    @jsii.member(jsii_name="maxUrlsPerMinuteCrawlRateInput")
    def max_urls_per_minute_crawl_rate_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxUrlsPerMinuteCrawlRateInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyConfigurationInput")
    def proxy_configuration_input(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration"]:
        return typing.cast(typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration"], jsii.get(self, "proxyConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="urlExclusionPatternsInput")
    def url_exclusion_patterns_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "urlExclusionPatternsInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInclusionPatternsInput")
    def url_inclusion_patterns_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "urlInclusionPatternsInput"))

    @builtins.property
    @jsii.member(jsii_name="urlsInput")
    def urls_input(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationUrls"]:
        return typing.cast(typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationUrls"], jsii.get(self, "urlsInput"))

    @builtins.property
    @jsii.member(jsii_name="crawlDepth")
    def crawl_depth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "crawlDepth"))

    @crawl_depth.setter
    def crawl_depth(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57f4e8d67769d76d4ed7982a2acfad07816f2c1f9b00cdf73c9dbd93f7a623dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crawlDepth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxContentSizePerPageInMegaBytes")
    def max_content_size_per_page_in_mega_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxContentSizePerPageInMegaBytes"))

    @max_content_size_per_page_in_mega_bytes.setter
    def max_content_size_per_page_in_mega_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6308e23cd8e38f39fb8e77c6cb9850012d2117f20aef9af8d8003bad87e1db34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxContentSizePerPageInMegaBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxLinksPerPage")
    def max_links_per_page(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxLinksPerPage"))

    @max_links_per_page.setter
    def max_links_per_page(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e570ab658e36943958dff243114b1f1f1289546a6d7bf3bd7b768545134acd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxLinksPerPage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxUrlsPerMinuteCrawlRate")
    def max_urls_per_minute_crawl_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxUrlsPerMinuteCrawlRate"))

    @max_urls_per_minute_crawl_rate.setter
    def max_urls_per_minute_crawl_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__269d6a9db5e94f0cf201c519a1a382a72d7a5654f04f9959c4fa94f518a7ede0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxUrlsPerMinuteCrawlRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urlExclusionPatterns")
    def url_exclusion_patterns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "urlExclusionPatterns"))

    @url_exclusion_patterns.setter
    def url_exclusion_patterns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81a75d9a298c98c949fc2b06c55eacf87b27c02874d3bc86ed6e4cd25e1735e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urlExclusionPatterns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urlInclusionPatterns")
    def url_inclusion_patterns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "urlInclusionPatterns"))

    @url_inclusion_patterns.setter
    def url_inclusion_patterns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f02b99ffd03191677673b9de168f353ab9f46abab6519e086c3157b8ae5ee288)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urlInclusionPatterns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationWebCrawlerConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationWebCrawlerConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceConfigurationWebCrawlerConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9142aa81645558749e6047e8da3022520259ff1f03e89052f924ed43eff76fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration",
    jsii_struct_bases=[],
    name_mapping={"host": "host", "port": "port", "credentials": "credentials"},
)
class KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration:
    def __init__(
        self,
        *,
        host: builtins.str,
        port: jsii.Number,
        credentials: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#host KendraDataSource#host}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#port KendraDataSource#port}.
        :param credentials: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#credentials KendraDataSource#credentials}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4a28e475cf043a03e2d33cba36540d1f8de1178d75bb352941bd3f2e414c909)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host": host,
            "port": port,
        }
        if credentials is not None:
            self._values["credentials"] = credentials

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#host KendraDataSource#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#port KendraDataSource#port}.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def credentials(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#credentials KendraDataSource#credentials}.'''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd7a20aca04a6cf35ae07cb7a733fa0c2e8da98d9b385f2e3cdb5a5a87913572)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCredentials")
    def reset_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentials", []))

    @builtins.property
    @jsii.member(jsii_name="credentialsInput")
    def credentials_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "credentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="credentials")
    def credentials(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "credentials"))

    @credentials.setter
    def credentials(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abbb9570a7a9bec4e4be06fc7d1b9974d7644f6d604755319fcbd78beb43a1e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13a4d8c6678dd75c09c571a17a04672f88a1ddc154a5801e8bc993fe6c761f97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1f895b4b604f4034ea64cb7ffe273dc2f28fa6754b4638ef9a116b8f5365e8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19fef78fe0f7e00e7d2978dd0b3491ac20affb4822cf9a129659e658eaeaea52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationUrls",
    jsii_struct_bases=[],
    name_mapping={
        "seed_url_configuration": "seedUrlConfiguration",
        "site_maps_configuration": "siteMapsConfiguration",
    },
)
class KendraDataSourceConfigurationWebCrawlerConfigurationUrls:
    def __init__(
        self,
        *,
        seed_url_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        site_maps_configuration: typing.Optional[typing.Union["KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param seed_url_configuration: seed_url_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#seed_url_configuration KendraDataSource#seed_url_configuration}
        :param site_maps_configuration: site_maps_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#site_maps_configuration KendraDataSource#site_maps_configuration}
        '''
        if isinstance(seed_url_configuration, dict):
            seed_url_configuration = KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration(**seed_url_configuration)
        if isinstance(site_maps_configuration, dict):
            site_maps_configuration = KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration(**site_maps_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fd08ac2965ef9f7f37ba19435c8be680af2c623a53f74c5549118cabd141027)
            check_type(argname="argument seed_url_configuration", value=seed_url_configuration, expected_type=type_hints["seed_url_configuration"])
            check_type(argname="argument site_maps_configuration", value=site_maps_configuration, expected_type=type_hints["site_maps_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if seed_url_configuration is not None:
            self._values["seed_url_configuration"] = seed_url_configuration
        if site_maps_configuration is not None:
            self._values["site_maps_configuration"] = site_maps_configuration

    @builtins.property
    def seed_url_configuration(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration"]:
        '''seed_url_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#seed_url_configuration KendraDataSource#seed_url_configuration}
        '''
        result = self._values.get("seed_url_configuration")
        return typing.cast(typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration"], result)

    @builtins.property
    def site_maps_configuration(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration"]:
        '''site_maps_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#site_maps_configuration KendraDataSource#site_maps_configuration}
        '''
        result = self._values.get("site_maps_configuration")
        return typing.cast(typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfigurationWebCrawlerConfigurationUrls(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceConfigurationWebCrawlerConfigurationUrlsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationUrlsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__591c8142ace51bd2cd827ce8eba949fdc7446689877a7a0ef9fe77d87f612e0d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSeedUrlConfiguration")
    def put_seed_url_configuration(
        self,
        *,
        seed_urls: typing.Sequence[builtins.str],
        web_crawler_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param seed_urls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#seed_urls KendraDataSource#seed_urls}.
        :param web_crawler_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#web_crawler_mode KendraDataSource#web_crawler_mode}.
        '''
        value = KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration(
            seed_urls=seed_urls, web_crawler_mode=web_crawler_mode
        )

        return typing.cast(None, jsii.invoke(self, "putSeedUrlConfiguration", [value]))

    @jsii.member(jsii_name="putSiteMapsConfiguration")
    def put_site_maps_configuration(
        self,
        *,
        site_maps: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param site_maps: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#site_maps KendraDataSource#site_maps}.
        '''
        value = KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration(
            site_maps=site_maps
        )

        return typing.cast(None, jsii.invoke(self, "putSiteMapsConfiguration", [value]))

    @jsii.member(jsii_name="resetSeedUrlConfiguration")
    def reset_seed_url_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeedUrlConfiguration", []))

    @jsii.member(jsii_name="resetSiteMapsConfiguration")
    def reset_site_maps_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSiteMapsConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="seedUrlConfiguration")
    def seed_url_configuration(
        self,
    ) -> "KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfigurationOutputReference":
        return typing.cast("KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfigurationOutputReference", jsii.get(self, "seedUrlConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="siteMapsConfiguration")
    def site_maps_configuration(
        self,
    ) -> "KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfigurationOutputReference":
        return typing.cast("KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfigurationOutputReference", jsii.get(self, "siteMapsConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="seedUrlConfigurationInput")
    def seed_url_configuration_input(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration"]:
        return typing.cast(typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration"], jsii.get(self, "seedUrlConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="siteMapsConfigurationInput")
    def site_maps_configuration_input(
        self,
    ) -> typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration"]:
        return typing.cast(typing.Optional["KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration"], jsii.get(self, "siteMapsConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationUrls]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationUrls], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationUrls],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__604dd32932f83c6df950becd92e8c040aaa63e5cd059624881cc8d2410a61e7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration",
    jsii_struct_bases=[],
    name_mapping={"seed_urls": "seedUrls", "web_crawler_mode": "webCrawlerMode"},
)
class KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration:
    def __init__(
        self,
        *,
        seed_urls: typing.Sequence[builtins.str],
        web_crawler_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param seed_urls: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#seed_urls KendraDataSource#seed_urls}.
        :param web_crawler_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#web_crawler_mode KendraDataSource#web_crawler_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__accf063ff811c335d20239a62d744fd1663a7c842370738df337a915011f0df8)
            check_type(argname="argument seed_urls", value=seed_urls, expected_type=type_hints["seed_urls"])
            check_type(argname="argument web_crawler_mode", value=web_crawler_mode, expected_type=type_hints["web_crawler_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "seed_urls": seed_urls,
        }
        if web_crawler_mode is not None:
            self._values["web_crawler_mode"] = web_crawler_mode

    @builtins.property
    def seed_urls(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#seed_urls KendraDataSource#seed_urls}.'''
        result = self._values.get("seed_urls")
        assert result is not None, "Required property 'seed_urls' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def web_crawler_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#web_crawler_mode KendraDataSource#web_crawler_mode}.'''
        result = self._values.get("web_crawler_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0748d1756046567bb4301c67b7dd0f85ea6a6a8df952eb20b35e2482f4df633b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetWebCrawlerMode")
    def reset_web_crawler_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebCrawlerMode", []))

    @builtins.property
    @jsii.member(jsii_name="seedUrlsInput")
    def seed_urls_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "seedUrlsInput"))

    @builtins.property
    @jsii.member(jsii_name="webCrawlerModeInput")
    def web_crawler_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webCrawlerModeInput"))

    @builtins.property
    @jsii.member(jsii_name="seedUrls")
    def seed_urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "seedUrls"))

    @seed_urls.setter
    def seed_urls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94d30dcbce06d9b557fb40c070e29efe9a716377cd8d3d717e7b82eb940c5740)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seedUrls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webCrawlerMode")
    def web_crawler_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webCrawlerMode"))

    @web_crawler_mode.setter
    def web_crawler_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2006be9ee78b5a0d7518e1cf0bbae16b4a618ffeb0b08566539f0dec630cef52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webCrawlerMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9c46f0dd39363df727e7de08127a0797a6abbdd0e54f01c73afde2415bd1f5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration",
    jsii_struct_bases=[],
    name_mapping={"site_maps": "siteMaps"},
)
class KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration:
    def __init__(self, *, site_maps: typing.Sequence[builtins.str]) -> None:
        '''
        :param site_maps: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#site_maps KendraDataSource#site_maps}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a500df945e9ea3034a7dc1431d8160c06032e9aef4e5a4c5dd7e0a50a7e2ff89)
            check_type(argname="argument site_maps", value=site_maps, expected_type=type_hints["site_maps"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "site_maps": site_maps,
        }

    @builtins.property
    def site_maps(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#site_maps KendraDataSource#site_maps}.'''
        result = self._values.get("site_maps")
        assert result is not None, "Required property 'site_maps' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7d9cc6d5898ee4680653c15e4bf70c6aa947a64f8fd22043504deceaf043e3d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="siteMapsInput")
    def site_maps_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "siteMapsInput"))

    @builtins.property
    @jsii.member(jsii_name="siteMaps")
    def site_maps(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "siteMaps"))

    @site_maps.setter
    def site_maps(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a15cafefe5ce00a160f850f2d6f0dd6199435f4b99bfb6cd7b3228212d17f3b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "siteMaps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff8ddbfdd5e92ddab2e6a203c6fce6c12cfad3e2f97925eeeba274899deae33e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "inline_configurations": "inlineConfigurations",
        "post_extraction_hook_configuration": "postExtractionHookConfiguration",
        "pre_extraction_hook_configuration": "preExtractionHookConfiguration",
        "role_arn": "roleArn",
    },
)
class KendraDataSourceCustomDocumentEnrichmentConfiguration:
    def __init__(
        self,
        *,
        inline_configurations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        post_extraction_hook_configuration: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        pre_extraction_hook_configuration: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param inline_configurations: inline_configurations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#inline_configurations KendraDataSource#inline_configurations}
        :param post_extraction_hook_configuration: post_extraction_hook_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#post_extraction_hook_configuration KendraDataSource#post_extraction_hook_configuration}
        :param pre_extraction_hook_configuration: pre_extraction_hook_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#pre_extraction_hook_configuration KendraDataSource#pre_extraction_hook_configuration}
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#role_arn KendraDataSource#role_arn}.
        '''
        if isinstance(post_extraction_hook_configuration, dict):
            post_extraction_hook_configuration = KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration(**post_extraction_hook_configuration)
        if isinstance(pre_extraction_hook_configuration, dict):
            pre_extraction_hook_configuration = KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration(**pre_extraction_hook_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca97bec22f615c8851dc2bb26dcc3bd38a2f395498ca54c8ffa8432626aed21a)
            check_type(argname="argument inline_configurations", value=inline_configurations, expected_type=type_hints["inline_configurations"])
            check_type(argname="argument post_extraction_hook_configuration", value=post_extraction_hook_configuration, expected_type=type_hints["post_extraction_hook_configuration"])
            check_type(argname="argument pre_extraction_hook_configuration", value=pre_extraction_hook_configuration, expected_type=type_hints["pre_extraction_hook_configuration"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if inline_configurations is not None:
            self._values["inline_configurations"] = inline_configurations
        if post_extraction_hook_configuration is not None:
            self._values["post_extraction_hook_configuration"] = post_extraction_hook_configuration
        if pre_extraction_hook_configuration is not None:
            self._values["pre_extraction_hook_configuration"] = pre_extraction_hook_configuration
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def inline_configurations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations"]]]:
        '''inline_configurations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#inline_configurations KendraDataSource#inline_configurations}
        '''
        result = self._values.get("inline_configurations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations"]]], result)

    @builtins.property
    def post_extraction_hook_configuration(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration"]:
        '''post_extraction_hook_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#post_extraction_hook_configuration KendraDataSource#post_extraction_hook_configuration}
        '''
        result = self._values.get("post_extraction_hook_configuration")
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration"], result)

    @builtins.property
    def pre_extraction_hook_configuration(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration"]:
        '''pre_extraction_hook_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#pre_extraction_hook_configuration KendraDataSource#pre_extraction_hook_configuration}
        '''
        result = self._values.get("pre_extraction_hook_configuration")
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration"], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#role_arn KendraDataSource#role_arn}.'''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceCustomDocumentEnrichmentConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations",
    jsii_struct_bases=[],
    name_mapping={
        "condition": "condition",
        "document_content_deletion": "documentContentDeletion",
        "target": "target",
    },
)
class KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations:
    def __init__(
        self,
        *,
        condition: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        document_content_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        target: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#condition KendraDataSource#condition}
        :param document_content_deletion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#document_content_deletion KendraDataSource#document_content_deletion}.
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#target KendraDataSource#target}
        '''
        if isinstance(condition, dict):
            condition = KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition(**condition)
        if isinstance(target, dict):
            target = KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget(**target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a95729cc2ec5d41e4e1857db8756e206e2e802751db594b5a77399ce38b2c5a8)
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument document_content_deletion", value=document_content_deletion, expected_type=type_hints["document_content_deletion"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if condition is not None:
            self._values["condition"] = condition
        if document_content_deletion is not None:
            self._values["document_content_deletion"] = document_content_deletion
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def condition(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition"]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#condition KendraDataSource#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition"], result)

    @builtins.property
    def document_content_deletion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#document_content_deletion KendraDataSource#document_content_deletion}.'''
        result = self._values.get("document_content_deletion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def target(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget"]:
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#target KendraDataSource#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition",
    jsii_struct_bases=[],
    name_mapping={
        "condition_document_attribute_key": "conditionDocumentAttributeKey",
        "operator": "operator",
        "condition_on_value": "conditionOnValue",
    },
)
class KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition:
    def __init__(
        self,
        *,
        condition_document_attribute_key: builtins.str,
        operator: builtins.str,
        condition_on_value: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param condition_document_attribute_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#condition_document_attribute_key KendraDataSource#condition_document_attribute_key}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#operator KendraDataSource#operator}.
        :param condition_on_value: condition_on_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#condition_on_value KendraDataSource#condition_on_value}
        '''
        if isinstance(condition_on_value, dict):
            condition_on_value = KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue(**condition_on_value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3829374b8ce0393bbd420a21184976a5aef23cbf5819d8bd4f37817f007bc06)
            check_type(argname="argument condition_document_attribute_key", value=condition_document_attribute_key, expected_type=type_hints["condition_document_attribute_key"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument condition_on_value", value=condition_on_value, expected_type=type_hints["condition_on_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "condition_document_attribute_key": condition_document_attribute_key,
            "operator": operator,
        }
        if condition_on_value is not None:
            self._values["condition_on_value"] = condition_on_value

    @builtins.property
    def condition_document_attribute_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#condition_document_attribute_key KendraDataSource#condition_document_attribute_key}.'''
        result = self._values.get("condition_document_attribute_key")
        assert result is not None, "Required property 'condition_document_attribute_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#operator KendraDataSource#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition_on_value(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue"]:
        '''condition_on_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#condition_on_value KendraDataSource#condition_on_value}
        '''
        result = self._values.get("condition_on_value")
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue",
    jsii_struct_bases=[],
    name_mapping={
        "date_value": "dateValue",
        "long_value": "longValue",
        "string_list_value": "stringListValue",
        "string_value": "stringValue",
    },
)
class KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue:
    def __init__(
        self,
        *,
        date_value: typing.Optional[builtins.str] = None,
        long_value: typing.Optional[jsii.Number] = None,
        string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param date_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#date_value KendraDataSource#date_value}.
        :param long_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#long_value KendraDataSource#long_value}.
        :param string_list_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#string_list_value KendraDataSource#string_list_value}.
        :param string_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#string_value KendraDataSource#string_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07027ac4ece4958e53744a46668d1f8589ec79f6b3cbec9c62db33e106747364)
            check_type(argname="argument date_value", value=date_value, expected_type=type_hints["date_value"])
            check_type(argname="argument long_value", value=long_value, expected_type=type_hints["long_value"])
            check_type(argname="argument string_list_value", value=string_list_value, expected_type=type_hints["string_list_value"])
            check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if date_value is not None:
            self._values["date_value"] = date_value
        if long_value is not None:
            self._values["long_value"] = long_value
        if string_list_value is not None:
            self._values["string_list_value"] = string_list_value
        if string_value is not None:
            self._values["string_value"] = string_value

    @builtins.property
    def date_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#date_value KendraDataSource#date_value}.'''
        result = self._values.get("date_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def long_value(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#long_value KendraDataSource#long_value}.'''
        result = self._values.get("long_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def string_list_value(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#string_list_value KendraDataSource#string_list_value}.'''
        result = self._values.get("string_list_value")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#string_value KendraDataSource#string_value}.'''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32c3a16499c749976a3c970cd84191d0c47e74e39e08e3d4aad9f11128317c08)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDateValue")
    def reset_date_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateValue", []))

    @jsii.member(jsii_name="resetLongValue")
    def reset_long_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLongValue", []))

    @jsii.member(jsii_name="resetStringListValue")
    def reset_string_list_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringListValue", []))

    @jsii.member(jsii_name="resetStringValue")
    def reset_string_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringValue", []))

    @builtins.property
    @jsii.member(jsii_name="dateValueInput")
    def date_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dateValueInput"))

    @builtins.property
    @jsii.member(jsii_name="longValueInput")
    def long_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "longValueInput"))

    @builtins.property
    @jsii.member(jsii_name="stringListValueInput")
    def string_list_value_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "stringListValueInput"))

    @builtins.property
    @jsii.member(jsii_name="stringValueInput")
    def string_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stringValueInput"))

    @builtins.property
    @jsii.member(jsii_name="dateValue")
    def date_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dateValue"))

    @date_value.setter
    def date_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03b43185c02eee2c270d9050438c4a04a3d5fb1a6a3cb2e1dbdbb48851c1457a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dateValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="longValue")
    def long_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "longValue"))

    @long_value.setter
    def long_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5caab1d316ffb51f3b191bd02782ea3f86333b861caadd929c64ef20d9d61bf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "longValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringListValue")
    def string_list_value(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stringListValue"))

    @string_list_value.setter
    def string_list_value(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0bc749ab4476020a1bbf92c6c53ff2d76de2758d5683b849c8b860d20763638)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringListValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stringValue"))

    @string_value.setter
    def string_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9481895c630c1838730b876c693e8728741a36dd14a922087a6a0aff03ce0ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ffbd3c92f052b1c97149e454399d5e203d4e9143e963f3ff25060067556c68d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d376dcdaa1fda0b81d1e2938e6d6a13b816ffddb66e4c0be91448147adee5a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConditionOnValue")
    def put_condition_on_value(
        self,
        *,
        date_value: typing.Optional[builtins.str] = None,
        long_value: typing.Optional[jsii.Number] = None,
        string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param date_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#date_value KendraDataSource#date_value}.
        :param long_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#long_value KendraDataSource#long_value}.
        :param string_list_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#string_list_value KendraDataSource#string_list_value}.
        :param string_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#string_value KendraDataSource#string_value}.
        '''
        value = KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue(
            date_value=date_value,
            long_value=long_value,
            string_list_value=string_list_value,
            string_value=string_value,
        )

        return typing.cast(None, jsii.invoke(self, "putConditionOnValue", [value]))

    @jsii.member(jsii_name="resetConditionOnValue")
    def reset_condition_on_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditionOnValue", []))

    @builtins.property
    @jsii.member(jsii_name="conditionOnValue")
    def condition_on_value(
        self,
    ) -> KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValueOutputReference:
        return typing.cast(KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValueOutputReference, jsii.get(self, "conditionOnValue"))

    @builtins.property
    @jsii.member(jsii_name="conditionDocumentAttributeKeyInput")
    def condition_document_attribute_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionDocumentAttributeKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionOnValueInput")
    def condition_on_value_input(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue], jsii.get(self, "conditionOnValueInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionDocumentAttributeKey")
    def condition_document_attribute_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conditionDocumentAttributeKey"))

    @condition_document_attribute_key.setter
    def condition_document_attribute_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b97e1e6b0d8e912b7abd950a305103e12b879bb9c005740733d0ecb48737693a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conditionDocumentAttributeKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37dabbca442d639199b2e8fc1a4ec063a755135b643f70afe24964f9ab6a97a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6ef84b06640a7b4d4d4354110551a93af8f91ee6ed364d6b438305d221a87f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62ce4fcba6f3b65a6d7c888a33b50d7b5d89b9c9f55e07df099134e07965c80f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc4c0f438f60a7692ada22aa2f2dfea1bd2a05418e2e3fa03ff21f8788bde257)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ead77504dd915ff185a6693c7cc4b3a974d145e5bb207cc182289a3f3fdf37c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8697fc92b4b57127b21d0dcc59cda22635a00de1f0bbf84efeeed15ee2a98c91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db7f778b4664185b5344b58bbd71bdc1103d92949e68b097839ae112e4f300ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6773ce6083d041fb4e0d092f62c647da5a8819a69112db078ea35032e1f865a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0eccea1901fe88bb81f2926318595973aa3372f37382878c287432e2189ca8e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        *,
        condition_document_attribute_key: builtins.str,
        operator: builtins.str,
        condition_on_value: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param condition_document_attribute_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#condition_document_attribute_key KendraDataSource#condition_document_attribute_key}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#operator KendraDataSource#operator}.
        :param condition_on_value: condition_on_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#condition_on_value KendraDataSource#condition_on_value}
        '''
        value = KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition(
            condition_document_attribute_key=condition_document_attribute_key,
            operator=operator,
            condition_on_value=condition_on_value,
        )

        return typing.cast(None, jsii.invoke(self, "putCondition", [value]))

    @jsii.member(jsii_name="putTarget")
    def put_target(
        self,
        *,
        target_document_attribute_key: typing.Optional[builtins.str] = None,
        target_document_attribute_value: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue", typing.Dict[builtins.str, typing.Any]]] = None,
        target_document_attribute_value_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param target_document_attribute_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#target_document_attribute_key KendraDataSource#target_document_attribute_key}.
        :param target_document_attribute_value: target_document_attribute_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#target_document_attribute_value KendraDataSource#target_document_attribute_value}
        :param target_document_attribute_value_deletion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#target_document_attribute_value_deletion KendraDataSource#target_document_attribute_value_deletion}.
        '''
        value = KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget(
            target_document_attribute_key=target_document_attribute_key,
            target_document_attribute_value=target_document_attribute_value,
            target_document_attribute_value_deletion=target_document_attribute_value_deletion,
        )

        return typing.cast(None, jsii.invoke(self, "putTarget", [value]))

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetDocumentContentDeletion")
    def reset_document_content_deletion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentContentDeletion", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(
        self,
    ) -> KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionOutputReference:
        return typing.cast(KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionOutputReference, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(
        self,
    ) -> "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetOutputReference":
        return typing.cast("KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetOutputReference", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="documentContentDeletionInput")
    def document_content_deletion_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "documentContentDeletionInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget"]:
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget"], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="documentContentDeletion")
    def document_content_deletion(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "documentContentDeletion"))

    @document_content_deletion.setter
    def document_content_deletion(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9559f8c6023d0d540fb8ff9136a01435483bf57c59f81b42ff15c0ec7eeec9c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documentContentDeletion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d7e5a5a5a91cda7468af4e05e788e2a1c9f4a0dd7c79f0d07c02aee1f733ae5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget",
    jsii_struct_bases=[],
    name_mapping={
        "target_document_attribute_key": "targetDocumentAttributeKey",
        "target_document_attribute_value": "targetDocumentAttributeValue",
        "target_document_attribute_value_deletion": "targetDocumentAttributeValueDeletion",
    },
)
class KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget:
    def __init__(
        self,
        *,
        target_document_attribute_key: typing.Optional[builtins.str] = None,
        target_document_attribute_value: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue", typing.Dict[builtins.str, typing.Any]]] = None,
        target_document_attribute_value_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param target_document_attribute_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#target_document_attribute_key KendraDataSource#target_document_attribute_key}.
        :param target_document_attribute_value: target_document_attribute_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#target_document_attribute_value KendraDataSource#target_document_attribute_value}
        :param target_document_attribute_value_deletion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#target_document_attribute_value_deletion KendraDataSource#target_document_attribute_value_deletion}.
        '''
        if isinstance(target_document_attribute_value, dict):
            target_document_attribute_value = KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue(**target_document_attribute_value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0f9dce499602eb3af9747d2d01d402af538613c4c45f8c1b674f6a31536edc4)
            check_type(argname="argument target_document_attribute_key", value=target_document_attribute_key, expected_type=type_hints["target_document_attribute_key"])
            check_type(argname="argument target_document_attribute_value", value=target_document_attribute_value, expected_type=type_hints["target_document_attribute_value"])
            check_type(argname="argument target_document_attribute_value_deletion", value=target_document_attribute_value_deletion, expected_type=type_hints["target_document_attribute_value_deletion"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if target_document_attribute_key is not None:
            self._values["target_document_attribute_key"] = target_document_attribute_key
        if target_document_attribute_value is not None:
            self._values["target_document_attribute_value"] = target_document_attribute_value
        if target_document_attribute_value_deletion is not None:
            self._values["target_document_attribute_value_deletion"] = target_document_attribute_value_deletion

    @builtins.property
    def target_document_attribute_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#target_document_attribute_key KendraDataSource#target_document_attribute_key}.'''
        result = self._values.get("target_document_attribute_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_document_attribute_value(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue"]:
        '''target_document_attribute_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#target_document_attribute_value KendraDataSource#target_document_attribute_value}
        '''
        result = self._values.get("target_document_attribute_value")
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue"], result)

    @builtins.property
    def target_document_attribute_value_deletion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#target_document_attribute_value_deletion KendraDataSource#target_document_attribute_value_deletion}.'''
        result = self._values.get("target_document_attribute_value_deletion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c9059dd09ca5886c5d4e7a88080c5c143812c59e96900d60e50c7da9b16683d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTargetDocumentAttributeValue")
    def put_target_document_attribute_value(
        self,
        *,
        date_value: typing.Optional[builtins.str] = None,
        long_value: typing.Optional[jsii.Number] = None,
        string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param date_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#date_value KendraDataSource#date_value}.
        :param long_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#long_value KendraDataSource#long_value}.
        :param string_list_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#string_list_value KendraDataSource#string_list_value}.
        :param string_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#string_value KendraDataSource#string_value}.
        '''
        value = KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue(
            date_value=date_value,
            long_value=long_value,
            string_list_value=string_list_value,
            string_value=string_value,
        )

        return typing.cast(None, jsii.invoke(self, "putTargetDocumentAttributeValue", [value]))

    @jsii.member(jsii_name="resetTargetDocumentAttributeKey")
    def reset_target_document_attribute_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetDocumentAttributeKey", []))

    @jsii.member(jsii_name="resetTargetDocumentAttributeValue")
    def reset_target_document_attribute_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetDocumentAttributeValue", []))

    @jsii.member(jsii_name="resetTargetDocumentAttributeValueDeletion")
    def reset_target_document_attribute_value_deletion(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetDocumentAttributeValueDeletion", []))

    @builtins.property
    @jsii.member(jsii_name="targetDocumentAttributeValue")
    def target_document_attribute_value(
        self,
    ) -> "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValueOutputReference":
        return typing.cast("KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValueOutputReference", jsii.get(self, "targetDocumentAttributeValue"))

    @builtins.property
    @jsii.member(jsii_name="targetDocumentAttributeKeyInput")
    def target_document_attribute_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetDocumentAttributeKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="targetDocumentAttributeValueDeletionInput")
    def target_document_attribute_value_deletion_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "targetDocumentAttributeValueDeletionInput"))

    @builtins.property
    @jsii.member(jsii_name="targetDocumentAttributeValueInput")
    def target_document_attribute_value_input(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue"]:
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue"], jsii.get(self, "targetDocumentAttributeValueInput"))

    @builtins.property
    @jsii.member(jsii_name="targetDocumentAttributeKey")
    def target_document_attribute_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetDocumentAttributeKey"))

    @target_document_attribute_key.setter
    def target_document_attribute_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6c4f1bd94c16f4a021d2794f51781621d806b763c9376d6639413463b1a2e20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetDocumentAttributeKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetDocumentAttributeValueDeletion")
    def target_document_attribute_value_deletion(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "targetDocumentAttributeValueDeletion"))

    @target_document_attribute_value_deletion.setter
    def target_document_attribute_value_deletion(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f448e920fa38a5c782add36e994cfe1ca03aa7509d9dfd563f2a62e3a670b753)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetDocumentAttributeValueDeletion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__499a27499462ffc1aecf625a245e6986d80a934ad6734e8c3c30876b49451412)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue",
    jsii_struct_bases=[],
    name_mapping={
        "date_value": "dateValue",
        "long_value": "longValue",
        "string_list_value": "stringListValue",
        "string_value": "stringValue",
    },
)
class KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue:
    def __init__(
        self,
        *,
        date_value: typing.Optional[builtins.str] = None,
        long_value: typing.Optional[jsii.Number] = None,
        string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param date_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#date_value KendraDataSource#date_value}.
        :param long_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#long_value KendraDataSource#long_value}.
        :param string_list_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#string_list_value KendraDataSource#string_list_value}.
        :param string_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#string_value KendraDataSource#string_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b1897d9891cc52661cfb8f7bfc9e032d6ff9f2ada84bfd6e2b4b52230231c85)
            check_type(argname="argument date_value", value=date_value, expected_type=type_hints["date_value"])
            check_type(argname="argument long_value", value=long_value, expected_type=type_hints["long_value"])
            check_type(argname="argument string_list_value", value=string_list_value, expected_type=type_hints["string_list_value"])
            check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if date_value is not None:
            self._values["date_value"] = date_value
        if long_value is not None:
            self._values["long_value"] = long_value
        if string_list_value is not None:
            self._values["string_list_value"] = string_list_value
        if string_value is not None:
            self._values["string_value"] = string_value

    @builtins.property
    def date_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#date_value KendraDataSource#date_value}.'''
        result = self._values.get("date_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def long_value(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#long_value KendraDataSource#long_value}.'''
        result = self._values.get("long_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def string_list_value(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#string_list_value KendraDataSource#string_list_value}.'''
        result = self._values.get("string_list_value")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#string_value KendraDataSource#string_value}.'''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6dd602ea82cd1d86d12ba2a8db4c6d7d0cab9e5eeecf4d4483efd2cb2d41c3f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDateValue")
    def reset_date_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateValue", []))

    @jsii.member(jsii_name="resetLongValue")
    def reset_long_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLongValue", []))

    @jsii.member(jsii_name="resetStringListValue")
    def reset_string_list_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringListValue", []))

    @jsii.member(jsii_name="resetStringValue")
    def reset_string_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringValue", []))

    @builtins.property
    @jsii.member(jsii_name="dateValueInput")
    def date_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dateValueInput"))

    @builtins.property
    @jsii.member(jsii_name="longValueInput")
    def long_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "longValueInput"))

    @builtins.property
    @jsii.member(jsii_name="stringListValueInput")
    def string_list_value_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "stringListValueInput"))

    @builtins.property
    @jsii.member(jsii_name="stringValueInput")
    def string_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stringValueInput"))

    @builtins.property
    @jsii.member(jsii_name="dateValue")
    def date_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dateValue"))

    @date_value.setter
    def date_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94db43b9d120ecfb737dbc7bb9b361187a4d89b205768dcc5668dfef2e183ab6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dateValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="longValue")
    def long_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "longValue"))

    @long_value.setter
    def long_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__961820718d05159d6de76e0e675996ecdd934cc1cb7e1859ccb06a2d4f0bd6de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "longValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringListValue")
    def string_list_value(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stringListValue"))

    @string_list_value.setter
    def string_list_value(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__609244fd1e0902a25693abdf631c48dd379690d00333e1a6049cf6ea70efbe95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringListValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stringValue"))

    @string_value.setter
    def string_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12aa2867569aaa621a6eceb583bce5e4b11706dca451cf7fe02ec199cf595c0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63272bba77c2399c30ca0797f261b180f8f5ff4b63d27c42723b38251eb4ac90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraDataSourceCustomDocumentEnrichmentConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a802050aed6aeafefd1e402f82734347f9b5bb1b372cbf1215085a396ebd3c8a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInlineConfigurations")
    def put_inline_configurations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a37349163957e804cc865e3958ab39315f6dc2cd89bc17fc59dddaaa0b3bc91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInlineConfigurations", [value]))

    @jsii.member(jsii_name="putPostExtractionHookConfiguration")
    def put_post_extraction_hook_configuration(
        self,
        *,
        lambda_arn: builtins.str,
        s3_bucket: builtins.str,
        invocation_condition: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param lambda_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#lambda_arn KendraDataSource#lambda_arn}.
        :param s3_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#s3_bucket KendraDataSource#s3_bucket}.
        :param invocation_condition: invocation_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#invocation_condition KendraDataSource#invocation_condition}
        '''
        value = KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration(
            lambda_arn=lambda_arn,
            s3_bucket=s3_bucket,
            invocation_condition=invocation_condition,
        )

        return typing.cast(None, jsii.invoke(self, "putPostExtractionHookConfiguration", [value]))

    @jsii.member(jsii_name="putPreExtractionHookConfiguration")
    def put_pre_extraction_hook_configuration(
        self,
        *,
        lambda_arn: builtins.str,
        s3_bucket: builtins.str,
        invocation_condition: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param lambda_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#lambda_arn KendraDataSource#lambda_arn}.
        :param s3_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#s3_bucket KendraDataSource#s3_bucket}.
        :param invocation_condition: invocation_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#invocation_condition KendraDataSource#invocation_condition}
        '''
        value = KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration(
            lambda_arn=lambda_arn,
            s3_bucket=s3_bucket,
            invocation_condition=invocation_condition,
        )

        return typing.cast(None, jsii.invoke(self, "putPreExtractionHookConfiguration", [value]))

    @jsii.member(jsii_name="resetInlineConfigurations")
    def reset_inline_configurations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInlineConfigurations", []))

    @jsii.member(jsii_name="resetPostExtractionHookConfiguration")
    def reset_post_extraction_hook_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostExtractionHookConfiguration", []))

    @jsii.member(jsii_name="resetPreExtractionHookConfiguration")
    def reset_pre_extraction_hook_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreExtractionHookConfiguration", []))

    @jsii.member(jsii_name="resetRoleArn")
    def reset_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoleArn", []))

    @builtins.property
    @jsii.member(jsii_name="inlineConfigurations")
    def inline_configurations(
        self,
    ) -> KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsList:
        return typing.cast(KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsList, jsii.get(self, "inlineConfigurations"))

    @builtins.property
    @jsii.member(jsii_name="postExtractionHookConfiguration")
    def post_extraction_hook_configuration(
        self,
    ) -> "KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationOutputReference":
        return typing.cast("KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationOutputReference", jsii.get(self, "postExtractionHookConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="preExtractionHookConfiguration")
    def pre_extraction_hook_configuration(
        self,
    ) -> "KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationOutputReference":
        return typing.cast("KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationOutputReference", jsii.get(self, "preExtractionHookConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="inlineConfigurationsInput")
    def inline_configurations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations]]], jsii.get(self, "inlineConfigurationsInput"))

    @builtins.property
    @jsii.member(jsii_name="postExtractionHookConfigurationInput")
    def post_extraction_hook_configuration_input(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration"]:
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration"], jsii.get(self, "postExtractionHookConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="preExtractionHookConfigurationInput")
    def pre_extraction_hook_configuration_input(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration"]:
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration"], jsii.get(self, "preExtractionHookConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4a7160ddd8a64807b4613808e336c5c45adcbbbf023415d94307b571b286635)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d5af5b193e153e889d72671843793ce8717e70df16f560dd4382184921cb4eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "lambda_arn": "lambdaArn",
        "s3_bucket": "s3Bucket",
        "invocation_condition": "invocationCondition",
    },
)
class KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration:
    def __init__(
        self,
        *,
        lambda_arn: builtins.str,
        s3_bucket: builtins.str,
        invocation_condition: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param lambda_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#lambda_arn KendraDataSource#lambda_arn}.
        :param s3_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#s3_bucket KendraDataSource#s3_bucket}.
        :param invocation_condition: invocation_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#invocation_condition KendraDataSource#invocation_condition}
        '''
        if isinstance(invocation_condition, dict):
            invocation_condition = KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition(**invocation_condition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94b89b3e90ceb94180a2a331c1c9b1e2a61b52f296281784db648c68abb3445f)
            check_type(argname="argument lambda_arn", value=lambda_arn, expected_type=type_hints["lambda_arn"])
            check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
            check_type(argname="argument invocation_condition", value=invocation_condition, expected_type=type_hints["invocation_condition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lambda_arn": lambda_arn,
            "s3_bucket": s3_bucket,
        }
        if invocation_condition is not None:
            self._values["invocation_condition"] = invocation_condition

    @builtins.property
    def lambda_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#lambda_arn KendraDataSource#lambda_arn}.'''
        result = self._values.get("lambda_arn")
        assert result is not None, "Required property 'lambda_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_bucket(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#s3_bucket KendraDataSource#s3_bucket}.'''
        result = self._values.get("s3_bucket")
        assert result is not None, "Required property 's3_bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def invocation_condition(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition"]:
        '''invocation_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#invocation_condition KendraDataSource#invocation_condition}
        '''
        result = self._values.get("invocation_condition")
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition",
    jsii_struct_bases=[],
    name_mapping={
        "condition_document_attribute_key": "conditionDocumentAttributeKey",
        "operator": "operator",
        "condition_on_value": "conditionOnValue",
    },
)
class KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition:
    def __init__(
        self,
        *,
        condition_document_attribute_key: builtins.str,
        operator: builtins.str,
        condition_on_value: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param condition_document_attribute_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#condition_document_attribute_key KendraDataSource#condition_document_attribute_key}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#operator KendraDataSource#operator}.
        :param condition_on_value: condition_on_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#condition_on_value KendraDataSource#condition_on_value}
        '''
        if isinstance(condition_on_value, dict):
            condition_on_value = KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue(**condition_on_value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b5a9981acd65c6dc1b84655118ead31177df4ece8470339b4fceea51e65c293)
            check_type(argname="argument condition_document_attribute_key", value=condition_document_attribute_key, expected_type=type_hints["condition_document_attribute_key"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument condition_on_value", value=condition_on_value, expected_type=type_hints["condition_on_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "condition_document_attribute_key": condition_document_attribute_key,
            "operator": operator,
        }
        if condition_on_value is not None:
            self._values["condition_on_value"] = condition_on_value

    @builtins.property
    def condition_document_attribute_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#condition_document_attribute_key KendraDataSource#condition_document_attribute_key}.'''
        result = self._values.get("condition_document_attribute_key")
        assert result is not None, "Required property 'condition_document_attribute_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#operator KendraDataSource#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition_on_value(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue"]:
        '''condition_on_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#condition_on_value KendraDataSource#condition_on_value}
        '''
        result = self._values.get("condition_on_value")
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue",
    jsii_struct_bases=[],
    name_mapping={
        "date_value": "dateValue",
        "long_value": "longValue",
        "string_list_value": "stringListValue",
        "string_value": "stringValue",
    },
)
class KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue:
    def __init__(
        self,
        *,
        date_value: typing.Optional[builtins.str] = None,
        long_value: typing.Optional[jsii.Number] = None,
        string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param date_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#date_value KendraDataSource#date_value}.
        :param long_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#long_value KendraDataSource#long_value}.
        :param string_list_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#string_list_value KendraDataSource#string_list_value}.
        :param string_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#string_value KendraDataSource#string_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96ad55b3fc3c1bad9b2741d437121c3836eada48fe3b306866a638f5d5086ffb)
            check_type(argname="argument date_value", value=date_value, expected_type=type_hints["date_value"])
            check_type(argname="argument long_value", value=long_value, expected_type=type_hints["long_value"])
            check_type(argname="argument string_list_value", value=string_list_value, expected_type=type_hints["string_list_value"])
            check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if date_value is not None:
            self._values["date_value"] = date_value
        if long_value is not None:
            self._values["long_value"] = long_value
        if string_list_value is not None:
            self._values["string_list_value"] = string_list_value
        if string_value is not None:
            self._values["string_value"] = string_value

    @builtins.property
    def date_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#date_value KendraDataSource#date_value}.'''
        result = self._values.get("date_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def long_value(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#long_value KendraDataSource#long_value}.'''
        result = self._values.get("long_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def string_list_value(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#string_list_value KendraDataSource#string_list_value}.'''
        result = self._values.get("string_list_value")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#string_value KendraDataSource#string_value}.'''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__832828cd21387267f12ea438a81001f49c3e0b9d6ad47e0d61e3f7f852f5b71f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDateValue")
    def reset_date_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateValue", []))

    @jsii.member(jsii_name="resetLongValue")
    def reset_long_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLongValue", []))

    @jsii.member(jsii_name="resetStringListValue")
    def reset_string_list_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringListValue", []))

    @jsii.member(jsii_name="resetStringValue")
    def reset_string_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringValue", []))

    @builtins.property
    @jsii.member(jsii_name="dateValueInput")
    def date_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dateValueInput"))

    @builtins.property
    @jsii.member(jsii_name="longValueInput")
    def long_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "longValueInput"))

    @builtins.property
    @jsii.member(jsii_name="stringListValueInput")
    def string_list_value_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "stringListValueInput"))

    @builtins.property
    @jsii.member(jsii_name="stringValueInput")
    def string_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stringValueInput"))

    @builtins.property
    @jsii.member(jsii_name="dateValue")
    def date_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dateValue"))

    @date_value.setter
    def date_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81cc0d9afefeeb974034a808f0f7e0f2e76f34dcebe15cc932a7f214d02b75bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dateValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="longValue")
    def long_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "longValue"))

    @long_value.setter
    def long_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__974ca8d0746360a5d887bd5aa09e9b3220a4062b82c5b2882cb5162fa25a8b51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "longValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringListValue")
    def string_list_value(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stringListValue"))

    @string_list_value.setter
    def string_list_value(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70bd634b2eb8a136eb5f3856de5bdf40647f985d531d7875383304db4c99c13f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringListValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stringValue"))

    @string_value.setter
    def string_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6ed5c29c52116abd48d9dcb042f2bd9b05e0a9a0b29da5b2fc33d4983d88fd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f17316d16d60d268e16f4e3e6ba363b06c94bb2e8aa5b6b11ed62be19556afe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ce1a342928eb8a24eaf5dec29a1c6af5fa786dd2e1abb62264504d7d656c239)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConditionOnValue")
    def put_condition_on_value(
        self,
        *,
        date_value: typing.Optional[builtins.str] = None,
        long_value: typing.Optional[jsii.Number] = None,
        string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param date_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#date_value KendraDataSource#date_value}.
        :param long_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#long_value KendraDataSource#long_value}.
        :param string_list_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#string_list_value KendraDataSource#string_list_value}.
        :param string_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#string_value KendraDataSource#string_value}.
        '''
        value = KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue(
            date_value=date_value,
            long_value=long_value,
            string_list_value=string_list_value,
            string_value=string_value,
        )

        return typing.cast(None, jsii.invoke(self, "putConditionOnValue", [value]))

    @jsii.member(jsii_name="resetConditionOnValue")
    def reset_condition_on_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditionOnValue", []))

    @builtins.property
    @jsii.member(jsii_name="conditionOnValue")
    def condition_on_value(
        self,
    ) -> KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValueOutputReference:
        return typing.cast(KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValueOutputReference, jsii.get(self, "conditionOnValue"))

    @builtins.property
    @jsii.member(jsii_name="conditionDocumentAttributeKeyInput")
    def condition_document_attribute_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionDocumentAttributeKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionOnValueInput")
    def condition_on_value_input(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue], jsii.get(self, "conditionOnValueInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionDocumentAttributeKey")
    def condition_document_attribute_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conditionDocumentAttributeKey"))

    @condition_document_attribute_key.setter
    def condition_document_attribute_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88c462c9f48b4bd7a474fc8c926774d059e4f72abe3c1e72e1d2709749670dd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conditionDocumentAttributeKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdaff859224c84d28d1ee7007262267342b0de2ac4aae102e49cfa00e6a7d291)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e090a450fe64ee80ce48bca0f61cd48f9aa25d3491222d437b79aba3c1b9d4be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d168492dde03cc50529fba526af4bb62bba774b1fb2bbf0014c01e4fbe8a9dac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInvocationCondition")
    def put_invocation_condition(
        self,
        *,
        condition_document_attribute_key: builtins.str,
        operator: builtins.str,
        condition_on_value: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param condition_document_attribute_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#condition_document_attribute_key KendraDataSource#condition_document_attribute_key}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#operator KendraDataSource#operator}.
        :param condition_on_value: condition_on_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#condition_on_value KendraDataSource#condition_on_value}
        '''
        value = KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition(
            condition_document_attribute_key=condition_document_attribute_key,
            operator=operator,
            condition_on_value=condition_on_value,
        )

        return typing.cast(None, jsii.invoke(self, "putInvocationCondition", [value]))

    @jsii.member(jsii_name="resetInvocationCondition")
    def reset_invocation_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvocationCondition", []))

    @builtins.property
    @jsii.member(jsii_name="invocationCondition")
    def invocation_condition(
        self,
    ) -> KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionOutputReference:
        return typing.cast(KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionOutputReference, jsii.get(self, "invocationCondition"))

    @builtins.property
    @jsii.member(jsii_name="invocationConditionInput")
    def invocation_condition_input(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition], jsii.get(self, "invocationConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaArnInput")
    def lambda_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lambdaArnInput"))

    @builtins.property
    @jsii.member(jsii_name="s3BucketInput")
    def s3_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3BucketInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaArn")
    def lambda_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lambdaArn"))

    @lambda_arn.setter
    def lambda_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a04e3ef5c8f29a1c08000526a9059441488d86d3b69a20d2e830ad7375b7d89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3Bucket")
    def s3_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Bucket"))

    @s3_bucket.setter
    def s3_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cae18ef77df3de5e2a3216608526abc823735a9b75258b5f6314d728de394c6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00aa594a06accab7ba2b4d8e645a0efc1e6339cdb2eb442b6efb5400d7cde67a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "lambda_arn": "lambdaArn",
        "s3_bucket": "s3Bucket",
        "invocation_condition": "invocationCondition",
    },
)
class KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration:
    def __init__(
        self,
        *,
        lambda_arn: builtins.str,
        s3_bucket: builtins.str,
        invocation_condition: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param lambda_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#lambda_arn KendraDataSource#lambda_arn}.
        :param s3_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#s3_bucket KendraDataSource#s3_bucket}.
        :param invocation_condition: invocation_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#invocation_condition KendraDataSource#invocation_condition}
        '''
        if isinstance(invocation_condition, dict):
            invocation_condition = KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition(**invocation_condition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__178d7e6a98768f110ea4414beda653e370d56d4140317f4ee480f7aaf6789b41)
            check_type(argname="argument lambda_arn", value=lambda_arn, expected_type=type_hints["lambda_arn"])
            check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
            check_type(argname="argument invocation_condition", value=invocation_condition, expected_type=type_hints["invocation_condition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lambda_arn": lambda_arn,
            "s3_bucket": s3_bucket,
        }
        if invocation_condition is not None:
            self._values["invocation_condition"] = invocation_condition

    @builtins.property
    def lambda_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#lambda_arn KendraDataSource#lambda_arn}.'''
        result = self._values.get("lambda_arn")
        assert result is not None, "Required property 'lambda_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_bucket(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#s3_bucket KendraDataSource#s3_bucket}.'''
        result = self._values.get("s3_bucket")
        assert result is not None, "Required property 's3_bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def invocation_condition(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition"]:
        '''invocation_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#invocation_condition KendraDataSource#invocation_condition}
        '''
        result = self._values.get("invocation_condition")
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition",
    jsii_struct_bases=[],
    name_mapping={
        "condition_document_attribute_key": "conditionDocumentAttributeKey",
        "operator": "operator",
        "condition_on_value": "conditionOnValue",
    },
)
class KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition:
    def __init__(
        self,
        *,
        condition_document_attribute_key: builtins.str,
        operator: builtins.str,
        condition_on_value: typing.Optional[typing.Union["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param condition_document_attribute_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#condition_document_attribute_key KendraDataSource#condition_document_attribute_key}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#operator KendraDataSource#operator}.
        :param condition_on_value: condition_on_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#condition_on_value KendraDataSource#condition_on_value}
        '''
        if isinstance(condition_on_value, dict):
            condition_on_value = KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue(**condition_on_value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b3874df348a22f8929fb36b2faa29f11ccb2e82468dafddc260e4c428be9b35)
            check_type(argname="argument condition_document_attribute_key", value=condition_document_attribute_key, expected_type=type_hints["condition_document_attribute_key"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument condition_on_value", value=condition_on_value, expected_type=type_hints["condition_on_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "condition_document_attribute_key": condition_document_attribute_key,
            "operator": operator,
        }
        if condition_on_value is not None:
            self._values["condition_on_value"] = condition_on_value

    @builtins.property
    def condition_document_attribute_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#condition_document_attribute_key KendraDataSource#condition_document_attribute_key}.'''
        result = self._values.get("condition_document_attribute_key")
        assert result is not None, "Required property 'condition_document_attribute_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#operator KendraDataSource#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition_on_value(
        self,
    ) -> typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue"]:
        '''condition_on_value block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#condition_on_value KendraDataSource#condition_on_value}
        '''
        result = self._values.get("condition_on_value")
        return typing.cast(typing.Optional["KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue",
    jsii_struct_bases=[],
    name_mapping={
        "date_value": "dateValue",
        "long_value": "longValue",
        "string_list_value": "stringListValue",
        "string_value": "stringValue",
    },
)
class KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue:
    def __init__(
        self,
        *,
        date_value: typing.Optional[builtins.str] = None,
        long_value: typing.Optional[jsii.Number] = None,
        string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param date_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#date_value KendraDataSource#date_value}.
        :param long_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#long_value KendraDataSource#long_value}.
        :param string_list_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#string_list_value KendraDataSource#string_list_value}.
        :param string_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#string_value KendraDataSource#string_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__524e7a2c82f3f35218252ed7acd6ab0aa9f0b23fa3904aabe3de0b3331b69da3)
            check_type(argname="argument date_value", value=date_value, expected_type=type_hints["date_value"])
            check_type(argname="argument long_value", value=long_value, expected_type=type_hints["long_value"])
            check_type(argname="argument string_list_value", value=string_list_value, expected_type=type_hints["string_list_value"])
            check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if date_value is not None:
            self._values["date_value"] = date_value
        if long_value is not None:
            self._values["long_value"] = long_value
        if string_list_value is not None:
            self._values["string_list_value"] = string_list_value
        if string_value is not None:
            self._values["string_value"] = string_value

    @builtins.property
    def date_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#date_value KendraDataSource#date_value}.'''
        result = self._values.get("date_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def long_value(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#long_value KendraDataSource#long_value}.'''
        result = self._values.get("long_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def string_list_value(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#string_list_value KendraDataSource#string_list_value}.'''
        result = self._values.get("string_list_value")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def string_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#string_value KendraDataSource#string_value}.'''
        result = self._values.get("string_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2188dc13b1baec7a6aa98906d33213575bd7d0aee0bb3ad37568660a66af9f6c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDateValue")
    def reset_date_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateValue", []))

    @jsii.member(jsii_name="resetLongValue")
    def reset_long_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLongValue", []))

    @jsii.member(jsii_name="resetStringListValue")
    def reset_string_list_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringListValue", []))

    @jsii.member(jsii_name="resetStringValue")
    def reset_string_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStringValue", []))

    @builtins.property
    @jsii.member(jsii_name="dateValueInput")
    def date_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dateValueInput"))

    @builtins.property
    @jsii.member(jsii_name="longValueInput")
    def long_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "longValueInput"))

    @builtins.property
    @jsii.member(jsii_name="stringListValueInput")
    def string_list_value_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "stringListValueInput"))

    @builtins.property
    @jsii.member(jsii_name="stringValueInput")
    def string_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stringValueInput"))

    @builtins.property
    @jsii.member(jsii_name="dateValue")
    def date_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dateValue"))

    @date_value.setter
    def date_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__852d620babb0ce2583e05ab48cfb58c914b4af85e42ff82927654f209195e866)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dateValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="longValue")
    def long_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "longValue"))

    @long_value.setter
    def long_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef557f9db711ff2a4a8a0d3bd98c4b43663aa794bbe9ec3b4f724c1b2cebec95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "longValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringListValue")
    def string_list_value(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "stringListValue"))

    @string_list_value.setter
    def string_list_value(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc73cc19b7c62562e8e196c4029f5f2cbbec4bbfa2da877bab1ba2ca933c60c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringListValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stringValue"))

    @string_value.setter
    def string_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b126cc463e07358057b03a5bd18e487b5393eedf179b1e68c2af51b61bfd8cc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stringValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb2733173cf0eaaefed2c2efdb5fff2d62aa0e33a0e3efa822da66001d80e9ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9965291a14dba086ff95092922b63149ce216d3532330731a15909547c8d83fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConditionOnValue")
    def put_condition_on_value(
        self,
        *,
        date_value: typing.Optional[builtins.str] = None,
        long_value: typing.Optional[jsii.Number] = None,
        string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
        string_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param date_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#date_value KendraDataSource#date_value}.
        :param long_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#long_value KendraDataSource#long_value}.
        :param string_list_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#string_list_value KendraDataSource#string_list_value}.
        :param string_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#string_value KendraDataSource#string_value}.
        '''
        value = KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue(
            date_value=date_value,
            long_value=long_value,
            string_list_value=string_list_value,
            string_value=string_value,
        )

        return typing.cast(None, jsii.invoke(self, "putConditionOnValue", [value]))

    @jsii.member(jsii_name="resetConditionOnValue")
    def reset_condition_on_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditionOnValue", []))

    @builtins.property
    @jsii.member(jsii_name="conditionOnValue")
    def condition_on_value(
        self,
    ) -> KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValueOutputReference:
        return typing.cast(KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValueOutputReference, jsii.get(self, "conditionOnValue"))

    @builtins.property
    @jsii.member(jsii_name="conditionDocumentAttributeKeyInput")
    def condition_document_attribute_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionDocumentAttributeKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionOnValueInput")
    def condition_on_value_input(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue], jsii.get(self, "conditionOnValueInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionDocumentAttributeKey")
    def condition_document_attribute_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conditionDocumentAttributeKey"))

    @condition_document_attribute_key.setter
    def condition_document_attribute_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ccdbfff19750f7d012badef459553b49f7727b9debbfd8b0d52b095c962dd07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conditionDocumentAttributeKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e9a77259e9d3466a447dac969b75ab43e8eaeed4ab6a3b674482c03802eb5e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f71db1f095b69d79eb0d583f3702c7a34afb58f3cad479bcee6a5cf3b844528d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__abfa26f23ea67de8b0dfd14917417587dac412b9a3dc98d98f14a9a45273d1fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInvocationCondition")
    def put_invocation_condition(
        self,
        *,
        condition_document_attribute_key: builtins.str,
        operator: builtins.str,
        condition_on_value: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param condition_document_attribute_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#condition_document_attribute_key KendraDataSource#condition_document_attribute_key}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#operator KendraDataSource#operator}.
        :param condition_on_value: condition_on_value block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#condition_on_value KendraDataSource#condition_on_value}
        '''
        value = KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition(
            condition_document_attribute_key=condition_document_attribute_key,
            operator=operator,
            condition_on_value=condition_on_value,
        )

        return typing.cast(None, jsii.invoke(self, "putInvocationCondition", [value]))

    @jsii.member(jsii_name="resetInvocationCondition")
    def reset_invocation_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvocationCondition", []))

    @builtins.property
    @jsii.member(jsii_name="invocationCondition")
    def invocation_condition(
        self,
    ) -> KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionOutputReference:
        return typing.cast(KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionOutputReference, jsii.get(self, "invocationCondition"))

    @builtins.property
    @jsii.member(jsii_name="invocationConditionInput")
    def invocation_condition_input(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition], jsii.get(self, "invocationConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaArnInput")
    def lambda_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lambdaArnInput"))

    @builtins.property
    @jsii.member(jsii_name="s3BucketInput")
    def s3_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3BucketInput"))

    @builtins.property
    @jsii.member(jsii_name="lambdaArn")
    def lambda_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lambdaArn"))

    @lambda_arn.setter
    def lambda_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a5e02f9302a87a1f70a2ed5a4290a7574d49fa53091aae75754f9af32a001f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="s3Bucket")
    def s3_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3Bucket"))

    @s3_bucket.setter
    def s3_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3590cdfe59554980c8d5ea46cd6a0b87a18605a51d835d963822e3f3fbd1b4fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration]:
        return typing.cast(typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__514f3099e796533d16ad0dfc0ee4db483e15f91399c5ba823baea9fd8bdbf61a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class KendraDataSourceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#create KendraDataSource#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#delete KendraDataSource#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#update KendraDataSource#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8bd7541e9304f7d416691eb47d2f0d2c4b06fc1df05b867d39365237770ec34)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#create KendraDataSource#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#delete KendraDataSource#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/kendra_data_source#update KendraDataSource#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KendraDataSourceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KendraDataSourceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.kendraDataSource.KendraDataSourceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__542e068156577db182bfbb1e0ed8b03f86e84d766ae6bdd34324f92d2d5f8ef9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__363a385c01f1683594af0485f0e45470276ab2e7814b3a8b5561d56492af9b29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fea4083afb56345c4ff2372e43270f8bbb23362d1f60f64f36c3310223196b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14b93990fda9a57b9563dfcd3e98f71ab3f51ef7b8d0d8891024b98cee5607df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraDataSourceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraDataSourceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraDataSourceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__704bca85e887be69b0770d3bd47d457ebd287338107cf040782e208af6f4d989)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "KendraDataSource",
    "KendraDataSourceConfig",
    "KendraDataSourceConfiguration",
    "KendraDataSourceConfigurationOutputReference",
    "KendraDataSourceConfigurationS3Configuration",
    "KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration",
    "KendraDataSourceConfigurationS3ConfigurationAccessControlListConfigurationOutputReference",
    "KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration",
    "KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfigurationOutputReference",
    "KendraDataSourceConfigurationS3ConfigurationOutputReference",
    "KendraDataSourceConfigurationTemplateConfiguration",
    "KendraDataSourceConfigurationTemplateConfigurationOutputReference",
    "KendraDataSourceConfigurationWebCrawlerConfiguration",
    "KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration",
    "KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication",
    "KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthenticationList",
    "KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthenticationOutputReference",
    "KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationOutputReference",
    "KendraDataSourceConfigurationWebCrawlerConfigurationOutputReference",
    "KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration",
    "KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfigurationOutputReference",
    "KendraDataSourceConfigurationWebCrawlerConfigurationUrls",
    "KendraDataSourceConfigurationWebCrawlerConfigurationUrlsOutputReference",
    "KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration",
    "KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfigurationOutputReference",
    "KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration",
    "KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfigurationOutputReference",
    "KendraDataSourceCustomDocumentEnrichmentConfiguration",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValueOutputReference",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionOutputReference",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsList",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsOutputReference",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetOutputReference",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValueOutputReference",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationOutputReference",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValueOutputReference",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionOutputReference",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationOutputReference",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValueOutputReference",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionOutputReference",
    "KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationOutputReference",
    "KendraDataSourceTimeouts",
    "KendraDataSourceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b0868e6a50aa75c9778b140853bc37464140b7c943903155cb455d2b5ea814ce(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    index_id: builtins.str,
    name: builtins.str,
    type: builtins.str,
    configuration: typing.Optional[typing.Union[KendraDataSourceConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_document_enrichment_configuration: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    language_code: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[KendraDataSourceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__c4749708cc69fa59aeada6558eae753cf3dba6d6da3084c9737cbc5e44761f7c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80f66c02dcfc71d4b8c6f80c4cbaab7866343e34c08b0b840d0b315202a74380(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b761ff8ce7117e1d9de3724bacca66b365848eb881b71af2e7a695ac7b3537f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f81e628d377c17c3a2a9656f1c6d72c41eaf63d561a6582e9ba12b2f7c1dc66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4991bef97708c5db1f901868d2c34ecdb68a1b3ec3b51f403dc7dcff50173f50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8992e002682220bad2465902f4e9eac3e56e6baff3911a607c467e4519aa049(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b652a40312f570933f456f5fc8e041d7396b917f417cadb37e0c5d4ddcdd77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80cd0b88394d0e4354d318499d5fdca53c7009a9f791a21b61703cf84e1a58c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1ecb4bb26fb4459498261f089a0376cdf1ae51c8ca1e655cc2c68ee10003a9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e32c70600e928e033506f0b19d70dfa4064fee64cf5e321776d93fd3c606cc9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74b25b31608114fdeab498e7f656549c55df80c059e51e86bac586610d3d38bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b50ce043c30ecca7c0443b3b48788fa87b35b794045d0376891068efa8e21e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    index_id: builtins.str,
    name: builtins.str,
    type: builtins.str,
    configuration: typing.Optional[typing.Union[KendraDataSourceConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_document_enrichment_configuration: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    language_code: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[KendraDataSourceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da020ac3544d5069a3d99af94f62ad680776778c483f14ab0b4350e15a32633e(
    *,
    s3_configuration: typing.Optional[typing.Union[KendraDataSourceConfigurationS3Configuration, typing.Dict[builtins.str, typing.Any]]] = None,
    template_configuration: typing.Optional[typing.Union[KendraDataSourceConfigurationTemplateConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    web_crawler_configuration: typing.Optional[typing.Union[KendraDataSourceConfigurationWebCrawlerConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__241e186b3b8534a7742360c8b9d5ee3df68d0733bd3d1f0fd7fe8c098ce899c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4311bff8737b9d246927116d372c9c7273ff30433533f9094c48e3cfc5fdd1b(
    value: typing.Optional[KendraDataSourceConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14868cd02eeb81315a1452dbb2230f703ffb303beee7f6dea34f0e4950d1bdc9(
    *,
    bucket_name: builtins.str,
    access_control_list_configuration: typing.Optional[typing.Union[KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    documents_metadata_configuration: typing.Optional[typing.Union[KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4979ded08423165f07b4fac0135b7243b37c177ee085c085b0cbd14d951d2a0(
    *,
    key_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__614760797d286f9faca7cd9acb7d05cf7b4848991d4b556e3bb4e5119ec23502(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29b709c0d0e487026f35e83212d211b2fdca801d377ab02c5cced5e43fe205b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdb552a83ea311fd523e3cf949be8368818a8fd77bd4e4588810f5277e10c8ce(
    value: typing.Optional[KendraDataSourceConfigurationS3ConfigurationAccessControlListConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__391b8de9e37dc26f022c7ea29fbc52bb9f49e195921d578c1b7e6ff9808ea721(
    *,
    s3_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b03198f904a9024307998f362df69f4434009d5641d8382f27d987f8dd53739b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d31ce1de2f7b43fc01b41672ea482c3fe109db1b5271d5c85f30dfeb51ee4289(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cfd41d5dcc686a454df4b15410ca222e67060c7314049f2b3ed082581b3d258(
    value: typing.Optional[KendraDataSourceConfigurationS3ConfigurationDocumentsMetadataConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__377447184ec21ba4c210523c0a1c686b7baee7827b6f6dd513568d0e20584417(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3748ea74b6f06b558d82844efa64856e3352faf8e7201a883b7468d523fbf530(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4208575c850a22cca7179f36e0dfad50d2259488e96353c44143df21572a930(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2476be289959f8a90676ab002971f7cc12e682050da4cb6c1c5fa1d762d6c91(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29a81581054c31afa916306202bd11079e87290f5c9173cfb617b524a779f669(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64edd1ec0de6e73858c8cab8afaadd693cd4eb3f3e254d6b31d3700d994a7ac6(
    value: typing.Optional[KendraDataSourceConfigurationS3Configuration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b7392cb25fe33a11273e79f1f32764e66f13ebe2825af22e47ed504c91135f6(
    *,
    template: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e1485943b33a83388e3377e8f5bebd27b914bdf242ca5ae5cca91b82f6823b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6120eb83bd4e82ae0343e27483417fc1bd02af3a8968a7f145105cc7071e77a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d0ab67d7d9922dec19c702d45967324787442e52218144a4d14a0f14d05180f(
    value: typing.Optional[KendraDataSourceConfigurationTemplateConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60573d69b390b309ce053e2c5381898b17a162170e75c93b81af9c47f0d95779(
    *,
    urls: typing.Union[KendraDataSourceConfigurationWebCrawlerConfigurationUrls, typing.Dict[builtins.str, typing.Any]],
    authentication_configuration: typing.Optional[typing.Union[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    crawl_depth: typing.Optional[jsii.Number] = None,
    max_content_size_per_page_in_mega_bytes: typing.Optional[jsii.Number] = None,
    max_links_per_page: typing.Optional[jsii.Number] = None,
    max_urls_per_minute_crawl_rate: typing.Optional[jsii.Number] = None,
    proxy_configuration: typing.Optional[typing.Union[KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    url_exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    url_inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cdf295e3ad7c3a330ba9f26f891c3505ec1471c7e4e86cca952b9b62139c7e1(
    *,
    basic_authentication: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1398dc54280b1c95a6e8534f6a1e890e2a03c2d58eebb25eff2cc8f01c19064a(
    *,
    credentials: builtins.str,
    host: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54bc2073c331179d82ff8254f066936865a5c6503a3b4e015ba543917edb1510(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1be841a7113343c1dc224bcbb70b3c48b21bd72107faa7f5da6cd317b178e59b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b245d76c9b5a20c8f84e2c058e97e2eb6fe510e7988a5ef34596e5bf72942a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0225f44047e80c74f74cee2d5813845614bcbf25e9641188cee7776cc3f2992b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a08ff2eb5147a6b8e5e41eccdda4c785122f25e6d9ccb9db90e37993328885a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d75b13e7369f97184d61f5f4e5c878d0f69c4621638235322b69649b96392b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68a7f0e8eb461f2d4d43a3a0d23ebef4d5779c74c0951eb1e4326c10482f66ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a23ec6693b16cacfe1f8fc9b23cf62a1e048e6c2bc0bbc565444e9c49e79ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f99e84855aadcb0a2a678ff890fc5aff76168dc8b73ac5543bac46c01ac0b39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a753f8f61edf17d4ad1445d90994cb6ba1c1a4caf99221acffbbe7512ea5e168(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f24385f654eb14b3622585bb6f2c1e0094840a0b336d61bd1c6eb7979825a54(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f0e9dcf376a03d6b5a400fb936843cab19c41b314b5c4bd0db2d2be42f8ba2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d09a3dbd00798bcdaca270bce551560167a37c668476118d8c4d1c29d866e990(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfigurationBasicAuthentication, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50429eb6ab7f266d71186b3b52970fa9485a738e9b1b77642ead041a6e8de2f0(
    value: typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationAuthenticationConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a61d658d7133ecff148c87596b592a3e18891a4edd6aad3e509ff4c3b015f711(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57f4e8d67769d76d4ed7982a2acfad07816f2c1f9b00cdf73c9dbd93f7a623dc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6308e23cd8e38f39fb8e77c6cb9850012d2117f20aef9af8d8003bad87e1db34(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e570ab658e36943958dff243114b1f1f1289546a6d7bf3bd7b768545134acd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__269d6a9db5e94f0cf201c519a1a382a72d7a5654f04f9959c4fa94f518a7ede0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81a75d9a298c98c949fc2b06c55eacf87b27c02874d3bc86ed6e4cd25e1735e8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f02b99ffd03191677673b9de168f353ab9f46abab6519e086c3157b8ae5ee288(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9142aa81645558749e6047e8da3022520259ff1f03e89052f924ed43eff76fd(
    value: typing.Optional[KendraDataSourceConfigurationWebCrawlerConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4a28e475cf043a03e2d33cba36540d1f8de1178d75bb352941bd3f2e414c909(
    *,
    host: builtins.str,
    port: jsii.Number,
    credentials: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd7a20aca04a6cf35ae07cb7a733fa0c2e8da98d9b385f2e3cdb5a5a87913572(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abbb9570a7a9bec4e4be06fc7d1b9974d7644f6d604755319fcbd78beb43a1e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13a4d8c6678dd75c09c571a17a04672f88a1ddc154a5801e8bc993fe6c761f97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f895b4b604f4034ea64cb7ffe273dc2f28fa6754b4638ef9a116b8f5365e8a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19fef78fe0f7e00e7d2978dd0b3491ac20affb4822cf9a129659e658eaeaea52(
    value: typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationProxyConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd08ac2965ef9f7f37ba19435c8be680af2c623a53f74c5549118cabd141027(
    *,
    seed_url_configuration: typing.Optional[typing.Union[KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    site_maps_configuration: typing.Optional[typing.Union[KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__591c8142ace51bd2cd827ce8eba949fdc7446689877a7a0ef9fe77d87f612e0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__604dd32932f83c6df950becd92e8c040aaa63e5cd059624881cc8d2410a61e7f(
    value: typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationUrls],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__accf063ff811c335d20239a62d744fd1663a7c842370738df337a915011f0df8(
    *,
    seed_urls: typing.Sequence[builtins.str],
    web_crawler_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0748d1756046567bb4301c67b7dd0f85ea6a6a8df952eb20b35e2482f4df633b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d30dcbce06d9b557fb40c070e29efe9a716377cd8d3d717e7b82eb940c5740(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2006be9ee78b5a0d7518e1cf0bbae16b4a618ffeb0b08566539f0dec630cef52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c46f0dd39363df727e7de08127a0797a6abbdd0e54f01c73afde2415bd1f5d(
    value: typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSeedUrlConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a500df945e9ea3034a7dc1431d8160c06032e9aef4e5a4c5dd7e0a50a7e2ff89(
    *,
    site_maps: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d9cc6d5898ee4680653c15e4bf70c6aa947a64f8fd22043504deceaf043e3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a15cafefe5ce00a160f850f2d6f0dd6199435f4b99bfb6cd7b3228212d17f3b1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff8ddbfdd5e92ddab2e6a203c6fce6c12cfad3e2f97925eeeba274899deae33e(
    value: typing.Optional[KendraDataSourceConfigurationWebCrawlerConfigurationUrlsSiteMapsConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca97bec22f615c8851dc2bb26dcc3bd38a2f395498ca54c8ffa8432626aed21a(
    *,
    inline_configurations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    post_extraction_hook_configuration: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    pre_extraction_hook_configuration: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a95729cc2ec5d41e4e1857db8756e206e2e802751db594b5a77399ce38b2c5a8(
    *,
    condition: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    document_content_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    target: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3829374b8ce0393bbd420a21184976a5aef23cbf5819d8bd4f37817f007bc06(
    *,
    condition_document_attribute_key: builtins.str,
    operator: builtins.str,
    condition_on_value: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07027ac4ece4958e53744a46668d1f8589ec79f6b3cbec9c62db33e106747364(
    *,
    date_value: typing.Optional[builtins.str] = None,
    long_value: typing.Optional[jsii.Number] = None,
    string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32c3a16499c749976a3c970cd84191d0c47e74e39e08e3d4aad9f11128317c08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b43185c02eee2c270d9050438c4a04a3d5fb1a6a3cb2e1dbdbb48851c1457a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5caab1d316ffb51f3b191bd02782ea3f86333b861caadd929c64ef20d9d61bf3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0bc749ab4476020a1bbf92c6c53ff2d76de2758d5683b849c8b860d20763638(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9481895c630c1838730b876c693e8728741a36dd14a922087a6a0aff03ce0ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ffbd3c92f052b1c97149e454399d5e203d4e9143e963f3ff25060067556c68d(
    value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsConditionConditionOnValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d376dcdaa1fda0b81d1e2938e6d6a13b816ffddb66e4c0be91448147adee5a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b97e1e6b0d8e912b7abd950a305103e12b879bb9c005740733d0ecb48737693a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37dabbca442d639199b2e8fc1a4ec063a755135b643f70afe24964f9ab6a97a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6ef84b06640a7b4d4d4354110551a93af8f91ee6ed364d6b438305d221a87f1(
    value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62ce4fcba6f3b65a6d7c888a33b50d7b5d89b9c9f55e07df099134e07965c80f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc4c0f438f60a7692ada22aa2f2dfea1bd2a05418e2e3fa03ff21f8788bde257(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ead77504dd915ff185a6693c7cc4b3a974d145e5bb207cc182289a3f3fdf37c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8697fc92b4b57127b21d0dcc59cda22635a00de1f0bbf84efeeed15ee2a98c91(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db7f778b4664185b5344b58bbd71bdc1103d92949e68b097839ae112e4f300ed(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6773ce6083d041fb4e0d092f62c647da5a8819a69112db078ea35032e1f865a8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eccea1901fe88bb81f2926318595973aa3372f37382878c287432e2189ca8e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9559f8c6023d0d540fb8ff9136a01435483bf57c59f81b42ff15c0ec7eeec9c0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d7e5a5a5a91cda7468af4e05e788e2a1c9f4a0dd7c79f0d07c02aee1f733ae5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0f9dce499602eb3af9747d2d01d402af538613c4c45f8c1b674f6a31536edc4(
    *,
    target_document_attribute_key: typing.Optional[builtins.str] = None,
    target_document_attribute_value: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue, typing.Dict[builtins.str, typing.Any]]] = None,
    target_document_attribute_value_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9059dd09ca5886c5d4e7a88080c5c143812c59e96900d60e50c7da9b16683d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6c4f1bd94c16f4a021d2794f51781621d806b763c9376d6639413463b1a2e20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f448e920fa38a5c782add36e994cfe1ca03aa7509d9dfd563f2a62e3a670b753(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__499a27499462ffc1aecf625a245e6986d80a934ad6734e8c3c30876b49451412(
    value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTarget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b1897d9891cc52661cfb8f7bfc9e032d6ff9f2ada84bfd6e2b4b52230231c85(
    *,
    date_value: typing.Optional[builtins.str] = None,
    long_value: typing.Optional[jsii.Number] = None,
    string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd602ea82cd1d86d12ba2a8db4c6d7d0cab9e5eeecf4d4483efd2cb2d41c3f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94db43b9d120ecfb737dbc7bb9b361187a4d89b205768dcc5668dfef2e183ab6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__961820718d05159d6de76e0e675996ecdd934cc1cb7e1859ccb06a2d4f0bd6de(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__609244fd1e0902a25693abdf631c48dd379690d00333e1a6049cf6ea70efbe95(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12aa2867569aaa621a6eceb583bce5e4b11706dca451cf7fe02ec199cf595c0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63272bba77c2399c30ca0797f261b180f8f5ff4b63d27c42723b38251eb4ac90(
    value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurationsTargetTargetDocumentAttributeValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a802050aed6aeafefd1e402f82734347f9b5bb1b372cbf1215085a396ebd3c8a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a37349163957e804cc865e3958ab39315f6dc2cd89bc17fc59dddaaa0b3bc91(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationInlineConfigurations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4a7160ddd8a64807b4613808e336c5c45adcbbbf023415d94307b571b286635(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d5af5b193e153e889d72671843793ce8717e70df16f560dd4382184921cb4eb(
    value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94b89b3e90ceb94180a2a331c1c9b1e2a61b52f296281784db648c68abb3445f(
    *,
    lambda_arn: builtins.str,
    s3_bucket: builtins.str,
    invocation_condition: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b5a9981acd65c6dc1b84655118ead31177df4ece8470339b4fceea51e65c293(
    *,
    condition_document_attribute_key: builtins.str,
    operator: builtins.str,
    condition_on_value: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96ad55b3fc3c1bad9b2741d437121c3836eada48fe3b306866a638f5d5086ffb(
    *,
    date_value: typing.Optional[builtins.str] = None,
    long_value: typing.Optional[jsii.Number] = None,
    string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__832828cd21387267f12ea438a81001f49c3e0b9d6ad47e0d61e3f7f852f5b71f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81cc0d9afefeeb974034a808f0f7e0f2e76f34dcebe15cc932a7f214d02b75bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__974ca8d0746360a5d887bd5aa09e9b3220a4062b82c5b2882cb5162fa25a8b51(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70bd634b2eb8a136eb5f3856de5bdf40647f985d531d7875383304db4c99c13f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6ed5c29c52116abd48d9dcb042f2bd9b05e0a9a0b29da5b2fc33d4983d88fd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f17316d16d60d268e16f4e3e6ba363b06c94bb2e8aa5b6b11ed62be19556afe5(
    value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationConditionConditionOnValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce1a342928eb8a24eaf5dec29a1c6af5fa786dd2e1abb62264504d7d656c239(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88c462c9f48b4bd7a474fc8c926774d059e4f72abe3c1e72e1d2709749670dd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdaff859224c84d28d1ee7007262267342b0de2ac4aae102e49cfa00e6a7d291(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e090a450fe64ee80ce48bca0f61cd48f9aa25d3491222d437b79aba3c1b9d4be(
    value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfigurationInvocationCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d168492dde03cc50529fba526af4bb62bba774b1fb2bbf0014c01e4fbe8a9dac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a04e3ef5c8f29a1c08000526a9059441488d86d3b69a20d2e830ad7375b7d89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae18ef77df3de5e2a3216608526abc823735a9b75258b5f6314d728de394c6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00aa594a06accab7ba2b4d8e645a0efc1e6339cdb2eb442b6efb5400d7cde67a(
    value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPostExtractionHookConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__178d7e6a98768f110ea4414beda653e370d56d4140317f4ee480f7aaf6789b41(
    *,
    lambda_arn: builtins.str,
    s3_bucket: builtins.str,
    invocation_condition: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b3874df348a22f8929fb36b2faa29f11ccb2e82468dafddc260e4c428be9b35(
    *,
    condition_document_attribute_key: builtins.str,
    operator: builtins.str,
    condition_on_value: typing.Optional[typing.Union[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__524e7a2c82f3f35218252ed7acd6ab0aa9f0b23fa3904aabe3de0b3331b69da3(
    *,
    date_value: typing.Optional[builtins.str] = None,
    long_value: typing.Optional[jsii.Number] = None,
    string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2188dc13b1baec7a6aa98906d33213575bd7d0aee0bb3ad37568660a66af9f6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__852d620babb0ce2583e05ab48cfb58c914b4af85e42ff82927654f209195e866(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef557f9db711ff2a4a8a0d3bd98c4b43663aa794bbe9ec3b4f724c1b2cebec95(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc73cc19b7c62562e8e196c4029f5f2cbbec4bbfa2da877bab1ba2ca933c60c6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b126cc463e07358057b03a5bd18e487b5393eedf179b1e68c2af51b61bfd8cc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb2733173cf0eaaefed2c2efdb5fff2d62aa0e33a0e3efa822da66001d80e9ae(
    value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationConditionConditionOnValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9965291a14dba086ff95092922b63149ce216d3532330731a15909547c8d83fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ccdbfff19750f7d012badef459553b49f7727b9debbfd8b0d52b095c962dd07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e9a77259e9d3466a447dac969b75ab43e8eaeed4ab6a3b674482c03802eb5e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f71db1f095b69d79eb0d583f3702c7a34afb58f3cad479bcee6a5cf3b844528d(
    value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfigurationInvocationCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abfa26f23ea67de8b0dfd14917417587dac412b9a3dc98d98f14a9a45273d1fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a5e02f9302a87a1f70a2ed5a4290a7574d49fa53091aae75754f9af32a001f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3590cdfe59554980c8d5ea46cd6a0b87a18605a51d835d963822e3f3fbd1b4fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514f3099e796533d16ad0dfc0ee4db483e15f91399c5ba823baea9fd8bdbf61a(
    value: typing.Optional[KendraDataSourceCustomDocumentEnrichmentConfigurationPreExtractionHookConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8bd7541e9304f7d416691eb47d2f0d2c4b06fc1df05b867d39365237770ec34(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__542e068156577db182bfbb1e0ed8b03f86e84d766ae6bdd34324f92d2d5f8ef9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363a385c01f1683594af0485f0e45470276ab2e7814b3a8b5561d56492af9b29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fea4083afb56345c4ff2372e43270f8bbb23362d1f60f64f36c3310223196b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14b93990fda9a57b9563dfcd3e98f71ab3f51ef7b8d0d8891024b98cee5607df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__704bca85e887be69b0770d3bd47d457ebd287338107cf040782e208af6f4d989(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KendraDataSourceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
