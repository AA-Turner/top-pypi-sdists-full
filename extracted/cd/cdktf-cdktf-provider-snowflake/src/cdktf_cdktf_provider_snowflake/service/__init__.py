r'''
# `snowflake_service`

Refer to the Terraform Registry for docs: [`snowflake_service`](https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service).
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


class Service(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.service.Service",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service snowflake_service}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        compute_pool: builtins.str,
        database: builtins.str,
        name: builtins.str,
        schema: builtins.str,
        auto_resume: typing.Optional[builtins.str] = None,
        auto_suspend_secs: typing.Optional[jsii.Number] = None,
        comment: typing.Optional[builtins.str] = None,
        external_access_integrations: typing.Optional[typing.Sequence[builtins.str]] = None,
        from_specification: typing.Optional[typing.Union["ServiceFromSpecification", typing.Dict[builtins.str, typing.Any]]] = None,
        from_specification_template: typing.Optional[typing.Union["ServiceFromSpecificationTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        max_instances: typing.Optional[jsii.Number] = None,
        min_instances: typing.Optional[jsii.Number] = None,
        min_ready_instances: typing.Optional[jsii.Number] = None,
        query_warehouse: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service snowflake_service} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param compute_pool: Specifies the name of the compute pool in your account on which to run the service. Identifiers with special or lower-case characters are not supported. This limitation in the provider follows the limitation in Snowflake (see `docs <https://docs.snowflake.com/en/sql-reference/sql/create-compute-pool>`_). Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#compute_pool Service#compute_pool}
        :param database: The database in which to create the service. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#database Service#database}
        :param name: Specifies the identifier for the service; must be unique for the schema in which the service is created. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#name Service#name}
        :param schema: The schema in which to create the service. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#schema Service#schema}
        :param auto_resume: (Default: fallback to Snowflake default - uses special value that cannot be set in the configuration manually (``default``)) Specifies whether to automatically resume a service. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#auto_resume Service#auto_resume}
        :param auto_suspend_secs: (Default: fallback to Snowflake default - uses special value that cannot be set in the configuration manually (``-1``)) Specifies the number of seconds of inactivity (service is idle) after which Snowflake automatically suspends the service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#auto_suspend_secs Service#auto_suspend_secs}
        :param comment: Specifies a comment for the service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#comment Service#comment}
        :param external_access_integrations: Specifies the names of the external access integrations that allow your service to access external sites. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#external_access_integrations Service#external_access_integrations}
        :param from_specification: from_specification block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#from_specification Service#from_specification}
        :param from_specification_template: from_specification_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#from_specification_template Service#from_specification_template}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#id Service#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_instances: Specifies the maximum number of service instances to run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#max_instances Service#max_instances}
        :param min_instances: Specifies the minimum number of service instances to run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#min_instances Service#min_instances}
        :param min_ready_instances: Indicates the minimum service instances that must be ready for Snowflake to consider the service is ready to process requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#min_ready_instances Service#min_ready_instances}
        :param query_warehouse: Warehouse to use if a service container connects to Snowflake to execute a query but does not explicitly specify a warehouse to use. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#query_warehouse Service#query_warehouse}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#timeouts Service#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0fcd171ed9fea040e48b958e427a617f7126c5cf53a6d7b698416da385f5ae9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ServiceConfig(
            compute_pool=compute_pool,
            database=database,
            name=name,
            schema=schema,
            auto_resume=auto_resume,
            auto_suspend_secs=auto_suspend_secs,
            comment=comment,
            external_access_integrations=external_access_integrations,
            from_specification=from_specification,
            from_specification_template=from_specification_template,
            id=id,
            max_instances=max_instances,
            min_instances=min_instances,
            min_ready_instances=min_ready_instances,
            query_warehouse=query_warehouse,
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
        '''Generates CDKTF code for importing a Service resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Service to import.
        :param import_from_id: The id of the existing Service that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Service to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9de553d7c8aca83290d9073d0dfc6dcec6a6b00e4177269840d4eceeee64cd4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFromSpecification")
    def put_from_specification(
        self,
        *,
        file: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        stage: typing.Optional[builtins.str] = None,
        text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file: The file name of the service specification. Example: ``spec.yaml``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#file Service#file}
        :param path: The path to the service specification file on the given stage. When the path is specified, the ``/`` character is automatically added as a path prefix. Example: ``path/to/spec``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#path Service#path}
        :param stage: The fully qualified name of the stage containing the service specification file. At symbol (``@``) is added automatically. Example: ``"\\"<db_name>\\".\\"<schema_name>\\".\\"<stage_name>\\""``. For more information about this resource, see `docs <./stage>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#stage Service#stage}
        :param text: The embedded text of the service specification. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#text Service#text}
        '''
        value = ServiceFromSpecification(file=file, path=path, stage=stage, text=text)

        return typing.cast(None, jsii.invoke(self, "putFromSpecification", [value]))

    @jsii.member(jsii_name="putFromSpecificationTemplate")
    def put_from_specification_template(
        self,
        *,
        using: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFromSpecificationTemplateUsing", typing.Dict[builtins.str, typing.Any]]]],
        file: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        stage: typing.Optional[builtins.str] = None,
        text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param using: using block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#using Service#using}
        :param file: The file name of the service specification template. Example: ``spec.yaml``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#file Service#file}
        :param path: The path to the service specification template file on the given stage. When the path is specified, the ``/`` character is automatically added as a path prefix. Example: ``path/to/spec``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#path Service#path}
        :param stage: The fully qualified name of the stage containing the service specification template file. At symbol (``@``) is added automatically. Example: ``"\\"<db_name>\\".\\"<schema_name>\\".\\"<stage_name>\\""``. For more information about this resource, see `docs <./stage>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#stage Service#stage}
        :param text: The embedded text of the service specification template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#text Service#text}
        '''
        value = ServiceFromSpecificationTemplate(
            using=using, file=file, path=path, stage=stage, text=text
        )

        return typing.cast(None, jsii.invoke(self, "putFromSpecificationTemplate", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#create Service#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#delete Service#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#read Service#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#update Service#update}.
        '''
        value = ServiceTimeouts(create=create, delete=delete, read=read, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAutoResume")
    def reset_auto_resume(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoResume", []))

    @jsii.member(jsii_name="resetAutoSuspendSecs")
    def reset_auto_suspend_secs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoSuspendSecs", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetExternalAccessIntegrations")
    def reset_external_access_integrations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalAccessIntegrations", []))

    @jsii.member(jsii_name="resetFromSpecification")
    def reset_from_specification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFromSpecification", []))

    @jsii.member(jsii_name="resetFromSpecificationTemplate")
    def reset_from_specification_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFromSpecificationTemplate", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaxInstances")
    def reset_max_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxInstances", []))

    @jsii.member(jsii_name="resetMinInstances")
    def reset_min_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinInstances", []))

    @jsii.member(jsii_name="resetMinReadyInstances")
    def reset_min_ready_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinReadyInstances", []))

    @jsii.member(jsii_name="resetQueryWarehouse")
    def reset_query_warehouse(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryWarehouse", []))

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
    @jsii.member(jsii_name="describeOutput")
    def describe_output(self) -> "ServiceDescribeOutputList":
        return typing.cast("ServiceDescribeOutputList", jsii.get(self, "describeOutput"))

    @builtins.property
    @jsii.member(jsii_name="fromSpecification")
    def from_specification(self) -> "ServiceFromSpecificationOutputReference":
        return typing.cast("ServiceFromSpecificationOutputReference", jsii.get(self, "fromSpecification"))

    @builtins.property
    @jsii.member(jsii_name="fromSpecificationTemplate")
    def from_specification_template(
        self,
    ) -> "ServiceFromSpecificationTemplateOutputReference":
        return typing.cast("ServiceFromSpecificationTemplateOutputReference", jsii.get(self, "fromSpecificationTemplate"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="serviceType")
    def service_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceType"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(self) -> "ServiceShowOutputList":
        return typing.cast("ServiceShowOutputList", jsii.get(self, "showOutput"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ServiceTimeoutsOutputReference":
        return typing.cast("ServiceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="autoResumeInput")
    def auto_resume_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoResumeInput"))

    @builtins.property
    @jsii.member(jsii_name="autoSuspendSecsInput")
    def auto_suspend_secs_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "autoSuspendSecsInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="computePoolInput")
    def compute_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computePoolInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="externalAccessIntegrationsInput")
    def external_access_integrations_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalAccessIntegrationsInput"))

    @builtins.property
    @jsii.member(jsii_name="fromSpecificationInput")
    def from_specification_input(self) -> typing.Optional["ServiceFromSpecification"]:
        return typing.cast(typing.Optional["ServiceFromSpecification"], jsii.get(self, "fromSpecificationInput"))

    @builtins.property
    @jsii.member(jsii_name="fromSpecificationTemplateInput")
    def from_specification_template_input(
        self,
    ) -> typing.Optional["ServiceFromSpecificationTemplate"]:
        return typing.cast(typing.Optional["ServiceFromSpecificationTemplate"], jsii.get(self, "fromSpecificationTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="maxInstancesInput")
    def max_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="minInstancesInput")
    def min_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="minReadyInstancesInput")
    def min_ready_instances_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minReadyInstancesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="queryWarehouseInput")
    def query_warehouse_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryWarehouseInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ServiceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ServiceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoResume")
    def auto_resume(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoResume"))

    @auto_resume.setter
    def auto_resume(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d263acd4b4ea426b784a6bdf6e1d4018322246b35478eeb738e69af2492a0bd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoResume", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoSuspendSecs")
    def auto_suspend_secs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "autoSuspendSecs"))

    @auto_suspend_secs.setter
    def auto_suspend_secs(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__450cf3e6b2ff5446085c39b2154ac5bd4f6ca62df51e39b8ebb5ff6464a1febe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoSuspendSecs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b72e9800dd0627e0116ca10d645c7f170826229c7e13950b7b73b16b7803aa26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="computePool")
    def compute_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "computePool"))

    @compute_pool.setter
    def compute_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17b6acfd4021f68f41835bf8c4a7204163616d8c57155bce1309b50a33538de0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computePool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93f15a05b6ffcadf7857b8caf91b24c78963e21d8384b10f89b5d8871d50f121)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalAccessIntegrations")
    def external_access_integrations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalAccessIntegrations"))

    @external_access_integrations.setter
    def external_access_integrations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7243b722e1d3b4eaef005697d60a303456c3c26cb5bc76aecc88cde1cd0ef283)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalAccessIntegrations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c08abe1cbc50c8a99c9278c400237e593b84f058f4875ebb0390df1825c8725)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxInstances")
    def max_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstances"))

    @max_instances.setter
    def max_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8caa250ebf5ffed3285247b3215a3c202941cdf7a0ff2718171acf5c8baf68da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minInstances")
    def min_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minInstances"))

    @min_instances.setter
    def min_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1d23aa2480cb2205ccf77896ada60cf36650da58fca7894bb8073a0f1416e97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minReadyInstances")
    def min_ready_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minReadyInstances"))

    @min_ready_instances.setter
    def min_ready_instances(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5343f4812b1716fde789cf39878014fda1bed9fe279eb3785e971dcbae9cb214)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minReadyInstances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c07ce04bb873d4b5aea44c62fbea67f165c2a06d2c498df401f012fcf238946)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryWarehouse")
    def query_warehouse(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryWarehouse"))

    @query_warehouse.setter
    def query_warehouse(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f8476c3051cb7824803c3669fc73f9140ef2fa7e87684eb48c1539cbe9d6630)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryWarehouse", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b04c88dbc1c8e82503fda700514dd813460428a4f8c2c951495f85de5e5ef20b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.service.ServiceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "compute_pool": "computePool",
        "database": "database",
        "name": "name",
        "schema": "schema",
        "auto_resume": "autoResume",
        "auto_suspend_secs": "autoSuspendSecs",
        "comment": "comment",
        "external_access_integrations": "externalAccessIntegrations",
        "from_specification": "fromSpecification",
        "from_specification_template": "fromSpecificationTemplate",
        "id": "id",
        "max_instances": "maxInstances",
        "min_instances": "minInstances",
        "min_ready_instances": "minReadyInstances",
        "query_warehouse": "queryWarehouse",
        "timeouts": "timeouts",
    },
)
class ServiceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        compute_pool: builtins.str,
        database: builtins.str,
        name: builtins.str,
        schema: builtins.str,
        auto_resume: typing.Optional[builtins.str] = None,
        auto_suspend_secs: typing.Optional[jsii.Number] = None,
        comment: typing.Optional[builtins.str] = None,
        external_access_integrations: typing.Optional[typing.Sequence[builtins.str]] = None,
        from_specification: typing.Optional[typing.Union["ServiceFromSpecification", typing.Dict[builtins.str, typing.Any]]] = None,
        from_specification_template: typing.Optional[typing.Union["ServiceFromSpecificationTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        max_instances: typing.Optional[jsii.Number] = None,
        min_instances: typing.Optional[jsii.Number] = None,
        min_ready_instances: typing.Optional[jsii.Number] = None,
        query_warehouse: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param compute_pool: Specifies the name of the compute pool in your account on which to run the service. Identifiers with special or lower-case characters are not supported. This limitation in the provider follows the limitation in Snowflake (see `docs <https://docs.snowflake.com/en/sql-reference/sql/create-compute-pool>`_). Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#compute_pool Service#compute_pool}
        :param database: The database in which to create the service. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#database Service#database}
        :param name: Specifies the identifier for the service; must be unique for the schema in which the service is created. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#name Service#name}
        :param schema: The schema in which to create the service. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#schema Service#schema}
        :param auto_resume: (Default: fallback to Snowflake default - uses special value that cannot be set in the configuration manually (``default``)) Specifies whether to automatically resume a service. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#auto_resume Service#auto_resume}
        :param auto_suspend_secs: (Default: fallback to Snowflake default - uses special value that cannot be set in the configuration manually (``-1``)) Specifies the number of seconds of inactivity (service is idle) after which Snowflake automatically suspends the service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#auto_suspend_secs Service#auto_suspend_secs}
        :param comment: Specifies a comment for the service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#comment Service#comment}
        :param external_access_integrations: Specifies the names of the external access integrations that allow your service to access external sites. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#external_access_integrations Service#external_access_integrations}
        :param from_specification: from_specification block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#from_specification Service#from_specification}
        :param from_specification_template: from_specification_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#from_specification_template Service#from_specification_template}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#id Service#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_instances: Specifies the maximum number of service instances to run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#max_instances Service#max_instances}
        :param min_instances: Specifies the minimum number of service instances to run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#min_instances Service#min_instances}
        :param min_ready_instances: Indicates the minimum service instances that must be ready for Snowflake to consider the service is ready to process requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#min_ready_instances Service#min_ready_instances}
        :param query_warehouse: Warehouse to use if a service container connects to Snowflake to execute a query but does not explicitly specify a warehouse to use. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#query_warehouse Service#query_warehouse}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#timeouts Service#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(from_specification, dict):
            from_specification = ServiceFromSpecification(**from_specification)
        if isinstance(from_specification_template, dict):
            from_specification_template = ServiceFromSpecificationTemplate(**from_specification_template)
        if isinstance(timeouts, dict):
            timeouts = ServiceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d46e53bbe6a0aff9af3c71b7b4cb56953271598fd0f516a29c41298e536688f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument compute_pool", value=compute_pool, expected_type=type_hints["compute_pool"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument auto_resume", value=auto_resume, expected_type=type_hints["auto_resume"])
            check_type(argname="argument auto_suspend_secs", value=auto_suspend_secs, expected_type=type_hints["auto_suspend_secs"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument external_access_integrations", value=external_access_integrations, expected_type=type_hints["external_access_integrations"])
            check_type(argname="argument from_specification", value=from_specification, expected_type=type_hints["from_specification"])
            check_type(argname="argument from_specification_template", value=from_specification_template, expected_type=type_hints["from_specification_template"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument max_instances", value=max_instances, expected_type=type_hints["max_instances"])
            check_type(argname="argument min_instances", value=min_instances, expected_type=type_hints["min_instances"])
            check_type(argname="argument min_ready_instances", value=min_ready_instances, expected_type=type_hints["min_ready_instances"])
            check_type(argname="argument query_warehouse", value=query_warehouse, expected_type=type_hints["query_warehouse"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "compute_pool": compute_pool,
            "database": database,
            "name": name,
            "schema": schema,
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
        if auto_resume is not None:
            self._values["auto_resume"] = auto_resume
        if auto_suspend_secs is not None:
            self._values["auto_suspend_secs"] = auto_suspend_secs
        if comment is not None:
            self._values["comment"] = comment
        if external_access_integrations is not None:
            self._values["external_access_integrations"] = external_access_integrations
        if from_specification is not None:
            self._values["from_specification"] = from_specification
        if from_specification_template is not None:
            self._values["from_specification_template"] = from_specification_template
        if id is not None:
            self._values["id"] = id
        if max_instances is not None:
            self._values["max_instances"] = max_instances
        if min_instances is not None:
            self._values["min_instances"] = min_instances
        if min_ready_instances is not None:
            self._values["min_ready_instances"] = min_ready_instances
        if query_warehouse is not None:
            self._values["query_warehouse"] = query_warehouse
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
    def compute_pool(self) -> builtins.str:
        '''Specifies the name of the compute pool in your account on which to run the service.

        Identifiers with special or lower-case characters are not supported. This limitation in the provider follows the limitation in Snowflake (see `docs <https://docs.snowflake.com/en/sql-reference/sql/create-compute-pool>`_). Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#compute_pool Service#compute_pool}
        '''
        result = self._values.get("compute_pool")
        assert result is not None, "Required property 'compute_pool' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database(self) -> builtins.str:
        '''The database in which to create the service.

        Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#database Service#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the identifier for the service;

        must be unique for the schema in which the service is created. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#name Service#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema(self) -> builtins.str:
        '''The schema in which to create the service.

        Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#schema Service#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_resume(self) -> typing.Optional[builtins.str]:
        '''(Default: fallback to Snowflake default - uses special value that cannot be set in the configuration manually (``default``)) Specifies whether to automatically resume a service.

        Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#auto_resume Service#auto_resume}
        '''
        result = self._values.get("auto_resume")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_suspend_secs(self) -> typing.Optional[jsii.Number]:
        '''(Default: fallback to Snowflake default - uses special value that cannot be set in the configuration manually (``-1``)) Specifies the number of seconds of inactivity (service is idle) after which Snowflake automatically suspends the service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#auto_suspend_secs Service#auto_suspend_secs}
        '''
        result = self._values.get("auto_suspend_secs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#comment Service#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_access_integrations(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the names of the external access integrations that allow your service to access external sites.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#external_access_integrations Service#external_access_integrations}
        '''
        result = self._values.get("external_access_integrations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def from_specification(self) -> typing.Optional["ServiceFromSpecification"]:
        '''from_specification block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#from_specification Service#from_specification}
        '''
        result = self._values.get("from_specification")
        return typing.cast(typing.Optional["ServiceFromSpecification"], result)

    @builtins.property
    def from_specification_template(
        self,
    ) -> typing.Optional["ServiceFromSpecificationTemplate"]:
        '''from_specification_template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#from_specification_template Service#from_specification_template}
        '''
        result = self._values.get("from_specification_template")
        return typing.cast(typing.Optional["ServiceFromSpecificationTemplate"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#id Service#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_instances(self) -> typing.Optional[jsii.Number]:
        '''Specifies the maximum number of service instances to run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#max_instances Service#max_instances}
        '''
        result = self._values.get("max_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_instances(self) -> typing.Optional[jsii.Number]:
        '''Specifies the minimum number of service instances to run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#min_instances Service#min_instances}
        '''
        result = self._values.get("min_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_ready_instances(self) -> typing.Optional[jsii.Number]:
        '''Indicates the minimum service instances that must be ready for Snowflake to consider the service is ready to process requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#min_ready_instances Service#min_ready_instances}
        '''
        result = self._values.get("min_ready_instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def query_warehouse(self) -> typing.Optional[builtins.str]:
        '''Warehouse to use if a service container connects to Snowflake to execute a query but does not explicitly specify a warehouse to use.

        Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#query_warehouse Service#query_warehouse}
        '''
        result = self._values.get("query_warehouse")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ServiceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#timeouts Service#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ServiceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.service.ServiceDescribeOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceDescribeOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceDescribeOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceDescribeOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.service.ServiceDescribeOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac1510b5763dbe9ffd148b232e3d3078ac8a6c06cd645236ff223aa85c4b100f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServiceDescribeOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2ec85eacd9f6f6b4d254854399f2d486d8b45ed20ba508edba3c13edd56fa4b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceDescribeOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d5c73fbc544a3a85a248360133784e9d97899fc075ad03a55f6bf5d19bc95f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31e4c2e4f16335b3911d9de15c6394d55a596a5c6f78578425b3e03a6910e241)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a7fd6f6a9cfcf98302139e16604d7c1bbd51ee0f0a0b4a2c3bc2eaacaa161a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceDescribeOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.service.ServiceDescribeOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d283526113d8152527306ab18928e33e5183abda4f6d9df30ba9ceea377e683)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="autoResume")
    def auto_resume(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "autoResume"))

    @builtins.property
    @jsii.member(jsii_name="autoSuspendSecs")
    def auto_suspend_secs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "autoSuspendSecs"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @builtins.property
    @jsii.member(jsii_name="computePool")
    def compute_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "computePool"))

    @builtins.property
    @jsii.member(jsii_name="createdOn")
    def created_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdOn"))

    @builtins.property
    @jsii.member(jsii_name="currentInstances")
    def current_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "currentInstances"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @builtins.property
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsName"))

    @builtins.property
    @jsii.member(jsii_name="externalAccessIntegrations")
    def external_access_integrations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalAccessIntegrations"))

    @builtins.property
    @jsii.member(jsii_name="isAsyncJob")
    def is_async_job(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isAsyncJob"))

    @builtins.property
    @jsii.member(jsii_name="isJob")
    def is_job(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isJob"))

    @builtins.property
    @jsii.member(jsii_name="isUpgrading")
    def is_upgrading(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isUpgrading"))

    @builtins.property
    @jsii.member(jsii_name="managingObjectDomain")
    def managing_object_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managingObjectDomain"))

    @builtins.property
    @jsii.member(jsii_name="managingObjectName")
    def managing_object_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managingObjectName"))

    @builtins.property
    @jsii.member(jsii_name="maxInstances")
    def max_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstances"))

    @builtins.property
    @jsii.member(jsii_name="minInstances")
    def min_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minInstances"))

    @builtins.property
    @jsii.member(jsii_name="minReadyInstances")
    def min_ready_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minReadyInstances"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @builtins.property
    @jsii.member(jsii_name="ownerRoleType")
    def owner_role_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ownerRoleType"))

    @builtins.property
    @jsii.member(jsii_name="queryWarehouse")
    def query_warehouse(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryWarehouse"))

    @builtins.property
    @jsii.member(jsii_name="resumedOn")
    def resumed_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resumedOn"))

    @builtins.property
    @jsii.member(jsii_name="schemaName")
    def schema_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaName"))

    @builtins.property
    @jsii.member(jsii_name="spec")
    def spec(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "spec"))

    @builtins.property
    @jsii.member(jsii_name="specDigest")
    def spec_digest(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "specDigest"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="suspendedOn")
    def suspended_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suspendedOn"))

    @builtins.property
    @jsii.member(jsii_name="targetInstances")
    def target_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetInstances"))

    @builtins.property
    @jsii.member(jsii_name="updatedOn")
    def updated_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedOn"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceDescribeOutput]:
        return typing.cast(typing.Optional[ServiceDescribeOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceDescribeOutput]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__269dcd001f411762ee5a648ece109908651f28f9fbd7f599b342ac39d3710f2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.service.ServiceFromSpecification",
    jsii_struct_bases=[],
    name_mapping={"file": "file", "path": "path", "stage": "stage", "text": "text"},
)
class ServiceFromSpecification:
    def __init__(
        self,
        *,
        file: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        stage: typing.Optional[builtins.str] = None,
        text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file: The file name of the service specification. Example: ``spec.yaml``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#file Service#file}
        :param path: The path to the service specification file on the given stage. When the path is specified, the ``/`` character is automatically added as a path prefix. Example: ``path/to/spec``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#path Service#path}
        :param stage: The fully qualified name of the stage containing the service specification file. At symbol (``@``) is added automatically. Example: ``"\\"<db_name>\\".\\"<schema_name>\\".\\"<stage_name>\\""``. For more information about this resource, see `docs <./stage>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#stage Service#stage}
        :param text: The embedded text of the service specification. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#text Service#text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__234162c6912411e3690e01268f7f6720bf8171c3b4f95f0f1193c446172f1316)
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if file is not None:
            self._values["file"] = file
        if path is not None:
            self._values["path"] = path
        if stage is not None:
            self._values["stage"] = stage
        if text is not None:
            self._values["text"] = text

    @builtins.property
    def file(self) -> typing.Optional[builtins.str]:
        '''The file name of the service specification. Example: ``spec.yaml``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#file Service#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path to the service specification file on the given stage.

        When the path is specified, the ``/`` character is automatically added as a path prefix. Example: ``path/to/spec``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#path Service#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        '''The fully qualified name of the stage containing the service specification file.

        At symbol (``@``) is added automatically. Example: ``"\\"<db_name>\\".\\"<schema_name>\\".\\"<stage_name>\\""``. For more information about this resource, see `docs <./stage>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#stage Service#stage}
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def text(self) -> typing.Optional[builtins.str]:
        '''The embedded text of the service specification.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#text Service#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFromSpecification(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceFromSpecificationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.service.ServiceFromSpecificationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81579154861c98e030d0f41f431ad1d4c22e361251bae81d14bf29ec72a70a55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFile")
    def reset_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFile", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetStage")
    def reset_stage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStage", []))

    @jsii.member(jsii_name="resetText")
    def reset_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetText", []))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="stageInput")
    def stage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stageInput"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "file"))

    @file.setter
    def file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c77fcf5e92eb6b86364e47f5697e128cc03e00ab04ce44e553956151b21ad934)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "file", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eca02107d98a7bb04cbdcab6eea727ade985cd6513bf9368fe9bb0d5bd5d58e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stage")
    def stage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stage"))

    @stage.setter
    def stage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__113c05d7b8bfbea5f3818c55fbab0087cbddf22f803360674baf8410dc75edf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01f2e6fa6945d8bc87397acce9acc651d9d4cd602bd36e2cbfd2a233643ed717)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceFromSpecification]:
        return typing.cast(typing.Optional[ServiceFromSpecification], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceFromSpecification]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6207310b0e7d2fde9ef4ae48645b312db9ca74f2c4a095b736c701c166ec0daa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.service.ServiceFromSpecificationTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "using": "using",
        "file": "file",
        "path": "path",
        "stage": "stage",
        "text": "text",
    },
)
class ServiceFromSpecificationTemplate:
    def __init__(
        self,
        *,
        using: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFromSpecificationTemplateUsing", typing.Dict[builtins.str, typing.Any]]]],
        file: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        stage: typing.Optional[builtins.str] = None,
        text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param using: using block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#using Service#using}
        :param file: The file name of the service specification template. Example: ``spec.yaml``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#file Service#file}
        :param path: The path to the service specification template file on the given stage. When the path is specified, the ``/`` character is automatically added as a path prefix. Example: ``path/to/spec``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#path Service#path}
        :param stage: The fully qualified name of the stage containing the service specification template file. At symbol (``@``) is added automatically. Example: ``"\\"<db_name>\\".\\"<schema_name>\\".\\"<stage_name>\\""``. For more information about this resource, see `docs <./stage>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#stage Service#stage}
        :param text: The embedded text of the service specification template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#text Service#text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de1e3c19cd8a4201167e510d062a44c0fab900e3089bdad644a11ceff51f5a9d)
            check_type(argname="argument using", value=using, expected_type=type_hints["using"])
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "using": using,
        }
        if file is not None:
            self._values["file"] = file
        if path is not None:
            self._values["path"] = path
        if stage is not None:
            self._values["stage"] = stage
        if text is not None:
            self._values["text"] = text

    @builtins.property
    def using(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFromSpecificationTemplateUsing"]]:
        '''using block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#using Service#using}
        '''
        result = self._values.get("using")
        assert result is not None, "Required property 'using' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFromSpecificationTemplateUsing"]], result)

    @builtins.property
    def file(self) -> typing.Optional[builtins.str]:
        '''The file name of the service specification template. Example: ``spec.yaml``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#file Service#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path to the service specification template file on the given stage.

        When the path is specified, the ``/`` character is automatically added as a path prefix. Example: ``path/to/spec``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#path Service#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        '''The fully qualified name of the stage containing the service specification template file.

        At symbol (``@``) is added automatically. Example: ``"\\"<db_name>\\".\\"<schema_name>\\".\\"<stage_name>\\""``. For more information about this resource, see `docs <./stage>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#stage Service#stage}
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def text(self) -> typing.Optional[builtins.str]:
        '''The embedded text of the service specification template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#text Service#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFromSpecificationTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceFromSpecificationTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.service.ServiceFromSpecificationTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c7b2630f3c13ba2ff89cf12434eb9437b4aafbc433f62c00c6554e57b5905fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putUsing")
    def put_using(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceFromSpecificationTemplateUsing", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e76e0f9842bc37c7ecd214eb81cb64976b8eaf73b49aaede9005232fe3b9693e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUsing", [value]))

    @jsii.member(jsii_name="resetFile")
    def reset_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFile", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetStage")
    def reset_stage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStage", []))

    @jsii.member(jsii_name="resetText")
    def reset_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetText", []))

    @builtins.property
    @jsii.member(jsii_name="using")
    def using(self) -> "ServiceFromSpecificationTemplateUsingList":
        return typing.cast("ServiceFromSpecificationTemplateUsingList", jsii.get(self, "using"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="stageInput")
    def stage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stageInput"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="usingInput")
    def using_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFromSpecificationTemplateUsing"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceFromSpecificationTemplateUsing"]]], jsii.get(self, "usingInput"))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "file"))

    @file.setter
    def file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b590775f9d2aa5db1a3fda3e216bdedc0f3ecdb2685a3492c13364f894b1e30b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "file", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c36e30c8de5ce2c982fa9c65bd6cf7af6e6815f1a4d8e9ac7c1dded12a0e754d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stage")
    def stage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stage"))

    @stage.setter
    def stage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79e2ef7e27104352e034b2d78b68aa5e122f94ce159727ddbaff751070864af9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f25c7e61e8d0a2dfca1862ebd46ba413cfb558afb694cf6e0c43b8a4c919b5c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceFromSpecificationTemplate]:
        return typing.cast(typing.Optional[ServiceFromSpecificationTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceFromSpecificationTemplate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bca621b79cddf2733c8c1d1c8c04bcb3c2c857b44123b099b4713c4580719c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.service.ServiceFromSpecificationTemplateUsing",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class ServiceFromSpecificationTemplateUsing:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: The name of the template variable. The provider wraps it in double quotes by default, so be aware of that while referencing the argument in the spec definition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#key Service#key}
        :param value: The value to assign to the variable in the template. The provider wraps it in ``$$`` by default, so be aware of that while referencing the argument in the spec definition. The value must either be alphanumeric or valid JSON. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#value Service#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a74dacf7c1eb23320456c1e0b51a4f3fcf2472193e821b5aad0508e9e1c4ada)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''The name of the template variable.

        The provider wraps it in double quotes by default, so be aware of that while referencing the argument in the spec definition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#key Service#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The value to assign to the variable in the template.

        The provider wraps it in ``$$`` by default, so be aware of that while referencing the argument in the spec definition. The value must either be alphanumeric or valid JSON.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#value Service#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceFromSpecificationTemplateUsing(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceFromSpecificationTemplateUsingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.service.ServiceFromSpecificationTemplateUsingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6302763d28e0537bee7b9ac9dfa57ad0880de74115f1d28cb7292295a130be3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceFromSpecificationTemplateUsingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87ae70e115430c1e22802a5e97f174273921612778a183096c73d91ebad54463)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceFromSpecificationTemplateUsingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df481a06f8439dab533bce7f78746b65086ed75deaef2ba3cfd93c9cc228c9ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__335d0271790e80a8e196ec4b7c9e4da140c42905c4992019b43ed2559c965fde)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a656540ddee1d5844427f4a6baaad44cb3a4626125f81721bd7944802452c66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFromSpecificationTemplateUsing]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFromSpecificationTemplateUsing]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFromSpecificationTemplateUsing]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a4c75f207cceaccf7ef936315d5168d3c9983f086fbc5c9abc8f639040c6485)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceFromSpecificationTemplateUsingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.service.ServiceFromSpecificationTemplateUsingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9b9c52482de53d06075ba32052d752a41d3ea5c7df143525666be6b00199b8c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fbda72232679a0ca5c9da69f3d9f1f393f524f2d3c53f28744d8855b0bc43d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d6e34f0c456f2515b5c88afc0ed72892eb3a6b21c97fba5085afd0432fb5756)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFromSpecificationTemplateUsing]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFromSpecificationTemplateUsing]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFromSpecificationTemplateUsing]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__530697145f48f11ec82244f34289dba245f51258f15da76f976f8a85074a0505)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.service.ServiceShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServiceShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.service.ServiceShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d88251feba5f00ee04ecb71311259071b29d18d3d01403d0d78c7ba0683e064e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServiceShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01dbab85703f015f8592c6b710984eea49587d753f3e76f0080571d5506986d9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85ff726d684550ed513f041a0ec8835a2e7a9dd01d4566a612d11277f0e0396b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1711059d9102cf84aad4dbc287e52469d9ce85cc61312c1229c97429107f972c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64c8bd852d0bf9dcbeb2ad7e90153b65c48962f4e89291df3dafaf39dc025668)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ServiceShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.service.ServiceShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af98bb95c58719eb256664438104a2e12a5c1ddca81e81e3f7f3ca2653de9583)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="autoResume")
    def auto_resume(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "autoResume"))

    @builtins.property
    @jsii.member(jsii_name="autoSuspendSecs")
    def auto_suspend_secs(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "autoSuspendSecs"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @builtins.property
    @jsii.member(jsii_name="computePool")
    def compute_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "computePool"))

    @builtins.property
    @jsii.member(jsii_name="createdOn")
    def created_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdOn"))

    @builtins.property
    @jsii.member(jsii_name="currentInstances")
    def current_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "currentInstances"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @builtins.property
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsName"))

    @builtins.property
    @jsii.member(jsii_name="externalAccessIntegrations")
    def external_access_integrations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalAccessIntegrations"))

    @builtins.property
    @jsii.member(jsii_name="isAsyncJob")
    def is_async_job(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isAsyncJob"))

    @builtins.property
    @jsii.member(jsii_name="isJob")
    def is_job(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isJob"))

    @builtins.property
    @jsii.member(jsii_name="isUpgrading")
    def is_upgrading(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isUpgrading"))

    @builtins.property
    @jsii.member(jsii_name="managingObjectDomain")
    def managing_object_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managingObjectDomain"))

    @builtins.property
    @jsii.member(jsii_name="managingObjectName")
    def managing_object_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managingObjectName"))

    @builtins.property
    @jsii.member(jsii_name="maxInstances")
    def max_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstances"))

    @builtins.property
    @jsii.member(jsii_name="minInstances")
    def min_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minInstances"))

    @builtins.property
    @jsii.member(jsii_name="minReadyInstances")
    def min_ready_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minReadyInstances"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @builtins.property
    @jsii.member(jsii_name="ownerRoleType")
    def owner_role_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ownerRoleType"))

    @builtins.property
    @jsii.member(jsii_name="queryWarehouse")
    def query_warehouse(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryWarehouse"))

    @builtins.property
    @jsii.member(jsii_name="resumedOn")
    def resumed_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resumedOn"))

    @builtins.property
    @jsii.member(jsii_name="schemaName")
    def schema_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaName"))

    @builtins.property
    @jsii.member(jsii_name="specDigest")
    def spec_digest(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "specDigest"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="suspendedOn")
    def suspended_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suspendedOn"))

    @builtins.property
    @jsii.member(jsii_name="targetInstances")
    def target_instances(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetInstances"))

    @builtins.property
    @jsii.member(jsii_name="updatedOn")
    def updated_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedOn"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceShowOutput]:
        return typing.cast(typing.Optional[ServiceShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceShowOutput]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee144607d7b9efb37d239a0759bf4e3848aa8f108a3fe41ebafb02dc802a2fed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.service.ServiceTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ServiceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#create Service#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#delete Service#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#read Service#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#update Service#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8700df35aebef680e60177be7b92d7b372d9d5579264ed7e4932bed52a1791c)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#create Service#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#delete Service#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#read Service#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflakedb/snowflake/2.3.0/docs/resources/service#update Service#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.service.ServiceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b639ad4308372d258d704927a0db367f3ff5f4d2115d80c1dbc3e8e8d40b837)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b669a834efc788cae0e9b8e28d5cd6b09ec42befa033d40c10998f81ad3a3ecb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e44199f3658b2b04e135e4b2897c56e8458eaa974c7e03c915259591ecb8ab01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad37557df8c978c9a89087f9810e597c3babce00cdb7805e1354b63a5a967027)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d89768aa65fcafafb9cb67e6ead0301bef7e67571a23224e0fcd207e6f5e267)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b1a92726447651dc42d998a40f518ad80ac5b431db07d4849a5fefe0ff7962d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Service",
    "ServiceConfig",
    "ServiceDescribeOutput",
    "ServiceDescribeOutputList",
    "ServiceDescribeOutputOutputReference",
    "ServiceFromSpecification",
    "ServiceFromSpecificationOutputReference",
    "ServiceFromSpecificationTemplate",
    "ServiceFromSpecificationTemplateOutputReference",
    "ServiceFromSpecificationTemplateUsing",
    "ServiceFromSpecificationTemplateUsingList",
    "ServiceFromSpecificationTemplateUsingOutputReference",
    "ServiceShowOutput",
    "ServiceShowOutputList",
    "ServiceShowOutputOutputReference",
    "ServiceTimeouts",
    "ServiceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f0fcd171ed9fea040e48b958e427a617f7126c5cf53a6d7b698416da385f5ae9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    compute_pool: builtins.str,
    database: builtins.str,
    name: builtins.str,
    schema: builtins.str,
    auto_resume: typing.Optional[builtins.str] = None,
    auto_suspend_secs: typing.Optional[jsii.Number] = None,
    comment: typing.Optional[builtins.str] = None,
    external_access_integrations: typing.Optional[typing.Sequence[builtins.str]] = None,
    from_specification: typing.Optional[typing.Union[ServiceFromSpecification, typing.Dict[builtins.str, typing.Any]]] = None,
    from_specification_template: typing.Optional[typing.Union[ServiceFromSpecificationTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    max_instances: typing.Optional[jsii.Number] = None,
    min_instances: typing.Optional[jsii.Number] = None,
    min_ready_instances: typing.Optional[jsii.Number] = None,
    query_warehouse: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b9de553d7c8aca83290d9073d0dfc6dcec6a6b00e4177269840d4eceeee64cd4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d263acd4b4ea426b784a6bdf6e1d4018322246b35478eeb738e69af2492a0bd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__450cf3e6b2ff5446085c39b2154ac5bd4f6ca62df51e39b8ebb5ff6464a1febe(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b72e9800dd0627e0116ca10d645c7f170826229c7e13950b7b73b16b7803aa26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b6acfd4021f68f41835bf8c4a7204163616d8c57155bce1309b50a33538de0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f15a05b6ffcadf7857b8caf91b24c78963e21d8384b10f89b5d8871d50f121(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7243b722e1d3b4eaef005697d60a303456c3c26cb5bc76aecc88cde1cd0ef283(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c08abe1cbc50c8a99c9278c400237e593b84f058f4875ebb0390df1825c8725(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8caa250ebf5ffed3285247b3215a3c202941cdf7a0ff2718171acf5c8baf68da(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1d23aa2480cb2205ccf77896ada60cf36650da58fca7894bb8073a0f1416e97(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5343f4812b1716fde789cf39878014fda1bed9fe279eb3785e971dcbae9cb214(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c07ce04bb873d4b5aea44c62fbea67f165c2a06d2c498df401f012fcf238946(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f8476c3051cb7824803c3669fc73f9140ef2fa7e87684eb48c1539cbe9d6630(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b04c88dbc1c8e82503fda700514dd813460428a4f8c2c951495f85de5e5ef20b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d46e53bbe6a0aff9af3c71b7b4cb56953271598fd0f516a29c41298e536688f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    compute_pool: builtins.str,
    database: builtins.str,
    name: builtins.str,
    schema: builtins.str,
    auto_resume: typing.Optional[builtins.str] = None,
    auto_suspend_secs: typing.Optional[jsii.Number] = None,
    comment: typing.Optional[builtins.str] = None,
    external_access_integrations: typing.Optional[typing.Sequence[builtins.str]] = None,
    from_specification: typing.Optional[typing.Union[ServiceFromSpecification, typing.Dict[builtins.str, typing.Any]]] = None,
    from_specification_template: typing.Optional[typing.Union[ServiceFromSpecificationTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    max_instances: typing.Optional[jsii.Number] = None,
    min_instances: typing.Optional[jsii.Number] = None,
    min_ready_instances: typing.Optional[jsii.Number] = None,
    query_warehouse: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac1510b5763dbe9ffd148b232e3d3078ac8a6c06cd645236ff223aa85c4b100f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2ec85eacd9f6f6b4d254854399f2d486d8b45ed20ba508edba3c13edd56fa4b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d5c73fbc544a3a85a248360133784e9d97899fc075ad03a55f6bf5d19bc95f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31e4c2e4f16335b3911d9de15c6394d55a596a5c6f78578425b3e03a6910e241(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a7fd6f6a9cfcf98302139e16604d7c1bbd51ee0f0a0b4a2c3bc2eaacaa161a5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d283526113d8152527306ab18928e33e5183abda4f6d9df30ba9ceea377e683(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__269dcd001f411762ee5a648ece109908651f28f9fbd7f599b342ac39d3710f2e(
    value: typing.Optional[ServiceDescribeOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__234162c6912411e3690e01268f7f6720bf8171c3b4f95f0f1193c446172f1316(
    *,
    file: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    stage: typing.Optional[builtins.str] = None,
    text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81579154861c98e030d0f41f431ad1d4c22e361251bae81d14bf29ec72a70a55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c77fcf5e92eb6b86364e47f5697e128cc03e00ab04ce44e553956151b21ad934(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eca02107d98a7bb04cbdcab6eea727ade985cd6513bf9368fe9bb0d5bd5d58e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__113c05d7b8bfbea5f3818c55fbab0087cbddf22f803360674baf8410dc75edf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01f2e6fa6945d8bc87397acce9acc651d9d4cd602bd36e2cbfd2a233643ed717(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6207310b0e7d2fde9ef4ae48645b312db9ca74f2c4a095b736c701c166ec0daa(
    value: typing.Optional[ServiceFromSpecification],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de1e3c19cd8a4201167e510d062a44c0fab900e3089bdad644a11ceff51f5a9d(
    *,
    using: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFromSpecificationTemplateUsing, typing.Dict[builtins.str, typing.Any]]]],
    file: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    stage: typing.Optional[builtins.str] = None,
    text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c7b2630f3c13ba2ff89cf12434eb9437b4aafbc433f62c00c6554e57b5905fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e76e0f9842bc37c7ecd214eb81cb64976b8eaf73b49aaede9005232fe3b9693e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceFromSpecificationTemplateUsing, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b590775f9d2aa5db1a3fda3e216bdedc0f3ecdb2685a3492c13364f894b1e30b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c36e30c8de5ce2c982fa9c65bd6cf7af6e6815f1a4d8e9ac7c1dded12a0e754d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e2ef7e27104352e034b2d78b68aa5e122f94ce159727ddbaff751070864af9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25c7e61e8d0a2dfca1862ebd46ba413cfb558afb694cf6e0c43b8a4c919b5c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bca621b79cddf2733c8c1d1c8c04bcb3c2c857b44123b099b4713c4580719c3(
    value: typing.Optional[ServiceFromSpecificationTemplate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a74dacf7c1eb23320456c1e0b51a4f3fcf2472193e821b5aad0508e9e1c4ada(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6302763d28e0537bee7b9ac9dfa57ad0880de74115f1d28cb7292295a130be3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87ae70e115430c1e22802a5e97f174273921612778a183096c73d91ebad54463(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df481a06f8439dab533bce7f78746b65086ed75deaef2ba3cfd93c9cc228c9ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__335d0271790e80a8e196ec4b7c9e4da140c42905c4992019b43ed2559c965fde(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a656540ddee1d5844427f4a6baaad44cb3a4626125f81721bd7944802452c66(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a4c75f207cceaccf7ef936315d5168d3c9983f086fbc5c9abc8f639040c6485(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceFromSpecificationTemplateUsing]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b9c52482de53d06075ba32052d752a41d3ea5c7df143525666be6b00199b8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fbda72232679a0ca5c9da69f3d9f1f393f524f2d3c53f28744d8855b0bc43d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d6e34f0c456f2515b5c88afc0ed72892eb3a6b21c97fba5085afd0432fb5756(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__530697145f48f11ec82244f34289dba245f51258f15da76f976f8a85074a0505(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceFromSpecificationTemplateUsing]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d88251feba5f00ee04ecb71311259071b29d18d3d01403d0d78c7ba0683e064e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01dbab85703f015f8592c6b710984eea49587d753f3e76f0080571d5506986d9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85ff726d684550ed513f041a0ec8835a2e7a9dd01d4566a612d11277f0e0396b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1711059d9102cf84aad4dbc287e52469d9ce85cc61312c1229c97429107f972c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64c8bd852d0bf9dcbeb2ad7e90153b65c48962f4e89291df3dafaf39dc025668(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af98bb95c58719eb256664438104a2e12a5c1ddca81e81e3f7f3ca2653de9583(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee144607d7b9efb37d239a0759bf4e3848aa8f108a3fe41ebafb02dc802a2fed(
    value: typing.Optional[ServiceShowOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8700df35aebef680e60177be7b92d7b372d9d5579264ed7e4932bed52a1791c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b639ad4308372d258d704927a0db367f3ff5f4d2115d80c1dbc3e8e8d40b837(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b669a834efc788cae0e9b8e28d5cd6b09ec42befa033d40c10998f81ad3a3ecb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e44199f3658b2b04e135e4b2897c56e8458eaa974c7e03c915259591ecb8ab01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad37557df8c978c9a89087f9810e597c3babce00cdb7805e1354b63a5a967027(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d89768aa65fcafafb9cb67e6ead0301bef7e67571a23224e0fcd207e6f5e267(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b1a92726447651dc42d998a40f518ad80ac5b431db07d4849a5fefe0ff7962d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
