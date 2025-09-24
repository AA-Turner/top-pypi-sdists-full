r'''
# `newrelic_cloud_gcp_integrations`

Refer to the Terraform Registry for docs: [`newrelic_cloud_gcp_integrations`](https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations).
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


class CloudGcpIntegrations(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrations",
):
    '''Represents a {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations newrelic_cloud_gcp_integrations}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        linked_account_id: jsii.Number,
        account_id: typing.Optional[jsii.Number] = None,
        alloy_db: typing.Optional[typing.Union["CloudGcpIntegrationsAlloyDb", typing.Dict[builtins.str, typing.Any]]] = None,
        app_engine: typing.Optional[typing.Union["CloudGcpIntegrationsAppEngine", typing.Dict[builtins.str, typing.Any]]] = None,
        big_query: typing.Optional[typing.Union["CloudGcpIntegrationsBigQuery", typing.Dict[builtins.str, typing.Any]]] = None,
        big_table: typing.Optional[typing.Union["CloudGcpIntegrationsBigTable", typing.Dict[builtins.str, typing.Any]]] = None,
        composer: typing.Optional[typing.Union["CloudGcpIntegrationsComposer", typing.Dict[builtins.str, typing.Any]]] = None,
        data_flow: typing.Optional[typing.Union["CloudGcpIntegrationsDataFlow", typing.Dict[builtins.str, typing.Any]]] = None,
        data_proc: typing.Optional[typing.Union["CloudGcpIntegrationsDataProc", typing.Dict[builtins.str, typing.Any]]] = None,
        data_store: typing.Optional[typing.Union["CloudGcpIntegrationsDataStore", typing.Dict[builtins.str, typing.Any]]] = None,
        fire_base_database: typing.Optional[typing.Union["CloudGcpIntegrationsFireBaseDatabase", typing.Dict[builtins.str, typing.Any]]] = None,
        fire_base_hosting: typing.Optional[typing.Union["CloudGcpIntegrationsFireBaseHosting", typing.Dict[builtins.str, typing.Any]]] = None,
        fire_base_storage: typing.Optional[typing.Union["CloudGcpIntegrationsFireBaseStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        fire_store: typing.Optional[typing.Union["CloudGcpIntegrationsFireStore", typing.Dict[builtins.str, typing.Any]]] = None,
        functions: typing.Optional[typing.Union["CloudGcpIntegrationsFunctions", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        interconnect: typing.Optional[typing.Union["CloudGcpIntegrationsInterconnect", typing.Dict[builtins.str, typing.Any]]] = None,
        kubernetes: typing.Optional[typing.Union["CloudGcpIntegrationsKubernetes", typing.Dict[builtins.str, typing.Any]]] = None,
        load_balancing: typing.Optional[typing.Union["CloudGcpIntegrationsLoadBalancing", typing.Dict[builtins.str, typing.Any]]] = None,
        mem_cache: typing.Optional[typing.Union["CloudGcpIntegrationsMemCache", typing.Dict[builtins.str, typing.Any]]] = None,
        pub_sub: typing.Optional[typing.Union["CloudGcpIntegrationsPubSub", typing.Dict[builtins.str, typing.Any]]] = None,
        redis: typing.Optional[typing.Union["CloudGcpIntegrationsRedis", typing.Dict[builtins.str, typing.Any]]] = None,
        router: typing.Optional[typing.Union["CloudGcpIntegrationsRouter", typing.Dict[builtins.str, typing.Any]]] = None,
        run: typing.Optional[typing.Union["CloudGcpIntegrationsRun", typing.Dict[builtins.str, typing.Any]]] = None,
        spanner: typing.Optional[typing.Union["CloudGcpIntegrationsSpanner", typing.Dict[builtins.str, typing.Any]]] = None,
        sql: typing.Optional[typing.Union["CloudGcpIntegrationsSql", typing.Dict[builtins.str, typing.Any]]] = None,
        storage: typing.Optional[typing.Union["CloudGcpIntegrationsStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_machines: typing.Optional[typing.Union["CloudGcpIntegrationsVirtualMachines", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_access: typing.Optional[typing.Union["CloudGcpIntegrationsVpcAccess", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations newrelic_cloud_gcp_integrations} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param linked_account_id: Id of the linked gcp account in New Relic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#linked_account_id CloudGcpIntegrations#linked_account_id}
        :param account_id: ID of the newrelic account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#account_id CloudGcpIntegrations#account_id}
        :param alloy_db: alloy_db block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#alloy_db CloudGcpIntegrations#alloy_db}
        :param app_engine: app_engine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#app_engine CloudGcpIntegrations#app_engine}
        :param big_query: big_query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#big_query CloudGcpIntegrations#big_query}
        :param big_table: big_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#big_table CloudGcpIntegrations#big_table}
        :param composer: composer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#composer CloudGcpIntegrations#composer}
        :param data_flow: data_flow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#data_flow CloudGcpIntegrations#data_flow}
        :param data_proc: data_proc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#data_proc CloudGcpIntegrations#data_proc}
        :param data_store: data_store block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#data_store CloudGcpIntegrations#data_store}
        :param fire_base_database: fire_base_database block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#fire_base_database CloudGcpIntegrations#fire_base_database}
        :param fire_base_hosting: fire_base_hosting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#fire_base_hosting CloudGcpIntegrations#fire_base_hosting}
        :param fire_base_storage: fire_base_storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#fire_base_storage CloudGcpIntegrations#fire_base_storage}
        :param fire_store: fire_store block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#fire_store CloudGcpIntegrations#fire_store}
        :param functions: functions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#functions CloudGcpIntegrations#functions}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#id CloudGcpIntegrations#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param interconnect: interconnect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#interconnect CloudGcpIntegrations#interconnect}
        :param kubernetes: kubernetes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#kubernetes CloudGcpIntegrations#kubernetes}
        :param load_balancing: load_balancing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#load_balancing CloudGcpIntegrations#load_balancing}
        :param mem_cache: mem_cache block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#mem_cache CloudGcpIntegrations#mem_cache}
        :param pub_sub: pub_sub block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#pub_sub CloudGcpIntegrations#pub_sub}
        :param redis: redis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#redis CloudGcpIntegrations#redis}
        :param router: router block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#router CloudGcpIntegrations#router}
        :param run: run block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#run CloudGcpIntegrations#run}
        :param spanner: spanner block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#spanner CloudGcpIntegrations#spanner}
        :param sql: sql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#sql CloudGcpIntegrations#sql}
        :param storage: storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#storage CloudGcpIntegrations#storage}
        :param virtual_machines: virtual_machines block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#virtual_machines CloudGcpIntegrations#virtual_machines}
        :param vpc_access: vpc_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#vpc_access CloudGcpIntegrations#vpc_access}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33cf7b4320a550d0b8747b67bd6309347e9661e4592c634f2a6c98923ce6ef57)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudGcpIntegrationsConfig(
            linked_account_id=linked_account_id,
            account_id=account_id,
            alloy_db=alloy_db,
            app_engine=app_engine,
            big_query=big_query,
            big_table=big_table,
            composer=composer,
            data_flow=data_flow,
            data_proc=data_proc,
            data_store=data_store,
            fire_base_database=fire_base_database,
            fire_base_hosting=fire_base_hosting,
            fire_base_storage=fire_base_storage,
            fire_store=fire_store,
            functions=functions,
            id=id,
            interconnect=interconnect,
            kubernetes=kubernetes,
            load_balancing=load_balancing,
            mem_cache=mem_cache,
            pub_sub=pub_sub,
            redis=redis,
            router=router,
            run=run,
            spanner=spanner,
            sql=sql,
            storage=storage,
            virtual_machines=virtual_machines,
            vpc_access=vpc_access,
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
        '''Generates CDKTF code for importing a CloudGcpIntegrations resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CloudGcpIntegrations to import.
        :param import_from_id: The id of the existing CloudGcpIntegrations that should be imported. Refer to the {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CloudGcpIntegrations to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d447a75ff07da8461de16a8e995d4eefecc1acbcf384f87a7f61499bf74068c8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAlloyDb")
    def put_alloy_db(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsAlloyDb(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAlloyDb", [value]))

    @jsii.member(jsii_name="putAppEngine")
    def put_app_engine(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsAppEngine(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putAppEngine", [value]))

    @jsii.member(jsii_name="putBigQuery")
    def put_big_query(
        self,
        *,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fetch_tags: to fetch tags of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#fetch_tags CloudGcpIntegrations#fetch_tags}
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsBigQuery(
            fetch_tags=fetch_tags, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putBigQuery", [value]))

    @jsii.member(jsii_name="putBigTable")
    def put_big_table(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsBigTable(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putBigTable", [value]))

    @jsii.member(jsii_name="putComposer")
    def put_composer(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsComposer(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putComposer", [value]))

    @jsii.member(jsii_name="putDataFlow")
    def put_data_flow(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsDataFlow(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putDataFlow", [value]))

    @jsii.member(jsii_name="putDataProc")
    def put_data_proc(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsDataProc(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putDataProc", [value]))

    @jsii.member(jsii_name="putDataStore")
    def put_data_store(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsDataStore(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putDataStore", [value]))

    @jsii.member(jsii_name="putFireBaseDatabase")
    def put_fire_base_database(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsFireBaseDatabase(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putFireBaseDatabase", [value]))

    @jsii.member(jsii_name="putFireBaseHosting")
    def put_fire_base_hosting(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsFireBaseHosting(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putFireBaseHosting", [value]))

    @jsii.member(jsii_name="putFireBaseStorage")
    def put_fire_base_storage(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsFireBaseStorage(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putFireBaseStorage", [value]))

    @jsii.member(jsii_name="putFireStore")
    def put_fire_store(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsFireStore(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putFireStore", [value]))

    @jsii.member(jsii_name="putFunctions")
    def put_functions(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsFunctions(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putFunctions", [value]))

    @jsii.member(jsii_name="putInterconnect")
    def put_interconnect(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsInterconnect(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putInterconnect", [value]))

    @jsii.member(jsii_name="putKubernetes")
    def put_kubernetes(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsKubernetes(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putKubernetes", [value]))

    @jsii.member(jsii_name="putLoadBalancing")
    def put_load_balancing(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsLoadBalancing(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putLoadBalancing", [value]))

    @jsii.member(jsii_name="putMemCache")
    def put_mem_cache(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsMemCache(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putMemCache", [value]))

    @jsii.member(jsii_name="putPubSub")
    def put_pub_sub(
        self,
        *,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fetch_tags: to fetch tags of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#fetch_tags CloudGcpIntegrations#fetch_tags}
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsPubSub(
            fetch_tags=fetch_tags, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putPubSub", [value]))

    @jsii.member(jsii_name="putRedis")
    def put_redis(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsRedis(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putRedis", [value]))

    @jsii.member(jsii_name="putRouter")
    def put_router(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsRouter(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putRouter", [value]))

    @jsii.member(jsii_name="putRun")
    def put_run(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsRun(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putRun", [value]))

    @jsii.member(jsii_name="putSpanner")
    def put_spanner(
        self,
        *,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fetch_tags: to fetch tags of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#fetch_tags CloudGcpIntegrations#fetch_tags}
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsSpanner(
            fetch_tags=fetch_tags, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putSpanner", [value]))

    @jsii.member(jsii_name="putSql")
    def put_sql(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsSql(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putSql", [value]))

    @jsii.member(jsii_name="putStorage")
    def put_storage(
        self,
        *,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fetch_tags: to fetch tags of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#fetch_tags CloudGcpIntegrations#fetch_tags}
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsStorage(
            fetch_tags=fetch_tags, metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putStorage", [value]))

    @jsii.member(jsii_name="putVirtualMachines")
    def put_virtual_machines(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsVirtualMachines(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualMachines", [value]))

    @jsii.member(jsii_name="putVpcAccess")
    def put_vpc_access(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        value = CloudGcpIntegrationsVpcAccess(
            metrics_polling_interval=metrics_polling_interval
        )

        return typing.cast(None, jsii.invoke(self, "putVpcAccess", [value]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetAlloyDb")
    def reset_alloy_db(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlloyDb", []))

    @jsii.member(jsii_name="resetAppEngine")
    def reset_app_engine(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppEngine", []))

    @jsii.member(jsii_name="resetBigQuery")
    def reset_big_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigQuery", []))

    @jsii.member(jsii_name="resetBigTable")
    def reset_big_table(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigTable", []))

    @jsii.member(jsii_name="resetComposer")
    def reset_composer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComposer", []))

    @jsii.member(jsii_name="resetDataFlow")
    def reset_data_flow(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataFlow", []))

    @jsii.member(jsii_name="resetDataProc")
    def reset_data_proc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataProc", []))

    @jsii.member(jsii_name="resetDataStore")
    def reset_data_store(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataStore", []))

    @jsii.member(jsii_name="resetFireBaseDatabase")
    def reset_fire_base_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFireBaseDatabase", []))

    @jsii.member(jsii_name="resetFireBaseHosting")
    def reset_fire_base_hosting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFireBaseHosting", []))

    @jsii.member(jsii_name="resetFireBaseStorage")
    def reset_fire_base_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFireBaseStorage", []))

    @jsii.member(jsii_name="resetFireStore")
    def reset_fire_store(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFireStore", []))

    @jsii.member(jsii_name="resetFunctions")
    def reset_functions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFunctions", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInterconnect")
    def reset_interconnect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterconnect", []))

    @jsii.member(jsii_name="resetKubernetes")
    def reset_kubernetes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubernetes", []))

    @jsii.member(jsii_name="resetLoadBalancing")
    def reset_load_balancing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancing", []))

    @jsii.member(jsii_name="resetMemCache")
    def reset_mem_cache(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemCache", []))

    @jsii.member(jsii_name="resetPubSub")
    def reset_pub_sub(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPubSub", []))

    @jsii.member(jsii_name="resetRedis")
    def reset_redis(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedis", []))

    @jsii.member(jsii_name="resetRouter")
    def reset_router(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouter", []))

    @jsii.member(jsii_name="resetRun")
    def reset_run(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRun", []))

    @jsii.member(jsii_name="resetSpanner")
    def reset_spanner(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpanner", []))

    @jsii.member(jsii_name="resetSql")
    def reset_sql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSql", []))

    @jsii.member(jsii_name="resetStorage")
    def reset_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorage", []))

    @jsii.member(jsii_name="resetVirtualMachines")
    def reset_virtual_machines(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualMachines", []))

    @jsii.member(jsii_name="resetVpcAccess")
    def reset_vpc_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcAccess", []))

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
    @jsii.member(jsii_name="alloyDb")
    def alloy_db(self) -> "CloudGcpIntegrationsAlloyDbOutputReference":
        return typing.cast("CloudGcpIntegrationsAlloyDbOutputReference", jsii.get(self, "alloyDb"))

    @builtins.property
    @jsii.member(jsii_name="appEngine")
    def app_engine(self) -> "CloudGcpIntegrationsAppEngineOutputReference":
        return typing.cast("CloudGcpIntegrationsAppEngineOutputReference", jsii.get(self, "appEngine"))

    @builtins.property
    @jsii.member(jsii_name="bigQuery")
    def big_query(self) -> "CloudGcpIntegrationsBigQueryOutputReference":
        return typing.cast("CloudGcpIntegrationsBigQueryOutputReference", jsii.get(self, "bigQuery"))

    @builtins.property
    @jsii.member(jsii_name="bigTable")
    def big_table(self) -> "CloudGcpIntegrationsBigTableOutputReference":
        return typing.cast("CloudGcpIntegrationsBigTableOutputReference", jsii.get(self, "bigTable"))

    @builtins.property
    @jsii.member(jsii_name="composer")
    def composer(self) -> "CloudGcpIntegrationsComposerOutputReference":
        return typing.cast("CloudGcpIntegrationsComposerOutputReference", jsii.get(self, "composer"))

    @builtins.property
    @jsii.member(jsii_name="dataFlow")
    def data_flow(self) -> "CloudGcpIntegrationsDataFlowOutputReference":
        return typing.cast("CloudGcpIntegrationsDataFlowOutputReference", jsii.get(self, "dataFlow"))

    @builtins.property
    @jsii.member(jsii_name="dataProc")
    def data_proc(self) -> "CloudGcpIntegrationsDataProcOutputReference":
        return typing.cast("CloudGcpIntegrationsDataProcOutputReference", jsii.get(self, "dataProc"))

    @builtins.property
    @jsii.member(jsii_name="dataStore")
    def data_store(self) -> "CloudGcpIntegrationsDataStoreOutputReference":
        return typing.cast("CloudGcpIntegrationsDataStoreOutputReference", jsii.get(self, "dataStore"))

    @builtins.property
    @jsii.member(jsii_name="fireBaseDatabase")
    def fire_base_database(
        self,
    ) -> "CloudGcpIntegrationsFireBaseDatabaseOutputReference":
        return typing.cast("CloudGcpIntegrationsFireBaseDatabaseOutputReference", jsii.get(self, "fireBaseDatabase"))

    @builtins.property
    @jsii.member(jsii_name="fireBaseHosting")
    def fire_base_hosting(self) -> "CloudGcpIntegrationsFireBaseHostingOutputReference":
        return typing.cast("CloudGcpIntegrationsFireBaseHostingOutputReference", jsii.get(self, "fireBaseHosting"))

    @builtins.property
    @jsii.member(jsii_name="fireBaseStorage")
    def fire_base_storage(self) -> "CloudGcpIntegrationsFireBaseStorageOutputReference":
        return typing.cast("CloudGcpIntegrationsFireBaseStorageOutputReference", jsii.get(self, "fireBaseStorage"))

    @builtins.property
    @jsii.member(jsii_name="fireStore")
    def fire_store(self) -> "CloudGcpIntegrationsFireStoreOutputReference":
        return typing.cast("CloudGcpIntegrationsFireStoreOutputReference", jsii.get(self, "fireStore"))

    @builtins.property
    @jsii.member(jsii_name="functions")
    def functions(self) -> "CloudGcpIntegrationsFunctionsOutputReference":
        return typing.cast("CloudGcpIntegrationsFunctionsOutputReference", jsii.get(self, "functions"))

    @builtins.property
    @jsii.member(jsii_name="interconnect")
    def interconnect(self) -> "CloudGcpIntegrationsInterconnectOutputReference":
        return typing.cast("CloudGcpIntegrationsInterconnectOutputReference", jsii.get(self, "interconnect"))

    @builtins.property
    @jsii.member(jsii_name="kubernetes")
    def kubernetes(self) -> "CloudGcpIntegrationsKubernetesOutputReference":
        return typing.cast("CloudGcpIntegrationsKubernetesOutputReference", jsii.get(self, "kubernetes"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancing")
    def load_balancing(self) -> "CloudGcpIntegrationsLoadBalancingOutputReference":
        return typing.cast("CloudGcpIntegrationsLoadBalancingOutputReference", jsii.get(self, "loadBalancing"))

    @builtins.property
    @jsii.member(jsii_name="memCache")
    def mem_cache(self) -> "CloudGcpIntegrationsMemCacheOutputReference":
        return typing.cast("CloudGcpIntegrationsMemCacheOutputReference", jsii.get(self, "memCache"))

    @builtins.property
    @jsii.member(jsii_name="pubSub")
    def pub_sub(self) -> "CloudGcpIntegrationsPubSubOutputReference":
        return typing.cast("CloudGcpIntegrationsPubSubOutputReference", jsii.get(self, "pubSub"))

    @builtins.property
    @jsii.member(jsii_name="redis")
    def redis(self) -> "CloudGcpIntegrationsRedisOutputReference":
        return typing.cast("CloudGcpIntegrationsRedisOutputReference", jsii.get(self, "redis"))

    @builtins.property
    @jsii.member(jsii_name="router")
    def router(self) -> "CloudGcpIntegrationsRouterOutputReference":
        return typing.cast("CloudGcpIntegrationsRouterOutputReference", jsii.get(self, "router"))

    @builtins.property
    @jsii.member(jsii_name="run")
    def run(self) -> "CloudGcpIntegrationsRunOutputReference":
        return typing.cast("CloudGcpIntegrationsRunOutputReference", jsii.get(self, "run"))

    @builtins.property
    @jsii.member(jsii_name="spanner")
    def spanner(self) -> "CloudGcpIntegrationsSpannerOutputReference":
        return typing.cast("CloudGcpIntegrationsSpannerOutputReference", jsii.get(self, "spanner"))

    @builtins.property
    @jsii.member(jsii_name="sql")
    def sql(self) -> "CloudGcpIntegrationsSqlOutputReference":
        return typing.cast("CloudGcpIntegrationsSqlOutputReference", jsii.get(self, "sql"))

    @builtins.property
    @jsii.member(jsii_name="storage")
    def storage(self) -> "CloudGcpIntegrationsStorageOutputReference":
        return typing.cast("CloudGcpIntegrationsStorageOutputReference", jsii.get(self, "storage"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachines")
    def virtual_machines(self) -> "CloudGcpIntegrationsVirtualMachinesOutputReference":
        return typing.cast("CloudGcpIntegrationsVirtualMachinesOutputReference", jsii.get(self, "virtualMachines"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccess")
    def vpc_access(self) -> "CloudGcpIntegrationsVpcAccessOutputReference":
        return typing.cast("CloudGcpIntegrationsVpcAccessOutputReference", jsii.get(self, "vpcAccess"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="alloyDbInput")
    def alloy_db_input(self) -> typing.Optional["CloudGcpIntegrationsAlloyDb"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsAlloyDb"], jsii.get(self, "alloyDbInput"))

    @builtins.property
    @jsii.member(jsii_name="appEngineInput")
    def app_engine_input(self) -> typing.Optional["CloudGcpIntegrationsAppEngine"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsAppEngine"], jsii.get(self, "appEngineInput"))

    @builtins.property
    @jsii.member(jsii_name="bigQueryInput")
    def big_query_input(self) -> typing.Optional["CloudGcpIntegrationsBigQuery"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsBigQuery"], jsii.get(self, "bigQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="bigTableInput")
    def big_table_input(self) -> typing.Optional["CloudGcpIntegrationsBigTable"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsBigTable"], jsii.get(self, "bigTableInput"))

    @builtins.property
    @jsii.member(jsii_name="composerInput")
    def composer_input(self) -> typing.Optional["CloudGcpIntegrationsComposer"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsComposer"], jsii.get(self, "composerInput"))

    @builtins.property
    @jsii.member(jsii_name="dataFlowInput")
    def data_flow_input(self) -> typing.Optional["CloudGcpIntegrationsDataFlow"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsDataFlow"], jsii.get(self, "dataFlowInput"))

    @builtins.property
    @jsii.member(jsii_name="dataProcInput")
    def data_proc_input(self) -> typing.Optional["CloudGcpIntegrationsDataProc"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsDataProc"], jsii.get(self, "dataProcInput"))

    @builtins.property
    @jsii.member(jsii_name="dataStoreInput")
    def data_store_input(self) -> typing.Optional["CloudGcpIntegrationsDataStore"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsDataStore"], jsii.get(self, "dataStoreInput"))

    @builtins.property
    @jsii.member(jsii_name="fireBaseDatabaseInput")
    def fire_base_database_input(
        self,
    ) -> typing.Optional["CloudGcpIntegrationsFireBaseDatabase"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsFireBaseDatabase"], jsii.get(self, "fireBaseDatabaseInput"))

    @builtins.property
    @jsii.member(jsii_name="fireBaseHostingInput")
    def fire_base_hosting_input(
        self,
    ) -> typing.Optional["CloudGcpIntegrationsFireBaseHosting"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsFireBaseHosting"], jsii.get(self, "fireBaseHostingInput"))

    @builtins.property
    @jsii.member(jsii_name="fireBaseStorageInput")
    def fire_base_storage_input(
        self,
    ) -> typing.Optional["CloudGcpIntegrationsFireBaseStorage"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsFireBaseStorage"], jsii.get(self, "fireBaseStorageInput"))

    @builtins.property
    @jsii.member(jsii_name="fireStoreInput")
    def fire_store_input(self) -> typing.Optional["CloudGcpIntegrationsFireStore"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsFireStore"], jsii.get(self, "fireStoreInput"))

    @builtins.property
    @jsii.member(jsii_name="functionsInput")
    def functions_input(self) -> typing.Optional["CloudGcpIntegrationsFunctions"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsFunctions"], jsii.get(self, "functionsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="interconnectInput")
    def interconnect_input(self) -> typing.Optional["CloudGcpIntegrationsInterconnect"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsInterconnect"], jsii.get(self, "interconnectInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesInput")
    def kubernetes_input(self) -> typing.Optional["CloudGcpIntegrationsKubernetes"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsKubernetes"], jsii.get(self, "kubernetesInput"))

    @builtins.property
    @jsii.member(jsii_name="linkedAccountIdInput")
    def linked_account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "linkedAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancingInput")
    def load_balancing_input(
        self,
    ) -> typing.Optional["CloudGcpIntegrationsLoadBalancing"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsLoadBalancing"], jsii.get(self, "loadBalancingInput"))

    @builtins.property
    @jsii.member(jsii_name="memCacheInput")
    def mem_cache_input(self) -> typing.Optional["CloudGcpIntegrationsMemCache"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsMemCache"], jsii.get(self, "memCacheInput"))

    @builtins.property
    @jsii.member(jsii_name="pubSubInput")
    def pub_sub_input(self) -> typing.Optional["CloudGcpIntegrationsPubSub"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsPubSub"], jsii.get(self, "pubSubInput"))

    @builtins.property
    @jsii.member(jsii_name="redisInput")
    def redis_input(self) -> typing.Optional["CloudGcpIntegrationsRedis"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsRedis"], jsii.get(self, "redisInput"))

    @builtins.property
    @jsii.member(jsii_name="routerInput")
    def router_input(self) -> typing.Optional["CloudGcpIntegrationsRouter"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsRouter"], jsii.get(self, "routerInput"))

    @builtins.property
    @jsii.member(jsii_name="runInput")
    def run_input(self) -> typing.Optional["CloudGcpIntegrationsRun"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsRun"], jsii.get(self, "runInput"))

    @builtins.property
    @jsii.member(jsii_name="spannerInput")
    def spanner_input(self) -> typing.Optional["CloudGcpIntegrationsSpanner"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsSpanner"], jsii.get(self, "spannerInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlInput")
    def sql_input(self) -> typing.Optional["CloudGcpIntegrationsSql"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsSql"], jsii.get(self, "sqlInput"))

    @builtins.property
    @jsii.member(jsii_name="storageInput")
    def storage_input(self) -> typing.Optional["CloudGcpIntegrationsStorage"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsStorage"], jsii.get(self, "storageInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualMachinesInput")
    def virtual_machines_input(
        self,
    ) -> typing.Optional["CloudGcpIntegrationsVirtualMachines"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsVirtualMachines"], jsii.get(self, "virtualMachinesInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccessInput")
    def vpc_access_input(self) -> typing.Optional["CloudGcpIntegrationsVpcAccess"]:
        return typing.cast(typing.Optional["CloudGcpIntegrationsVpcAccess"], jsii.get(self, "vpcAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efb17273c3fbf33f0e0609e23ca23b31c5b32738a1d8b2b6da8a7d06b98302a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7612724444e8d28a8a047dea1cc60ad7ba5efd08acd1c43430bee9c20c70e948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="linkedAccountId")
    def linked_account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "linkedAccountId"))

    @linked_account_id.setter
    def linked_account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f405e01509f6be3df35158b788d901dedb3966463a614901cea7783194002e99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkedAccountId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsAlloyDb",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudGcpIntegrationsAlloyDb:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29355de8dcddfb1ccde0ee296b6c01ed7c8bb2d347bd981860f69d6837e8bf49)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsAlloyDb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsAlloyDbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsAlloyDbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89eb41116e169274623cb2a3fe7c75889474cd876d4cb4478f73f30c5e9711c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05e092d8e4ece82f910d955afbd1cc28fd7f4386a93aa2519be40f770d847c0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsAlloyDb]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsAlloyDb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudGcpIntegrationsAlloyDb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b682132cb22a42ef53f5df73eb74283f27df5ebc1d42882eca6122d09263323)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsAppEngine",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudGcpIntegrationsAppEngine:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e0ea11eb547c1edb6235920c85306b5efb55576b0996e0804a953f588a3091c)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsAppEngine(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsAppEngineOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsAppEngineOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a81041e761f3ef997022d0857c5f7cbb087b0d3c7e3d85ff7a0735fdcb3f5f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f89cdcae0016a3ddfc9b1e25d81314e5238ab53c70f41880503cedb69d452da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsAppEngine]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsAppEngine], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudGcpIntegrationsAppEngine],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2c7e5d284b5ac99f4ee060e916e7063ea664c53d6427d4bda5a815e35801939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsBigQuery",
    jsii_struct_bases=[],
    name_mapping={
        "fetch_tags": "fetchTags",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudGcpIntegrationsBigQuery:
    def __init__(
        self,
        *,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fetch_tags: to fetch tags of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#fetch_tags CloudGcpIntegrations#fetch_tags}
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__617061e9fe40845851969430d28b73acc3f96927f1ddc19909745b5e85a2c5dc)
            check_type(argname="argument fetch_tags", value=fetch_tags, expected_type=type_hints["fetch_tags"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fetch_tags is not None:
            self._values["fetch_tags"] = fetch_tags
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''to fetch tags of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#fetch_tags CloudGcpIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsBigQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsBigQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsBigQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__629e2cd1c26a6dc4423c7ec01c00e05d19ef5a4891f4bf02dbdf62cd3ab37064)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFetchTags")
    def reset_fetch_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchTags", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="fetchTagsInput")
    def fetch_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchTags")
    def fetch_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchTags"))

    @fetch_tags.setter
    def fetch_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__934a776a9743e1bf514f49c415a095771d8b3bd7a8bc61d4676def55cdbd3f1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed50608b40c33129367e9f7eae7526d3a4ffa6e91047f053b61e3c2a71199b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsBigQuery]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsBigQuery], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudGcpIntegrationsBigQuery],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f690719ad14678b3251cbbab8f7bc87405388a47c4e168e6155d6c56fe8aed37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsBigTable",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudGcpIntegrationsBigTable:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe9da90aa8dd0ae0b9bac48957979fc030f02308d0840af73acbafa2ab8522aa)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsBigTable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsBigTableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsBigTableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__489f16073fa3a8949cb26acb09c88106fb29514e983eee5ac09c732a37e635f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b2852ff7c7db3dfa17efb03b250722fab788b7ef8168e22bd2187141b96c7f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsBigTable]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsBigTable], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudGcpIntegrationsBigTable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc6557653a3c54ddde560b23eaa19680214c572e4b6495bd499b0b5b25fca3fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsComposer",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudGcpIntegrationsComposer:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbf52cdfc38d910cf57ccb0e9c180cca525b94d5fb758cc9dec514f406740240)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsComposer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsComposerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsComposerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04b5a7d1231e2571095700053fc1d4c745c9680eba2207c748d4c03e24e4d8fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d1a5262362c2ec9745f38a66c861d9381b4385502f2819c929315fbabc20f58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsComposer]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsComposer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudGcpIntegrationsComposer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1e1859ec6b12748859d2eaf9bdfb30186a07d75c75994d1af620fe817bad9e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "linked_account_id": "linkedAccountId",
        "account_id": "accountId",
        "alloy_db": "alloyDb",
        "app_engine": "appEngine",
        "big_query": "bigQuery",
        "big_table": "bigTable",
        "composer": "composer",
        "data_flow": "dataFlow",
        "data_proc": "dataProc",
        "data_store": "dataStore",
        "fire_base_database": "fireBaseDatabase",
        "fire_base_hosting": "fireBaseHosting",
        "fire_base_storage": "fireBaseStorage",
        "fire_store": "fireStore",
        "functions": "functions",
        "id": "id",
        "interconnect": "interconnect",
        "kubernetes": "kubernetes",
        "load_balancing": "loadBalancing",
        "mem_cache": "memCache",
        "pub_sub": "pubSub",
        "redis": "redis",
        "router": "router",
        "run": "run",
        "spanner": "spanner",
        "sql": "sql",
        "storage": "storage",
        "virtual_machines": "virtualMachines",
        "vpc_access": "vpcAccess",
    },
)
class CloudGcpIntegrationsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        linked_account_id: jsii.Number,
        account_id: typing.Optional[jsii.Number] = None,
        alloy_db: typing.Optional[typing.Union[CloudGcpIntegrationsAlloyDb, typing.Dict[builtins.str, typing.Any]]] = None,
        app_engine: typing.Optional[typing.Union[CloudGcpIntegrationsAppEngine, typing.Dict[builtins.str, typing.Any]]] = None,
        big_query: typing.Optional[typing.Union[CloudGcpIntegrationsBigQuery, typing.Dict[builtins.str, typing.Any]]] = None,
        big_table: typing.Optional[typing.Union[CloudGcpIntegrationsBigTable, typing.Dict[builtins.str, typing.Any]]] = None,
        composer: typing.Optional[typing.Union[CloudGcpIntegrationsComposer, typing.Dict[builtins.str, typing.Any]]] = None,
        data_flow: typing.Optional[typing.Union["CloudGcpIntegrationsDataFlow", typing.Dict[builtins.str, typing.Any]]] = None,
        data_proc: typing.Optional[typing.Union["CloudGcpIntegrationsDataProc", typing.Dict[builtins.str, typing.Any]]] = None,
        data_store: typing.Optional[typing.Union["CloudGcpIntegrationsDataStore", typing.Dict[builtins.str, typing.Any]]] = None,
        fire_base_database: typing.Optional[typing.Union["CloudGcpIntegrationsFireBaseDatabase", typing.Dict[builtins.str, typing.Any]]] = None,
        fire_base_hosting: typing.Optional[typing.Union["CloudGcpIntegrationsFireBaseHosting", typing.Dict[builtins.str, typing.Any]]] = None,
        fire_base_storage: typing.Optional[typing.Union["CloudGcpIntegrationsFireBaseStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        fire_store: typing.Optional[typing.Union["CloudGcpIntegrationsFireStore", typing.Dict[builtins.str, typing.Any]]] = None,
        functions: typing.Optional[typing.Union["CloudGcpIntegrationsFunctions", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        interconnect: typing.Optional[typing.Union["CloudGcpIntegrationsInterconnect", typing.Dict[builtins.str, typing.Any]]] = None,
        kubernetes: typing.Optional[typing.Union["CloudGcpIntegrationsKubernetes", typing.Dict[builtins.str, typing.Any]]] = None,
        load_balancing: typing.Optional[typing.Union["CloudGcpIntegrationsLoadBalancing", typing.Dict[builtins.str, typing.Any]]] = None,
        mem_cache: typing.Optional[typing.Union["CloudGcpIntegrationsMemCache", typing.Dict[builtins.str, typing.Any]]] = None,
        pub_sub: typing.Optional[typing.Union["CloudGcpIntegrationsPubSub", typing.Dict[builtins.str, typing.Any]]] = None,
        redis: typing.Optional[typing.Union["CloudGcpIntegrationsRedis", typing.Dict[builtins.str, typing.Any]]] = None,
        router: typing.Optional[typing.Union["CloudGcpIntegrationsRouter", typing.Dict[builtins.str, typing.Any]]] = None,
        run: typing.Optional[typing.Union["CloudGcpIntegrationsRun", typing.Dict[builtins.str, typing.Any]]] = None,
        spanner: typing.Optional[typing.Union["CloudGcpIntegrationsSpanner", typing.Dict[builtins.str, typing.Any]]] = None,
        sql: typing.Optional[typing.Union["CloudGcpIntegrationsSql", typing.Dict[builtins.str, typing.Any]]] = None,
        storage: typing.Optional[typing.Union["CloudGcpIntegrationsStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_machines: typing.Optional[typing.Union["CloudGcpIntegrationsVirtualMachines", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_access: typing.Optional[typing.Union["CloudGcpIntegrationsVpcAccess", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param linked_account_id: Id of the linked gcp account in New Relic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#linked_account_id CloudGcpIntegrations#linked_account_id}
        :param account_id: ID of the newrelic account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#account_id CloudGcpIntegrations#account_id}
        :param alloy_db: alloy_db block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#alloy_db CloudGcpIntegrations#alloy_db}
        :param app_engine: app_engine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#app_engine CloudGcpIntegrations#app_engine}
        :param big_query: big_query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#big_query CloudGcpIntegrations#big_query}
        :param big_table: big_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#big_table CloudGcpIntegrations#big_table}
        :param composer: composer block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#composer CloudGcpIntegrations#composer}
        :param data_flow: data_flow block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#data_flow CloudGcpIntegrations#data_flow}
        :param data_proc: data_proc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#data_proc CloudGcpIntegrations#data_proc}
        :param data_store: data_store block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#data_store CloudGcpIntegrations#data_store}
        :param fire_base_database: fire_base_database block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#fire_base_database CloudGcpIntegrations#fire_base_database}
        :param fire_base_hosting: fire_base_hosting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#fire_base_hosting CloudGcpIntegrations#fire_base_hosting}
        :param fire_base_storage: fire_base_storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#fire_base_storage CloudGcpIntegrations#fire_base_storage}
        :param fire_store: fire_store block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#fire_store CloudGcpIntegrations#fire_store}
        :param functions: functions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#functions CloudGcpIntegrations#functions}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#id CloudGcpIntegrations#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param interconnect: interconnect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#interconnect CloudGcpIntegrations#interconnect}
        :param kubernetes: kubernetes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#kubernetes CloudGcpIntegrations#kubernetes}
        :param load_balancing: load_balancing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#load_balancing CloudGcpIntegrations#load_balancing}
        :param mem_cache: mem_cache block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#mem_cache CloudGcpIntegrations#mem_cache}
        :param pub_sub: pub_sub block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#pub_sub CloudGcpIntegrations#pub_sub}
        :param redis: redis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#redis CloudGcpIntegrations#redis}
        :param router: router block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#router CloudGcpIntegrations#router}
        :param run: run block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#run CloudGcpIntegrations#run}
        :param spanner: spanner block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#spanner CloudGcpIntegrations#spanner}
        :param sql: sql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#sql CloudGcpIntegrations#sql}
        :param storage: storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#storage CloudGcpIntegrations#storage}
        :param virtual_machines: virtual_machines block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#virtual_machines CloudGcpIntegrations#virtual_machines}
        :param vpc_access: vpc_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#vpc_access CloudGcpIntegrations#vpc_access}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(alloy_db, dict):
            alloy_db = CloudGcpIntegrationsAlloyDb(**alloy_db)
        if isinstance(app_engine, dict):
            app_engine = CloudGcpIntegrationsAppEngine(**app_engine)
        if isinstance(big_query, dict):
            big_query = CloudGcpIntegrationsBigQuery(**big_query)
        if isinstance(big_table, dict):
            big_table = CloudGcpIntegrationsBigTable(**big_table)
        if isinstance(composer, dict):
            composer = CloudGcpIntegrationsComposer(**composer)
        if isinstance(data_flow, dict):
            data_flow = CloudGcpIntegrationsDataFlow(**data_flow)
        if isinstance(data_proc, dict):
            data_proc = CloudGcpIntegrationsDataProc(**data_proc)
        if isinstance(data_store, dict):
            data_store = CloudGcpIntegrationsDataStore(**data_store)
        if isinstance(fire_base_database, dict):
            fire_base_database = CloudGcpIntegrationsFireBaseDatabase(**fire_base_database)
        if isinstance(fire_base_hosting, dict):
            fire_base_hosting = CloudGcpIntegrationsFireBaseHosting(**fire_base_hosting)
        if isinstance(fire_base_storage, dict):
            fire_base_storage = CloudGcpIntegrationsFireBaseStorage(**fire_base_storage)
        if isinstance(fire_store, dict):
            fire_store = CloudGcpIntegrationsFireStore(**fire_store)
        if isinstance(functions, dict):
            functions = CloudGcpIntegrationsFunctions(**functions)
        if isinstance(interconnect, dict):
            interconnect = CloudGcpIntegrationsInterconnect(**interconnect)
        if isinstance(kubernetes, dict):
            kubernetes = CloudGcpIntegrationsKubernetes(**kubernetes)
        if isinstance(load_balancing, dict):
            load_balancing = CloudGcpIntegrationsLoadBalancing(**load_balancing)
        if isinstance(mem_cache, dict):
            mem_cache = CloudGcpIntegrationsMemCache(**mem_cache)
        if isinstance(pub_sub, dict):
            pub_sub = CloudGcpIntegrationsPubSub(**pub_sub)
        if isinstance(redis, dict):
            redis = CloudGcpIntegrationsRedis(**redis)
        if isinstance(router, dict):
            router = CloudGcpIntegrationsRouter(**router)
        if isinstance(run, dict):
            run = CloudGcpIntegrationsRun(**run)
        if isinstance(spanner, dict):
            spanner = CloudGcpIntegrationsSpanner(**spanner)
        if isinstance(sql, dict):
            sql = CloudGcpIntegrationsSql(**sql)
        if isinstance(storage, dict):
            storage = CloudGcpIntegrationsStorage(**storage)
        if isinstance(virtual_machines, dict):
            virtual_machines = CloudGcpIntegrationsVirtualMachines(**virtual_machines)
        if isinstance(vpc_access, dict):
            vpc_access = CloudGcpIntegrationsVpcAccess(**vpc_access)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e8e342b2eb95e9d0b60dc1d58206e4733dcef22cc0f55837cebc900a39aa864)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument linked_account_id", value=linked_account_id, expected_type=type_hints["linked_account_id"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument alloy_db", value=alloy_db, expected_type=type_hints["alloy_db"])
            check_type(argname="argument app_engine", value=app_engine, expected_type=type_hints["app_engine"])
            check_type(argname="argument big_query", value=big_query, expected_type=type_hints["big_query"])
            check_type(argname="argument big_table", value=big_table, expected_type=type_hints["big_table"])
            check_type(argname="argument composer", value=composer, expected_type=type_hints["composer"])
            check_type(argname="argument data_flow", value=data_flow, expected_type=type_hints["data_flow"])
            check_type(argname="argument data_proc", value=data_proc, expected_type=type_hints["data_proc"])
            check_type(argname="argument data_store", value=data_store, expected_type=type_hints["data_store"])
            check_type(argname="argument fire_base_database", value=fire_base_database, expected_type=type_hints["fire_base_database"])
            check_type(argname="argument fire_base_hosting", value=fire_base_hosting, expected_type=type_hints["fire_base_hosting"])
            check_type(argname="argument fire_base_storage", value=fire_base_storage, expected_type=type_hints["fire_base_storage"])
            check_type(argname="argument fire_store", value=fire_store, expected_type=type_hints["fire_store"])
            check_type(argname="argument functions", value=functions, expected_type=type_hints["functions"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument interconnect", value=interconnect, expected_type=type_hints["interconnect"])
            check_type(argname="argument kubernetes", value=kubernetes, expected_type=type_hints["kubernetes"])
            check_type(argname="argument load_balancing", value=load_balancing, expected_type=type_hints["load_balancing"])
            check_type(argname="argument mem_cache", value=mem_cache, expected_type=type_hints["mem_cache"])
            check_type(argname="argument pub_sub", value=pub_sub, expected_type=type_hints["pub_sub"])
            check_type(argname="argument redis", value=redis, expected_type=type_hints["redis"])
            check_type(argname="argument router", value=router, expected_type=type_hints["router"])
            check_type(argname="argument run", value=run, expected_type=type_hints["run"])
            check_type(argname="argument spanner", value=spanner, expected_type=type_hints["spanner"])
            check_type(argname="argument sql", value=sql, expected_type=type_hints["sql"])
            check_type(argname="argument storage", value=storage, expected_type=type_hints["storage"])
            check_type(argname="argument virtual_machines", value=virtual_machines, expected_type=type_hints["virtual_machines"])
            check_type(argname="argument vpc_access", value=vpc_access, expected_type=type_hints["vpc_access"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "linked_account_id": linked_account_id,
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
        if account_id is not None:
            self._values["account_id"] = account_id
        if alloy_db is not None:
            self._values["alloy_db"] = alloy_db
        if app_engine is not None:
            self._values["app_engine"] = app_engine
        if big_query is not None:
            self._values["big_query"] = big_query
        if big_table is not None:
            self._values["big_table"] = big_table
        if composer is not None:
            self._values["composer"] = composer
        if data_flow is not None:
            self._values["data_flow"] = data_flow
        if data_proc is not None:
            self._values["data_proc"] = data_proc
        if data_store is not None:
            self._values["data_store"] = data_store
        if fire_base_database is not None:
            self._values["fire_base_database"] = fire_base_database
        if fire_base_hosting is not None:
            self._values["fire_base_hosting"] = fire_base_hosting
        if fire_base_storage is not None:
            self._values["fire_base_storage"] = fire_base_storage
        if fire_store is not None:
            self._values["fire_store"] = fire_store
        if functions is not None:
            self._values["functions"] = functions
        if id is not None:
            self._values["id"] = id
        if interconnect is not None:
            self._values["interconnect"] = interconnect
        if kubernetes is not None:
            self._values["kubernetes"] = kubernetes
        if load_balancing is not None:
            self._values["load_balancing"] = load_balancing
        if mem_cache is not None:
            self._values["mem_cache"] = mem_cache
        if pub_sub is not None:
            self._values["pub_sub"] = pub_sub
        if redis is not None:
            self._values["redis"] = redis
        if router is not None:
            self._values["router"] = router
        if run is not None:
            self._values["run"] = run
        if spanner is not None:
            self._values["spanner"] = spanner
        if sql is not None:
            self._values["sql"] = sql
        if storage is not None:
            self._values["storage"] = storage
        if virtual_machines is not None:
            self._values["virtual_machines"] = virtual_machines
        if vpc_access is not None:
            self._values["vpc_access"] = vpc_access

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
    def linked_account_id(self) -> jsii.Number:
        '''Id of the linked gcp account in New Relic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#linked_account_id CloudGcpIntegrations#linked_account_id}
        '''
        result = self._values.get("linked_account_id")
        assert result is not None, "Required property 'linked_account_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''ID of the newrelic account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#account_id CloudGcpIntegrations#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def alloy_db(self) -> typing.Optional[CloudGcpIntegrationsAlloyDb]:
        '''alloy_db block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#alloy_db CloudGcpIntegrations#alloy_db}
        '''
        result = self._values.get("alloy_db")
        return typing.cast(typing.Optional[CloudGcpIntegrationsAlloyDb], result)

    @builtins.property
    def app_engine(self) -> typing.Optional[CloudGcpIntegrationsAppEngine]:
        '''app_engine block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#app_engine CloudGcpIntegrations#app_engine}
        '''
        result = self._values.get("app_engine")
        return typing.cast(typing.Optional[CloudGcpIntegrationsAppEngine], result)

    @builtins.property
    def big_query(self) -> typing.Optional[CloudGcpIntegrationsBigQuery]:
        '''big_query block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#big_query CloudGcpIntegrations#big_query}
        '''
        result = self._values.get("big_query")
        return typing.cast(typing.Optional[CloudGcpIntegrationsBigQuery], result)

    @builtins.property
    def big_table(self) -> typing.Optional[CloudGcpIntegrationsBigTable]:
        '''big_table block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#big_table CloudGcpIntegrations#big_table}
        '''
        result = self._values.get("big_table")
        return typing.cast(typing.Optional[CloudGcpIntegrationsBigTable], result)

    @builtins.property
    def composer(self) -> typing.Optional[CloudGcpIntegrationsComposer]:
        '''composer block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#composer CloudGcpIntegrations#composer}
        '''
        result = self._values.get("composer")
        return typing.cast(typing.Optional[CloudGcpIntegrationsComposer], result)

    @builtins.property
    def data_flow(self) -> typing.Optional["CloudGcpIntegrationsDataFlow"]:
        '''data_flow block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#data_flow CloudGcpIntegrations#data_flow}
        '''
        result = self._values.get("data_flow")
        return typing.cast(typing.Optional["CloudGcpIntegrationsDataFlow"], result)

    @builtins.property
    def data_proc(self) -> typing.Optional["CloudGcpIntegrationsDataProc"]:
        '''data_proc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#data_proc CloudGcpIntegrations#data_proc}
        '''
        result = self._values.get("data_proc")
        return typing.cast(typing.Optional["CloudGcpIntegrationsDataProc"], result)

    @builtins.property
    def data_store(self) -> typing.Optional["CloudGcpIntegrationsDataStore"]:
        '''data_store block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#data_store CloudGcpIntegrations#data_store}
        '''
        result = self._values.get("data_store")
        return typing.cast(typing.Optional["CloudGcpIntegrationsDataStore"], result)

    @builtins.property
    def fire_base_database(
        self,
    ) -> typing.Optional["CloudGcpIntegrationsFireBaseDatabase"]:
        '''fire_base_database block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#fire_base_database CloudGcpIntegrations#fire_base_database}
        '''
        result = self._values.get("fire_base_database")
        return typing.cast(typing.Optional["CloudGcpIntegrationsFireBaseDatabase"], result)

    @builtins.property
    def fire_base_hosting(
        self,
    ) -> typing.Optional["CloudGcpIntegrationsFireBaseHosting"]:
        '''fire_base_hosting block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#fire_base_hosting CloudGcpIntegrations#fire_base_hosting}
        '''
        result = self._values.get("fire_base_hosting")
        return typing.cast(typing.Optional["CloudGcpIntegrationsFireBaseHosting"], result)

    @builtins.property
    def fire_base_storage(
        self,
    ) -> typing.Optional["CloudGcpIntegrationsFireBaseStorage"]:
        '''fire_base_storage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#fire_base_storage CloudGcpIntegrations#fire_base_storage}
        '''
        result = self._values.get("fire_base_storage")
        return typing.cast(typing.Optional["CloudGcpIntegrationsFireBaseStorage"], result)

    @builtins.property
    def fire_store(self) -> typing.Optional["CloudGcpIntegrationsFireStore"]:
        '''fire_store block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#fire_store CloudGcpIntegrations#fire_store}
        '''
        result = self._values.get("fire_store")
        return typing.cast(typing.Optional["CloudGcpIntegrationsFireStore"], result)

    @builtins.property
    def functions(self) -> typing.Optional["CloudGcpIntegrationsFunctions"]:
        '''functions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#functions CloudGcpIntegrations#functions}
        '''
        result = self._values.get("functions")
        return typing.cast(typing.Optional["CloudGcpIntegrationsFunctions"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#id CloudGcpIntegrations#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def interconnect(self) -> typing.Optional["CloudGcpIntegrationsInterconnect"]:
        '''interconnect block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#interconnect CloudGcpIntegrations#interconnect}
        '''
        result = self._values.get("interconnect")
        return typing.cast(typing.Optional["CloudGcpIntegrationsInterconnect"], result)

    @builtins.property
    def kubernetes(self) -> typing.Optional["CloudGcpIntegrationsKubernetes"]:
        '''kubernetes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#kubernetes CloudGcpIntegrations#kubernetes}
        '''
        result = self._values.get("kubernetes")
        return typing.cast(typing.Optional["CloudGcpIntegrationsKubernetes"], result)

    @builtins.property
    def load_balancing(self) -> typing.Optional["CloudGcpIntegrationsLoadBalancing"]:
        '''load_balancing block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#load_balancing CloudGcpIntegrations#load_balancing}
        '''
        result = self._values.get("load_balancing")
        return typing.cast(typing.Optional["CloudGcpIntegrationsLoadBalancing"], result)

    @builtins.property
    def mem_cache(self) -> typing.Optional["CloudGcpIntegrationsMemCache"]:
        '''mem_cache block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#mem_cache CloudGcpIntegrations#mem_cache}
        '''
        result = self._values.get("mem_cache")
        return typing.cast(typing.Optional["CloudGcpIntegrationsMemCache"], result)

    @builtins.property
    def pub_sub(self) -> typing.Optional["CloudGcpIntegrationsPubSub"]:
        '''pub_sub block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#pub_sub CloudGcpIntegrations#pub_sub}
        '''
        result = self._values.get("pub_sub")
        return typing.cast(typing.Optional["CloudGcpIntegrationsPubSub"], result)

    @builtins.property
    def redis(self) -> typing.Optional["CloudGcpIntegrationsRedis"]:
        '''redis block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#redis CloudGcpIntegrations#redis}
        '''
        result = self._values.get("redis")
        return typing.cast(typing.Optional["CloudGcpIntegrationsRedis"], result)

    @builtins.property
    def router(self) -> typing.Optional["CloudGcpIntegrationsRouter"]:
        '''router block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#router CloudGcpIntegrations#router}
        '''
        result = self._values.get("router")
        return typing.cast(typing.Optional["CloudGcpIntegrationsRouter"], result)

    @builtins.property
    def run(self) -> typing.Optional["CloudGcpIntegrationsRun"]:
        '''run block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#run CloudGcpIntegrations#run}
        '''
        result = self._values.get("run")
        return typing.cast(typing.Optional["CloudGcpIntegrationsRun"], result)

    @builtins.property
    def spanner(self) -> typing.Optional["CloudGcpIntegrationsSpanner"]:
        '''spanner block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#spanner CloudGcpIntegrations#spanner}
        '''
        result = self._values.get("spanner")
        return typing.cast(typing.Optional["CloudGcpIntegrationsSpanner"], result)

    @builtins.property
    def sql(self) -> typing.Optional["CloudGcpIntegrationsSql"]:
        '''sql block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#sql CloudGcpIntegrations#sql}
        '''
        result = self._values.get("sql")
        return typing.cast(typing.Optional["CloudGcpIntegrationsSql"], result)

    @builtins.property
    def storage(self) -> typing.Optional["CloudGcpIntegrationsStorage"]:
        '''storage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#storage CloudGcpIntegrations#storage}
        '''
        result = self._values.get("storage")
        return typing.cast(typing.Optional["CloudGcpIntegrationsStorage"], result)

    @builtins.property
    def virtual_machines(
        self,
    ) -> typing.Optional["CloudGcpIntegrationsVirtualMachines"]:
        '''virtual_machines block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#virtual_machines CloudGcpIntegrations#virtual_machines}
        '''
        result = self._values.get("virtual_machines")
        return typing.cast(typing.Optional["CloudGcpIntegrationsVirtualMachines"], result)

    @builtins.property
    def vpc_access(self) -> typing.Optional["CloudGcpIntegrationsVpcAccess"]:
        '''vpc_access block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#vpc_access CloudGcpIntegrations#vpc_access}
        '''
        result = self._values.get("vpc_access")
        return typing.cast(typing.Optional["CloudGcpIntegrationsVpcAccess"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsDataFlow",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudGcpIntegrationsDataFlow:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2a205eb5535f848fb3fda204e53e84569374d6a8f3d3d4804238c26747151b5)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsDataFlow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsDataFlowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsDataFlowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb82233f7982c8af7b035b5336eacef48d826c01663e660eb9123012c52bac1e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e82b7e04d0d4ad68d291199acb55e22ead1a032e44651a86b104774b6dce6c2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsDataFlow]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsDataFlow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudGcpIntegrationsDataFlow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c55413c461ed1ee687cf4dc3410c56a1abaab5e86d064a882c188e831a23fd4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsDataProc",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudGcpIntegrationsDataProc:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__558f131bc2ac60ce78703d1e844e3667ddf48d0845d84b0621571f0da03c7c2e)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsDataProc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsDataProcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsDataProcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__459ebc39f31e078e0f8a991656c8d69a1ad04e4b6a1871bf55b86fcd1bc047b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e266ea1e1c52daad4ed7717e332e40d9645c57f8194b428716d3b4f702a4d244)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsDataProc]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsDataProc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudGcpIntegrationsDataProc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be62ace775283f7dae5db463846b2cf012ec71b5a1dcf8989b7250e915e1b385)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsDataStore",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudGcpIntegrationsDataStore:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70d42693ec17f4a8379deafdc3420f75398c92462205f3fb6a20c3d08eae87ee)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsDataStore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsDataStoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsDataStoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5e7370b62da347d96755db35a74a9e1c48598453c963fce8e2d5cd4708155cf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18b0f10ab9fbb0ac011fa17fe54213c8404e21384c0f6560cd3972a270fb87ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsDataStore]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsDataStore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudGcpIntegrationsDataStore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__217d2dd9e3c26ed0d72c4b3c4ed3904d646b12c88f01a24c0d05ad07a0085620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsFireBaseDatabase",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudGcpIntegrationsFireBaseDatabase:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc1b2e9c0565d60e3ef8aa1fdbf6912aa14f5a1d66d53015b37bf72bfcabcf27)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsFireBaseDatabase(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsFireBaseDatabaseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsFireBaseDatabaseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf9820d55d5206026a75c0e2aa1f1d517a9602b00267895d07fc2e46cc85b98b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bde6e3cdfcbb839c0c695cf773ad332185cf0f3fe89aba7b8635ae083c7b95ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsFireBaseDatabase]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsFireBaseDatabase], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudGcpIntegrationsFireBaseDatabase],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e03b648f9c0f4f29be7e489e483816611f67442f91761b66f3b41abae9eaf1f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsFireBaseHosting",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudGcpIntegrationsFireBaseHosting:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e3e6955fb34ddcd4322b8eb71f6224d4cd41781881a13bab107e23c5c9ce7d5)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsFireBaseHosting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsFireBaseHostingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsFireBaseHostingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__770aa8332a56acb0a52f9e9178fd812241210e021fcd519e12a26b482f129916)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8f904d48d58bbc3fd6ab8dffdc1c179918b91a9dedcded20a316cde0acb4517)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsFireBaseHosting]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsFireBaseHosting], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudGcpIntegrationsFireBaseHosting],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b8bd136960429e6762ddcbdcabd8534937ec462f544280845cb5d77cb9e3825)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsFireBaseStorage",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudGcpIntegrationsFireBaseStorage:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e1a7d4351d19c35fbe54083830d66a521505e0ecbbc103f61a9d9d7808958af)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsFireBaseStorage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsFireBaseStorageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsFireBaseStorageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46770c9ea0c7f6d19454ad0a2967fc224ca4d8e322e637039dfcd855b9beb4cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a36206e59ae4c54565acd81382fc93fddf1277c0ea9f07ce2df513dc9a66ff7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsFireBaseStorage]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsFireBaseStorage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudGcpIntegrationsFireBaseStorage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b735b1ec022001bc530827a0b54999d40f32d167a57d97d039c0829fe7f6fb75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsFireStore",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudGcpIntegrationsFireStore:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9efe044ac01df6349684fff02b8ecb32b46c319177f0eb40c1e4f8abecd77ec2)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsFireStore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsFireStoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsFireStoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72f4dcbc4d1bcfac66a95eb99adb1fc680c5074f012c2ed59c7be1980d83d895)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79da00435b019fcdfb9d68fd0f6b503446161924b7718d5a30289636b18ca56a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsFireStore]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsFireStore], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudGcpIntegrationsFireStore],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfd828c850944326ca49a9a48ef13f764277aec7d0fb17ef6abc9b5fbab600c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsFunctions",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudGcpIntegrationsFunctions:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b07a3feb3bfa10839401358984240212d225fa1143a079d6b3fbcbbafb7250c)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsFunctions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsFunctionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsFunctionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0822057f4c0ebbc7d126e6542a068fe97388a5014f1af0ebde49ed3123919b7d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__581ddbb164bffd0e7991f4681fe325146cb4b66ba4854c665b61cbcf39f0f263)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsFunctions]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsFunctions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudGcpIntegrationsFunctions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc921840eaedc9456bb5ba0d73ae5b1f92da040144dd9ea762df10aa720c3184)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsInterconnect",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudGcpIntegrationsInterconnect:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c356d8e5106cc683b54aa7915321e67ae24e505896915da4cbeb99308881ff21)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsInterconnect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsInterconnectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsInterconnectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9b1e8f36fcadf99c7f7331324f27c85132c59286e04f5a05b5ae466a9554bef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da4c6c08ad43d3b76a17cf7b4e9cced4fc706b5e2cab4905ac09e535be5f9a73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsInterconnect]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsInterconnect], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudGcpIntegrationsInterconnect],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7d8650a042929d0db18da212e1bd688e5dce228c21038ee45c0a59612bc4741)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsKubernetes",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudGcpIntegrationsKubernetes:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49ca22d9002c24400ac9073477a909a1bbfdffc79df9fd437e9b2ee320616837)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsKubernetes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsKubernetesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsKubernetesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8b1d8707984de0bbd59167cb2a3ab41a5cb14f94578d4a09cdf38e0ac1ea751)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3718cca4e554c268dbede755917a9741a31da8de8f0418066060c8763259fb7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsKubernetes]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsKubernetes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudGcpIntegrationsKubernetes],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8f2d0cdc38ea39e782dd951b10c20f004e3b080bd4b62e69423b4d83547bcbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsLoadBalancing",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudGcpIntegrationsLoadBalancing:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__078d955cba770a049a33d2f96f4d82b4a21df4e6b9cf2bfb4ce14d5079b7600f)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsLoadBalancing(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsLoadBalancingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsLoadBalancingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cf9539c2ab45b7039e1b68283b3fa7db273604056725283ff964dcdd66be957)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e38bcf59c0e99ff42381469ccc35cc9de38c7ab77fa960a56d46a094afc1adb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsLoadBalancing]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsLoadBalancing], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudGcpIntegrationsLoadBalancing],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3090586d79097ae19b10a23d512e0c9ad4f6fce336e0155fa05bd4cd3674898a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsMemCache",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudGcpIntegrationsMemCache:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fea9d58597b8642758814be0c4bf452ecd7747e7c3b74899e273079a19d003d)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsMemCache(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsMemCacheOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsMemCacheOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e953cea525e672de042f03017c08d8869d1222e9ce9e56840b9abfe728bc548)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b27348d23d439a167a7ee34b5373d7345d7115af79b4481bee7bf063f0819324)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsMemCache]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsMemCache], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudGcpIntegrationsMemCache],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86c292aba9e14a75ca0bbea744e0673cbbf8c7a378fd31fc0e1fd9db318b1a54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsPubSub",
    jsii_struct_bases=[],
    name_mapping={
        "fetch_tags": "fetchTags",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudGcpIntegrationsPubSub:
    def __init__(
        self,
        *,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fetch_tags: to fetch tags of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#fetch_tags CloudGcpIntegrations#fetch_tags}
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bac7aa9ef6b2390b8d43609dc10cebf7ddcdf9168f10ab65a7f3c2ada4ef9a0)
            check_type(argname="argument fetch_tags", value=fetch_tags, expected_type=type_hints["fetch_tags"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fetch_tags is not None:
            self._values["fetch_tags"] = fetch_tags
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''to fetch tags of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#fetch_tags CloudGcpIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsPubSub(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsPubSubOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsPubSubOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db63e282478ac5622e1c3da952584a7336a9924e6d3ddd759056c3c0ef795c75)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFetchTags")
    def reset_fetch_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchTags", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="fetchTagsInput")
    def fetch_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchTags")
    def fetch_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchTags"))

    @fetch_tags.setter
    def fetch_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c1d5c53f92faa91d38e622674e1211bf3460911d87fd29a128376ecc972a507)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__780e9695039e263c1586254114675cb1eac8162a00bff84f81ac84b6f6593eae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsPubSub]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsPubSub], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudGcpIntegrationsPubSub],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f069af64eeda9029536dc787cf0dd641fd4371096a43774f21952066d6df08f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsRedis",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudGcpIntegrationsRedis:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afe264d508a177c0bbc708f60b46d28236be2f0a728305071d123b86a48cb8d6)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsRedis(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsRedisOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsRedisOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02d537995221ae0e596d5a82bf0347af93b9901a443f9d965cef9548cac4935b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f00117c03fdb0d6277fc3399f0be1cb4fcd188fe764d2b701dfc09b278fdc41e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsRedis]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsRedis], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudGcpIntegrationsRedis]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4740c0cb79cfeb242586884fc50ec432185384e31d05c91d45190467b5aa90ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsRouter",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudGcpIntegrationsRouter:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1931376ed6c03c1f432616f0cafadd6e76cabcd037668cfaa44a6668dfa6e7eb)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsRouter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsRouterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsRouterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3373b63a6001b8cc57fed9afd7df4bf7f741d2e9a2a225539bcc4acacf039e05)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ad3e1190fa027de7b7da0935c8e953226dbd4c01947a807310dc3bca4ed7fbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsRouter]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsRouter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudGcpIntegrationsRouter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b444a340570dfb1685003b0e1a54503c0e783085673b0c012317a82d157ffdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsRun",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudGcpIntegrationsRun:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__463dc5c7c136ca81a9ad5d4e9f3efa411c2e42c36b873f8aab443c8cc9ae26fd)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsRun(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsRunOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsRunOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__83f69ec7d185452763048a78fdff88dcecdb92af4e1d6f308fa788e9eee1b98c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__049bad8c86ceddae4dd492d36683cc0755961b770b0c6695245a9556586aa1eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsRun]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsRun], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudGcpIntegrationsRun]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d3415b42535d747142b6b10070558195395a59311ab3b30c2191c814c4f8fcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsSpanner",
    jsii_struct_bases=[],
    name_mapping={
        "fetch_tags": "fetchTags",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudGcpIntegrationsSpanner:
    def __init__(
        self,
        *,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fetch_tags: to fetch tags of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#fetch_tags CloudGcpIntegrations#fetch_tags}
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be803fe9240d7942d7a817db83e21f4f12e2f2d62e76fe7bd03d347ce54ad867)
            check_type(argname="argument fetch_tags", value=fetch_tags, expected_type=type_hints["fetch_tags"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fetch_tags is not None:
            self._values["fetch_tags"] = fetch_tags
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''to fetch tags of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#fetch_tags CloudGcpIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsSpanner(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsSpannerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsSpannerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08a52879dac8ee63de351ed8a01bfce1485ff594dce256d0dded1e635f21eac1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFetchTags")
    def reset_fetch_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchTags", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="fetchTagsInput")
    def fetch_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchTags")
    def fetch_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchTags"))

    @fetch_tags.setter
    def fetch_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a29d3cd92386c943d53117c945471afc9b870f415c6e555dabd4787237dc7e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8791345e7f64488fb3baf03a2704fd9eb18ecb9a9ffdd9b54e40218cfface7e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsSpanner]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsSpanner], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudGcpIntegrationsSpanner],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11f4878e69e58bab09b08ea764f7c03604ccd39ffa07f10eda3d06f1fb502b37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsSql",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudGcpIntegrationsSql:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363f433efbd0731d27127e0d457936c2871c0d12594afb3703d9990695d7249d)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsSql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsSqlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsSqlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__63e23a08a78149971662faad6ea7aad7f84cbd8af47887d1e660c43ebe452bdb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31b2d3d5a93031a4fcb0baa02354e30bdf4c5ebef4db238c17a7bc4621f9d444)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsSql]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsSql], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudGcpIntegrationsSql]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db7fde04ed8f39a3f22832a71cb90407ae32a2f4e0a22fc8b92d0c60a9aa1f65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsStorage",
    jsii_struct_bases=[],
    name_mapping={
        "fetch_tags": "fetchTags",
        "metrics_polling_interval": "metricsPollingInterval",
    },
)
class CloudGcpIntegrationsStorage:
    def __init__(
        self,
        *,
        fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fetch_tags: to fetch tags of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#fetch_tags CloudGcpIntegrations#fetch_tags}
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__015efa5c6806c56f2562f1f18e47552ef5c40476107739b7fa54ba9cbae44ec8)
            check_type(argname="argument fetch_tags", value=fetch_tags, expected_type=type_hints["fetch_tags"])
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fetch_tags is not None:
            self._values["fetch_tags"] = fetch_tags
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def fetch_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''to fetch tags of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#fetch_tags CloudGcpIntegrations#fetch_tags}
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsStorage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsStorageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsStorageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27b9341fe9c091f1be3570da729e46589074ffbe23bf9173be0578d1e7cf45e2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFetchTags")
    def reset_fetch_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFetchTags", []))

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="fetchTagsInput")
    def fetch_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fetchTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="fetchTags")
    def fetch_tags(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fetchTags"))

    @fetch_tags.setter
    def fetch_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01948fa66cd1b73ab7b5637ef68bf0929c01c869e767008366cfc900bc88b920)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fetchTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ddfdfc395e5151b44a42116d62f459ccddc56e259263336ac498f5464600dbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsStorage]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsStorage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudGcpIntegrationsStorage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ec6e5d06be7aa114d24105ec3fada4261bbf9abdc39bd946f61d9a4c9169598)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsVirtualMachines",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudGcpIntegrationsVirtualMachines:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88c9b145cea9e52f1e04454f450750cc6d80916f2d9fa488d319b132378246f1)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsVirtualMachines(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsVirtualMachinesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsVirtualMachinesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3065adcff3c5376c1d2cc12019dca3242973f19de7a267c1d7561a38ebd0efa3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3da990bf4bfa1b0cbae9d3d85c91c1bf51c59d0a7b6cb03582fe47d780f31f1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsVirtualMachines]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsVirtualMachines], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudGcpIntegrationsVirtualMachines],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36d1402068d6f2bc69b7d783424f23af51c20dd480c5d4bdafcdb88365d5f5d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsVpcAccess",
    jsii_struct_bases=[],
    name_mapping={"metrics_polling_interval": "metricsPollingInterval"},
)
class CloudGcpIntegrationsVpcAccess:
    def __init__(
        self,
        *,
        metrics_polling_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metrics_polling_interval: the data polling interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__458f0f4c35b6b85b9b482dad21a1fc61a8bbfb006c9c75634bc5062b82699bb2)
            check_type(argname="argument metrics_polling_interval", value=metrics_polling_interval, expected_type=type_hints["metrics_polling_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metrics_polling_interval is not None:
            self._values["metrics_polling_interval"] = metrics_polling_interval

    @builtins.property
    def metrics_polling_interval(self) -> typing.Optional[jsii.Number]:
        '''the data polling interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/cloud_gcp_integrations#metrics_polling_interval CloudGcpIntegrations#metrics_polling_interval}
        '''
        result = self._values.get("metrics_polling_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudGcpIntegrationsVpcAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudGcpIntegrationsVpcAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.cloudGcpIntegrations.CloudGcpIntegrationsVpcAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b4c308db8965b009091f8f760caad1c33d8ed44b7e154df8e948d99b793688d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricsPollingInterval")
    def reset_metrics_polling_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricsPollingInterval", []))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingIntervalInput")
    def metrics_polling_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "metricsPollingIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsPollingInterval")
    def metrics_polling_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "metricsPollingInterval"))

    @metrics_polling_interval.setter
    def metrics_polling_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28081ad56134f8e268170a6257e365c13591060e3d7e8dc387da48cb1d76f9c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricsPollingInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudGcpIntegrationsVpcAccess]:
        return typing.cast(typing.Optional[CloudGcpIntegrationsVpcAccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudGcpIntegrationsVpcAccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29456f463ac1122bec5491a6f23e842771c5b6a9952e23608d9412d0dea0450c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CloudGcpIntegrations",
    "CloudGcpIntegrationsAlloyDb",
    "CloudGcpIntegrationsAlloyDbOutputReference",
    "CloudGcpIntegrationsAppEngine",
    "CloudGcpIntegrationsAppEngineOutputReference",
    "CloudGcpIntegrationsBigQuery",
    "CloudGcpIntegrationsBigQueryOutputReference",
    "CloudGcpIntegrationsBigTable",
    "CloudGcpIntegrationsBigTableOutputReference",
    "CloudGcpIntegrationsComposer",
    "CloudGcpIntegrationsComposerOutputReference",
    "CloudGcpIntegrationsConfig",
    "CloudGcpIntegrationsDataFlow",
    "CloudGcpIntegrationsDataFlowOutputReference",
    "CloudGcpIntegrationsDataProc",
    "CloudGcpIntegrationsDataProcOutputReference",
    "CloudGcpIntegrationsDataStore",
    "CloudGcpIntegrationsDataStoreOutputReference",
    "CloudGcpIntegrationsFireBaseDatabase",
    "CloudGcpIntegrationsFireBaseDatabaseOutputReference",
    "CloudGcpIntegrationsFireBaseHosting",
    "CloudGcpIntegrationsFireBaseHostingOutputReference",
    "CloudGcpIntegrationsFireBaseStorage",
    "CloudGcpIntegrationsFireBaseStorageOutputReference",
    "CloudGcpIntegrationsFireStore",
    "CloudGcpIntegrationsFireStoreOutputReference",
    "CloudGcpIntegrationsFunctions",
    "CloudGcpIntegrationsFunctionsOutputReference",
    "CloudGcpIntegrationsInterconnect",
    "CloudGcpIntegrationsInterconnectOutputReference",
    "CloudGcpIntegrationsKubernetes",
    "CloudGcpIntegrationsKubernetesOutputReference",
    "CloudGcpIntegrationsLoadBalancing",
    "CloudGcpIntegrationsLoadBalancingOutputReference",
    "CloudGcpIntegrationsMemCache",
    "CloudGcpIntegrationsMemCacheOutputReference",
    "CloudGcpIntegrationsPubSub",
    "CloudGcpIntegrationsPubSubOutputReference",
    "CloudGcpIntegrationsRedis",
    "CloudGcpIntegrationsRedisOutputReference",
    "CloudGcpIntegrationsRouter",
    "CloudGcpIntegrationsRouterOutputReference",
    "CloudGcpIntegrationsRun",
    "CloudGcpIntegrationsRunOutputReference",
    "CloudGcpIntegrationsSpanner",
    "CloudGcpIntegrationsSpannerOutputReference",
    "CloudGcpIntegrationsSql",
    "CloudGcpIntegrationsSqlOutputReference",
    "CloudGcpIntegrationsStorage",
    "CloudGcpIntegrationsStorageOutputReference",
    "CloudGcpIntegrationsVirtualMachines",
    "CloudGcpIntegrationsVirtualMachinesOutputReference",
    "CloudGcpIntegrationsVpcAccess",
    "CloudGcpIntegrationsVpcAccessOutputReference",
]

publication.publish()

def _typecheckingstub__33cf7b4320a550d0b8747b67bd6309347e9661e4592c634f2a6c98923ce6ef57(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    linked_account_id: jsii.Number,
    account_id: typing.Optional[jsii.Number] = None,
    alloy_db: typing.Optional[typing.Union[CloudGcpIntegrationsAlloyDb, typing.Dict[builtins.str, typing.Any]]] = None,
    app_engine: typing.Optional[typing.Union[CloudGcpIntegrationsAppEngine, typing.Dict[builtins.str, typing.Any]]] = None,
    big_query: typing.Optional[typing.Union[CloudGcpIntegrationsBigQuery, typing.Dict[builtins.str, typing.Any]]] = None,
    big_table: typing.Optional[typing.Union[CloudGcpIntegrationsBigTable, typing.Dict[builtins.str, typing.Any]]] = None,
    composer: typing.Optional[typing.Union[CloudGcpIntegrationsComposer, typing.Dict[builtins.str, typing.Any]]] = None,
    data_flow: typing.Optional[typing.Union[CloudGcpIntegrationsDataFlow, typing.Dict[builtins.str, typing.Any]]] = None,
    data_proc: typing.Optional[typing.Union[CloudGcpIntegrationsDataProc, typing.Dict[builtins.str, typing.Any]]] = None,
    data_store: typing.Optional[typing.Union[CloudGcpIntegrationsDataStore, typing.Dict[builtins.str, typing.Any]]] = None,
    fire_base_database: typing.Optional[typing.Union[CloudGcpIntegrationsFireBaseDatabase, typing.Dict[builtins.str, typing.Any]]] = None,
    fire_base_hosting: typing.Optional[typing.Union[CloudGcpIntegrationsFireBaseHosting, typing.Dict[builtins.str, typing.Any]]] = None,
    fire_base_storage: typing.Optional[typing.Union[CloudGcpIntegrationsFireBaseStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    fire_store: typing.Optional[typing.Union[CloudGcpIntegrationsFireStore, typing.Dict[builtins.str, typing.Any]]] = None,
    functions: typing.Optional[typing.Union[CloudGcpIntegrationsFunctions, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    interconnect: typing.Optional[typing.Union[CloudGcpIntegrationsInterconnect, typing.Dict[builtins.str, typing.Any]]] = None,
    kubernetes: typing.Optional[typing.Union[CloudGcpIntegrationsKubernetes, typing.Dict[builtins.str, typing.Any]]] = None,
    load_balancing: typing.Optional[typing.Union[CloudGcpIntegrationsLoadBalancing, typing.Dict[builtins.str, typing.Any]]] = None,
    mem_cache: typing.Optional[typing.Union[CloudGcpIntegrationsMemCache, typing.Dict[builtins.str, typing.Any]]] = None,
    pub_sub: typing.Optional[typing.Union[CloudGcpIntegrationsPubSub, typing.Dict[builtins.str, typing.Any]]] = None,
    redis: typing.Optional[typing.Union[CloudGcpIntegrationsRedis, typing.Dict[builtins.str, typing.Any]]] = None,
    router: typing.Optional[typing.Union[CloudGcpIntegrationsRouter, typing.Dict[builtins.str, typing.Any]]] = None,
    run: typing.Optional[typing.Union[CloudGcpIntegrationsRun, typing.Dict[builtins.str, typing.Any]]] = None,
    spanner: typing.Optional[typing.Union[CloudGcpIntegrationsSpanner, typing.Dict[builtins.str, typing.Any]]] = None,
    sql: typing.Optional[typing.Union[CloudGcpIntegrationsSql, typing.Dict[builtins.str, typing.Any]]] = None,
    storage: typing.Optional[typing.Union[CloudGcpIntegrationsStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_machines: typing.Optional[typing.Union[CloudGcpIntegrationsVirtualMachines, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_access: typing.Optional[typing.Union[CloudGcpIntegrationsVpcAccess, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d447a75ff07da8461de16a8e995d4eefecc1acbcf384f87a7f61499bf74068c8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efb17273c3fbf33f0e0609e23ca23b31c5b32738a1d8b2b6da8a7d06b98302a1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7612724444e8d28a8a047dea1cc60ad7ba5efd08acd1c43430bee9c20c70e948(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f405e01509f6be3df35158b788d901dedb3966463a614901cea7783194002e99(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29355de8dcddfb1ccde0ee296b6c01ed7c8bb2d347bd981860f69d6837e8bf49(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89eb41116e169274623cb2a3fe7c75889474cd876d4cb4478f73f30c5e9711c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e092d8e4ece82f910d955afbd1cc28fd7f4386a93aa2519be40f770d847c0c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b682132cb22a42ef53f5df73eb74283f27df5ebc1d42882eca6122d09263323(
    value: typing.Optional[CloudGcpIntegrationsAlloyDb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e0ea11eb547c1edb6235920c85306b5efb55576b0996e0804a953f588a3091c(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a81041e761f3ef997022d0857c5f7cbb087b0d3c7e3d85ff7a0735fdcb3f5f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f89cdcae0016a3ddfc9b1e25d81314e5238ab53c70f41880503cedb69d452da(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2c7e5d284b5ac99f4ee060e916e7063ea664c53d6427d4bda5a815e35801939(
    value: typing.Optional[CloudGcpIntegrationsAppEngine],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__617061e9fe40845851969430d28b73acc3f96927f1ddc19909745b5e85a2c5dc(
    *,
    fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__629e2cd1c26a6dc4423c7ec01c00e05d19ef5a4891f4bf02dbdf62cd3ab37064(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__934a776a9743e1bf514f49c415a095771d8b3bd7a8bc61d4676def55cdbd3f1a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed50608b40c33129367e9f7eae7526d3a4ffa6e91047f053b61e3c2a71199b3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f690719ad14678b3251cbbab8f7bc87405388a47c4e168e6155d6c56fe8aed37(
    value: typing.Optional[CloudGcpIntegrationsBigQuery],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe9da90aa8dd0ae0b9bac48957979fc030f02308d0840af73acbafa2ab8522aa(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__489f16073fa3a8949cb26acb09c88106fb29514e983eee5ac09c732a37e635f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b2852ff7c7db3dfa17efb03b250722fab788b7ef8168e22bd2187141b96c7f8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc6557653a3c54ddde560b23eaa19680214c572e4b6495bd499b0b5b25fca3fd(
    value: typing.Optional[CloudGcpIntegrationsBigTable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbf52cdfc38d910cf57ccb0e9c180cca525b94d5fb758cc9dec514f406740240(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04b5a7d1231e2571095700053fc1d4c745c9680eba2207c748d4c03e24e4d8fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d1a5262362c2ec9745f38a66c861d9381b4385502f2819c929315fbabc20f58(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1e1859ec6b12748859d2eaf9bdfb30186a07d75c75994d1af620fe817bad9e0(
    value: typing.Optional[CloudGcpIntegrationsComposer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e8e342b2eb95e9d0b60dc1d58206e4733dcef22cc0f55837cebc900a39aa864(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    linked_account_id: jsii.Number,
    account_id: typing.Optional[jsii.Number] = None,
    alloy_db: typing.Optional[typing.Union[CloudGcpIntegrationsAlloyDb, typing.Dict[builtins.str, typing.Any]]] = None,
    app_engine: typing.Optional[typing.Union[CloudGcpIntegrationsAppEngine, typing.Dict[builtins.str, typing.Any]]] = None,
    big_query: typing.Optional[typing.Union[CloudGcpIntegrationsBigQuery, typing.Dict[builtins.str, typing.Any]]] = None,
    big_table: typing.Optional[typing.Union[CloudGcpIntegrationsBigTable, typing.Dict[builtins.str, typing.Any]]] = None,
    composer: typing.Optional[typing.Union[CloudGcpIntegrationsComposer, typing.Dict[builtins.str, typing.Any]]] = None,
    data_flow: typing.Optional[typing.Union[CloudGcpIntegrationsDataFlow, typing.Dict[builtins.str, typing.Any]]] = None,
    data_proc: typing.Optional[typing.Union[CloudGcpIntegrationsDataProc, typing.Dict[builtins.str, typing.Any]]] = None,
    data_store: typing.Optional[typing.Union[CloudGcpIntegrationsDataStore, typing.Dict[builtins.str, typing.Any]]] = None,
    fire_base_database: typing.Optional[typing.Union[CloudGcpIntegrationsFireBaseDatabase, typing.Dict[builtins.str, typing.Any]]] = None,
    fire_base_hosting: typing.Optional[typing.Union[CloudGcpIntegrationsFireBaseHosting, typing.Dict[builtins.str, typing.Any]]] = None,
    fire_base_storage: typing.Optional[typing.Union[CloudGcpIntegrationsFireBaseStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    fire_store: typing.Optional[typing.Union[CloudGcpIntegrationsFireStore, typing.Dict[builtins.str, typing.Any]]] = None,
    functions: typing.Optional[typing.Union[CloudGcpIntegrationsFunctions, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    interconnect: typing.Optional[typing.Union[CloudGcpIntegrationsInterconnect, typing.Dict[builtins.str, typing.Any]]] = None,
    kubernetes: typing.Optional[typing.Union[CloudGcpIntegrationsKubernetes, typing.Dict[builtins.str, typing.Any]]] = None,
    load_balancing: typing.Optional[typing.Union[CloudGcpIntegrationsLoadBalancing, typing.Dict[builtins.str, typing.Any]]] = None,
    mem_cache: typing.Optional[typing.Union[CloudGcpIntegrationsMemCache, typing.Dict[builtins.str, typing.Any]]] = None,
    pub_sub: typing.Optional[typing.Union[CloudGcpIntegrationsPubSub, typing.Dict[builtins.str, typing.Any]]] = None,
    redis: typing.Optional[typing.Union[CloudGcpIntegrationsRedis, typing.Dict[builtins.str, typing.Any]]] = None,
    router: typing.Optional[typing.Union[CloudGcpIntegrationsRouter, typing.Dict[builtins.str, typing.Any]]] = None,
    run: typing.Optional[typing.Union[CloudGcpIntegrationsRun, typing.Dict[builtins.str, typing.Any]]] = None,
    spanner: typing.Optional[typing.Union[CloudGcpIntegrationsSpanner, typing.Dict[builtins.str, typing.Any]]] = None,
    sql: typing.Optional[typing.Union[CloudGcpIntegrationsSql, typing.Dict[builtins.str, typing.Any]]] = None,
    storage: typing.Optional[typing.Union[CloudGcpIntegrationsStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_machines: typing.Optional[typing.Union[CloudGcpIntegrationsVirtualMachines, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_access: typing.Optional[typing.Union[CloudGcpIntegrationsVpcAccess, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2a205eb5535f848fb3fda204e53e84569374d6a8f3d3d4804238c26747151b5(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb82233f7982c8af7b035b5336eacef48d826c01663e660eb9123012c52bac1e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e82b7e04d0d4ad68d291199acb55e22ead1a032e44651a86b104774b6dce6c2d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55413c461ed1ee687cf4dc3410c56a1abaab5e86d064a882c188e831a23fd4a(
    value: typing.Optional[CloudGcpIntegrationsDataFlow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__558f131bc2ac60ce78703d1e844e3667ddf48d0845d84b0621571f0da03c7c2e(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__459ebc39f31e078e0f8a991656c8d69a1ad04e4b6a1871bf55b86fcd1bc047b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e266ea1e1c52daad4ed7717e332e40d9645c57f8194b428716d3b4f702a4d244(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be62ace775283f7dae5db463846b2cf012ec71b5a1dcf8989b7250e915e1b385(
    value: typing.Optional[CloudGcpIntegrationsDataProc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70d42693ec17f4a8379deafdc3420f75398c92462205f3fb6a20c3d08eae87ee(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5e7370b62da347d96755db35a74a9e1c48598453c963fce8e2d5cd4708155cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18b0f10ab9fbb0ac011fa17fe54213c8404e21384c0f6560cd3972a270fb87ae(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__217d2dd9e3c26ed0d72c4b3c4ed3904d646b12c88f01a24c0d05ad07a0085620(
    value: typing.Optional[CloudGcpIntegrationsDataStore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc1b2e9c0565d60e3ef8aa1fdbf6912aa14f5a1d66d53015b37bf72bfcabcf27(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf9820d55d5206026a75c0e2aa1f1d517a9602b00267895d07fc2e46cc85b98b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bde6e3cdfcbb839c0c695cf773ad332185cf0f3fe89aba7b8635ae083c7b95ae(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e03b648f9c0f4f29be7e489e483816611f67442f91761b66f3b41abae9eaf1f8(
    value: typing.Optional[CloudGcpIntegrationsFireBaseDatabase],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e3e6955fb34ddcd4322b8eb71f6224d4cd41781881a13bab107e23c5c9ce7d5(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__770aa8332a56acb0a52f9e9178fd812241210e021fcd519e12a26b482f129916(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f904d48d58bbc3fd6ab8dffdc1c179918b91a9dedcded20a316cde0acb4517(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b8bd136960429e6762ddcbdcabd8534937ec462f544280845cb5d77cb9e3825(
    value: typing.Optional[CloudGcpIntegrationsFireBaseHosting],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e1a7d4351d19c35fbe54083830d66a521505e0ecbbc103f61a9d9d7808958af(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46770c9ea0c7f6d19454ad0a2967fc224ca4d8e322e637039dfcd855b9beb4cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a36206e59ae4c54565acd81382fc93fddf1277c0ea9f07ce2df513dc9a66ff7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b735b1ec022001bc530827a0b54999d40f32d167a57d97d039c0829fe7f6fb75(
    value: typing.Optional[CloudGcpIntegrationsFireBaseStorage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9efe044ac01df6349684fff02b8ecb32b46c319177f0eb40c1e4f8abecd77ec2(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72f4dcbc4d1bcfac66a95eb99adb1fc680c5074f012c2ed59c7be1980d83d895(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79da00435b019fcdfb9d68fd0f6b503446161924b7718d5a30289636b18ca56a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfd828c850944326ca49a9a48ef13f764277aec7d0fb17ef6abc9b5fbab600c3(
    value: typing.Optional[CloudGcpIntegrationsFireStore],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b07a3feb3bfa10839401358984240212d225fa1143a079d6b3fbcbbafb7250c(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0822057f4c0ebbc7d126e6542a068fe97388a5014f1af0ebde49ed3123919b7d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__581ddbb164bffd0e7991f4681fe325146cb4b66ba4854c665b61cbcf39f0f263(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc921840eaedc9456bb5ba0d73ae5b1f92da040144dd9ea762df10aa720c3184(
    value: typing.Optional[CloudGcpIntegrationsFunctions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c356d8e5106cc683b54aa7915321e67ae24e505896915da4cbeb99308881ff21(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9b1e8f36fcadf99c7f7331324f27c85132c59286e04f5a05b5ae466a9554bef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da4c6c08ad43d3b76a17cf7b4e9cced4fc706b5e2cab4905ac09e535be5f9a73(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d8650a042929d0db18da212e1bd688e5dce228c21038ee45c0a59612bc4741(
    value: typing.Optional[CloudGcpIntegrationsInterconnect],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49ca22d9002c24400ac9073477a909a1bbfdffc79df9fd437e9b2ee320616837(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8b1d8707984de0bbd59167cb2a3ab41a5cb14f94578d4a09cdf38e0ac1ea751(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3718cca4e554c268dbede755917a9741a31da8de8f0418066060c8763259fb7b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8f2d0cdc38ea39e782dd951b10c20f004e3b080bd4b62e69423b4d83547bcbb(
    value: typing.Optional[CloudGcpIntegrationsKubernetes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__078d955cba770a049a33d2f96f4d82b4a21df4e6b9cf2bfb4ce14d5079b7600f(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cf9539c2ab45b7039e1b68283b3fa7db273604056725283ff964dcdd66be957(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e38bcf59c0e99ff42381469ccc35cc9de38c7ab77fa960a56d46a094afc1adb1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3090586d79097ae19b10a23d512e0c9ad4f6fce336e0155fa05bd4cd3674898a(
    value: typing.Optional[CloudGcpIntegrationsLoadBalancing],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fea9d58597b8642758814be0c4bf452ecd7747e7c3b74899e273079a19d003d(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e953cea525e672de042f03017c08d8869d1222e9ce9e56840b9abfe728bc548(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b27348d23d439a167a7ee34b5373d7345d7115af79b4481bee7bf063f0819324(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86c292aba9e14a75ca0bbea744e0673cbbf8c7a378fd31fc0e1fd9db318b1a54(
    value: typing.Optional[CloudGcpIntegrationsMemCache],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bac7aa9ef6b2390b8d43609dc10cebf7ddcdf9168f10ab65a7f3c2ada4ef9a0(
    *,
    fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db63e282478ac5622e1c3da952584a7336a9924e6d3ddd759056c3c0ef795c75(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c1d5c53f92faa91d38e622674e1211bf3460911d87fd29a128376ecc972a507(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__780e9695039e263c1586254114675cb1eac8162a00bff84f81ac84b6f6593eae(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f069af64eeda9029536dc787cf0dd641fd4371096a43774f21952066d6df08f8(
    value: typing.Optional[CloudGcpIntegrationsPubSub],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afe264d508a177c0bbc708f60b46d28236be2f0a728305071d123b86a48cb8d6(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02d537995221ae0e596d5a82bf0347af93b9901a443f9d965cef9548cac4935b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f00117c03fdb0d6277fc3399f0be1cb4fcd188fe764d2b701dfc09b278fdc41e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4740c0cb79cfeb242586884fc50ec432185384e31d05c91d45190467b5aa90ca(
    value: typing.Optional[CloudGcpIntegrationsRedis],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1931376ed6c03c1f432616f0cafadd6e76cabcd037668cfaa44a6668dfa6e7eb(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3373b63a6001b8cc57fed9afd7df4bf7f741d2e9a2a225539bcc4acacf039e05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ad3e1190fa027de7b7da0935c8e953226dbd4c01947a807310dc3bca4ed7fbf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b444a340570dfb1685003b0e1a54503c0e783085673b0c012317a82d157ffdd(
    value: typing.Optional[CloudGcpIntegrationsRouter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__463dc5c7c136ca81a9ad5d4e9f3efa411c2e42c36b873f8aab443c8cc9ae26fd(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83f69ec7d185452763048a78fdff88dcecdb92af4e1d6f308fa788e9eee1b98c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__049bad8c86ceddae4dd492d36683cc0755961b770b0c6695245a9556586aa1eb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d3415b42535d747142b6b10070558195395a59311ab3b30c2191c814c4f8fcd(
    value: typing.Optional[CloudGcpIntegrationsRun],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be803fe9240d7942d7a817db83e21f4f12e2f2d62e76fe7bd03d347ce54ad867(
    *,
    fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08a52879dac8ee63de351ed8a01bfce1485ff594dce256d0dded1e635f21eac1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a29d3cd92386c943d53117c945471afc9b870f415c6e555dabd4787237dc7e8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8791345e7f64488fb3baf03a2704fd9eb18ecb9a9ffdd9b54e40218cfface7e8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f4878e69e58bab09b08ea764f7c03604ccd39ffa07f10eda3d06f1fb502b37(
    value: typing.Optional[CloudGcpIntegrationsSpanner],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363f433efbd0731d27127e0d457936c2871c0d12594afb3703d9990695d7249d(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63e23a08a78149971662faad6ea7aad7f84cbd8af47887d1e660c43ebe452bdb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31b2d3d5a93031a4fcb0baa02354e30bdf4c5ebef4db238c17a7bc4621f9d444(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db7fde04ed8f39a3f22832a71cb90407ae32a2f4e0a22fc8b92d0c60a9aa1f65(
    value: typing.Optional[CloudGcpIntegrationsSql],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015efa5c6806c56f2562f1f18e47552ef5c40476107739b7fa54ba9cbae44ec8(
    *,
    fetch_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b9341fe9c091f1be3570da729e46589074ffbe23bf9173be0578d1e7cf45e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01948fa66cd1b73ab7b5637ef68bf0929c01c869e767008366cfc900bc88b920(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ddfdfc395e5151b44a42116d62f459ccddc56e259263336ac498f5464600dbe(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ec6e5d06be7aa114d24105ec3fada4261bbf9abdc39bd946f61d9a4c9169598(
    value: typing.Optional[CloudGcpIntegrationsStorage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88c9b145cea9e52f1e04454f450750cc6d80916f2d9fa488d319b132378246f1(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3065adcff3c5376c1d2cc12019dca3242973f19de7a267c1d7561a38ebd0efa3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da990bf4bfa1b0cbae9d3d85c91c1bf51c59d0a7b6cb03582fe47d780f31f1d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36d1402068d6f2bc69b7d783424f23af51c20dd480c5d4bdafcdb88365d5f5d6(
    value: typing.Optional[CloudGcpIntegrationsVirtualMachines],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__458f0f4c35b6b85b9b482dad21a1fc61a8bbfb006c9c75634bc5062b82699bb2(
    *,
    metrics_polling_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b4c308db8965b009091f8f760caad1c33d8ed44b7e154df8e948d99b793688d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28081ad56134f8e268170a6257e365c13591060e3d7e8dc387da48cb1d76f9c4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29456f463ac1122bec5491a6f23e842771c5b6a9952e23608d9412d0dea0450c(
    value: typing.Optional[CloudGcpIntegrationsVpcAccess],
) -> None:
    """Type checking stubs"""
    pass
