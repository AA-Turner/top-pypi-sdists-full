# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

from typing import List
import logging
import time

from .anzo_client import AnzoClient
from .quad_store import QuadStore, Quad
from .query_result import QueryResult
from .uris import TYPE_PRED, ALL_NAMED_GRAPHS_URI


logger = logging.getLogger(__name__)


class GraphmartManager:
    """Class for managing the state of an Anzo Graphmart

    Attributes:
        anzo_client: An AnzoClient object pointing to the Anzo
            with the Graphmart
        graphmart_uri: URI of the Graphmart to manage

    Usage:
        from pyanzo import AnzoClient, GraphmartManager
        anzo_client = AnzoClient("localhost", "8443", "
        graphmart_uri = "http://cambridgesemantics.com/graphmart/123"
        graphmart_manager = GraphmartManager(anzo_client, graphmart_uri)
        graphmart_manager.activate()
    """

    ACTIVATION_URI = "http://cambridgesemantics.com/semanticServices/gqe#deployGraphmart"  # noqa
    DYNAMIC_ACTIVATION_URI = "http://cambridgesemantics.com/semanticServices/Cloud/SpinupWorkflowService#startWorkflow" # noqa
    REFRESH_URI = "http://cambridgesemantics.com/semanticServices/gqe#refreshGraphmart"  # noqa
    RELOAD_URI = "http://cambridgesemantics.com/semanticServices/gqe#reloadGraphmart"  # noqa
    START_WORKFLOW_URI = "http://cambridgesemantics.com/semanticServices/Cloud/TeardownWorkflowService#startWorkflow"  # noqa
    SUCCESS_PREDICATE = "http://cambridgesemantics.com/ontologies/Graphmarts#success"  # noqa

    def __init__(self, anzo_client: AnzoClient, graphmart_uri: str):
        """Constructs a GraphmartManager for managing the state of a Graphmart

        Args:
            anzo_client: An AnzoClient object used for interacting with an Anzo
                server.
            graphmart_uri: The URI of the graphmart. It's assumed that the
                Graphmart is on the server underlying the anzo client object.

        Returns:
            A GraphmartManager object
        """
        self.anzo_client = anzo_client
        self.graphmart_uri = graphmart_uri
        self.sleep_time = 1

    def query(self, query_string: str = "", query_file: str = "",
              data_layers: List[str] = None) -> QueryResult:
        """Queries the Graphmart

        Either query_string or query_file must be provided but not both.

        If no data layers are provided, then all data layers are queried.
        """

        return self.anzo_client.query_graphmart(
            self.graphmart_uri, query_string=query_string,
            query_file=query_file, data_layers=data_layers
        )

    def deactivate(self) -> str:
        """Deactivates the Graphmart

        It is recommended to confirm that the Graphmart is offline by calling
        GraphmartManager.is_graphmart_online after this method completes.
        """

        request = self._build_deactivate_request()

        # Don't check the response because it doesn't contain information.
        # It's best to check if the deactivation failed by
        # calling self.is_graphmart_online

        response = self.anzo_client.execute_semantic_service(
            self.START_WORKFLOW_URI, request
        )
        # sleep one second to let the deactivate propagate
        time.sleep(self.sleep_time)
        return response.to_trig_string()

    def dynamic_activate(self, azg_launch_config: str = "", azg_version:str = "", azg_size: str = "") -> str:
        """Activates the Graphmart and spins up a k8s configured anzograph cluster 
        based on the parameters provided. All parameters are technically optional, but will most likely fail if not provided.
        
        This will silently fail if the launch config, azg version or azg size specified are not valid values.
        Args:
            azg_launch_config (required): The launch configuration containing the hardware specification of the virtual anzograph cluster to be deployed.
            azg_version (required): The version of the anzograph cluster to be deployed
            azg_size (required): The size of the anzograph node pool

        """
        request = self._build_dynamic_activate_request(azg_launch_config, azg_version, azg_size)

        response = self.anzo_client.execute_semantic_service(
             self.DYNAMIC_ACTIVATION_URI, request
        )
        time.sleep(self.sleep_time)  # sleep to let the activate propagate
        return response.to_trig_string()

        
        #
    def activate(self, azg_uri: str = "") -> str:
        """Activates the Graphmart

        If there are multiple AnzoGraph datasources and an
        AnzoGraph URI is not specified, then an arbitrary AnzoGraph
        datasource will be used (this is Anzo behavior,
        not GraphmartManager behavior).

        Note that layers can fail to load and a runtime error won't
        be raised.

        It is recommended to confirm that the Graphmart is online
        and that the expected layers are online after activating the Graphmart.

        If the activate call fails, a runtime error will be raised.

        In more detail:
        1. The semantic service request will internally fail if the
           graph fails to activate
        2. This results in a 500 error being returned from the AnzoClient
           endpoint
        3. Pyanzo will raise a 500 error

        If the Graphmart is already activated, then an error is _not_ thrown.

        Args:
            azg_uri (optional): URI of the AnzoGraph datasource.
        """

        request = self._build_activate_request(azg_uri)

        # Don't check the response because it doesn't contain information. It's
        # best to check if the activation failed by (a) the method
        # execute_semantic_service didn't raise an error and (b) by checking
        # that the Graphmart and expected layers are online

        response = self.anzo_client.execute_semantic_service(
            self.ACTIVATION_URI, request
        )
        time.sleep(self.sleep_time)  # sleep to let the activate propagate
        return response.to_trig_string()

    def refresh(self) -> str:
        """Refreshes the Graphmart

        Note that layers can fail to load and a runtime error won't
        be raised.
        """
        request = self._build_refresh_request()
        response = self.anzo_client.execute_semantic_service(
            self.REFRESH_URI, request
        )

        # This will be true even if some layers failed
        success_quadstore = response.filter(
            predicate=self.SUCCESS_PREDICATE, statement_object="true"
        )
        if len(success_quadstore) != 1:
            raise RuntimeError(f"Refreshing Graphmart {self} failed.")
        # sleep to let the refresh propagate
        time.sleep(self.sleep_time)
        try:
            res = response.to_trig_string()
        except:
            res = response
        return res

    def reload(self) -> str:
        """Reloads the Graphmart.

        Note that layers can fail to load and a runtime error won't
        be raised.
        """
        request = self._build_refresh_request()
        response = self.anzo_client.execute_semantic_service(
            self.RELOAD_URI, request
        )
        time.sleep(self.sleep_time)  # sleep to let the reload propagate
        try:
            res = response.to_trig_string()
        except:
            res = response
        return res

    def is_graphmart_online(self) -> bool:
        """Return True if the Graphmart is online and false otherwise.

        Notes
        - If some layers failed to load, this may return True. It's better to
        run are_layers_online
        - If the Graphmart is activating, refreshing, or reloading, it may
        be online, depending on the Graphmart settings
        """

        query = self._build_are_online_query([self.graphmart_uri])
        query_res = self.anzo_client.query_system_tables(query)
        record_dicts = query_res.as_table_results().as_record_dictionaries()

        error_msg = (
            "Query checking the status of the Graphmart"
            "returned ambiguous results"
        )

        if len(record_dicts) != 1:
            raise RuntimeError(error_msg)

        row = record_dicts[0]
        if row["uri"] != self.graphmart_uri:
            raise RuntimeError(error_msg)

        return "System#Online" in row["status"]

    def are_layers_online(self, layer_uris: List[str] = None) -> bool:
        """Returns True if the specified layers are online. If layer_uris is
        None or empty empty then it will return True if all layers are
        online and False if at least one layer is not online

        TODO: mayabe this only check activated layers, if the default is specified.
        """

        layer_uris = layer_uris if layer_uris else self.get_layers()
        if not layer_uris:
            raise RuntimeError(
                "Cannot determine if layers are online because"
                "there are no layers in the Graphmart"
            )

        return self._are_assets_online(layer_uris)

    def _are_assets_online(self, uris: List[str]) -> bool:
        if not uris:
            raise ValueError("List of uris must be non-empty")

        query = self._build_are_online_query(uris)
        query_res = self.anzo_client.query_system_tables(query_string=query)

        are_all_online = True

        for row in query_res.as_table_results().as_record_dictionaries():
            uri = row["uri"]

            is_online = "System#Online" in row["status"]
            if not is_online:
                status = row["status"]
                logger.debug(f"Asset {uri} isn't online; its state: {status}")
                are_all_online = False

        return are_all_online

    def get_layers(self) -> List[str]:
        layer_query = """
            SELECT DISTINCT ?layer WHERE {
                ?gmart <http://openanzo.org/ontologies/2008/07/Anzo#defaultNamedGraph> ?layer .
                ?layer a <http://cambridgesemantics.com/ontologies/Graphmarts#Layer> .
                FILTER(?gmart=<{GRAPHMART}>)
            }
        """.replace("{GRAPHMART}", self.graphmart_uri)  # noqa
        layers_lists = self.anzo_client.query_journal(
            layer_query, named_graphs=ALL_NAMED_GRAPHS_URI
        ).as_table_results().as_list()

        return [l for layer_list in layers_lists for l in layer_list]

    def get_steps(self) -> List[str]:
        step_query = """
            SELECT DISTINCT ?step WHERE {
                ?gmart <http://openanzo.org/ontologies/2008/07/Anzo#defaultNamedGraph> ?step .
                ?step a <http://cambridgesemantics.com/ontologies/Graphmarts#Step> .
                FILTER(?gmart=<{GRAPHMART}>)
            }
        """.replace("{GRAPHMART}", self.graphmart_uri)  # noqa
        step_lists = self.anzo_client.query_journal(
            step_query, named_graphs=ALL_NAMED_GRAPHS_URI
        ).as_table_results().as_list()

        return [s for step_list in step_lists for s in step_list]

    def enable_layers(self, layer_uris: List[str] = None) -> None:
        """Enables the list of layers provided. If layer uris is none, then
        all layers are enabled.
        """

        layer_uris_list = layer_uris if layer_uris else []
        query = self._build_enable_disable_query(True, layer_uris_list)
        self.anzo_client.update_journal(query)
        time.sleep(self.sleep_time)  # sleep to let the update propagate

    def disable_layers(self, layer_uris: List[str] = None) -> None:
        """Disables the list of layers provided. If layer uris is none, then
        all layers are disabled
        """

        layer_uris_list = layer_uris if layer_uris else []
        query = self._build_enable_disable_query(False, layer_uris_list)
        self.anzo_client.update_journal(query)
        time.sleep(self.sleep_time)  # sleep to let the update propagate

    def enable_steps(self, step_uris: List[str] = None) -> None:
        """Enables the list of steps provided. If steps uris is none, then
        all steps are enabled.
        """

        step_uris_list = step_uris if step_uris else []
        query = self._build_enable_disable_query(True, step_uris_list)
        self.anzo_client.update_journal(query)
        time.sleep(self.sleep_time)  # sleep to let the update propagate

    def disable_steps(self, step_uris: List[str] = None) -> None:
        """Disables the list of steps provided. If steps uris is none, then
        all steps are enabled.
        """

        step_uris_list = step_uris if step_uris else []
        query = self._build_enable_disable_query(False, step_uris_list)
        self.anzo_client.update_journal(query)
        time.sleep(self.sleep_time)  # sleep to let the update propagate

    def are_steps_online(self, step_uris: List[str] = None) -> None:
        """Returns True if the specified steps are online
        """

        step_uris = step_uris if step_uris else self.get_steps()
        if not step_uris:
            raise RuntimeError(
                "Cannot determine if steps are online because"
                "there are no steps in the Graphmart"
            )

        return self._are_assets_online(step_uris)

    def _make_values_clause(self, var_name: str, values: List[str]) -> str:
        if not values:
            raise ValueError("Values list must be non-empty")

        encoded_values = [f"({val})" for val in values]

        ret = f" VALUES ({var_name}) {{ "
        ret += " ".join(encoded_values)
        ret += " } "
        return ret

    def _build_are_online_query(self, uris: List[str]) -> str:
        query_base = """
        SELECT DISTINCT ?uri ?status
        WHERE {
            OPTIONAL { ?uri <http://cambridgesemantics.com/ontologies/GraphmartStatus#status> ?status . }
            {VALUES}
        }
        """  # noqa

        if not uris:
            msg = "At least one URI must be provided for building query"
            raise ValueError(msg)

        uris_with_brackers = [f"<{uri}>" for uri in uris]
        values_sub = self._make_values_clause(
            "?uri", uris_with_brackers
        )
        query = query_base.replace("{VALUES}", values_sub)
        return query

    def _build_enable_disable_query(self, should_enable: bool,
                                    uris: List[str]) -> str:
        query_base = """
        DELETE {
            GRAPH ?uri {
                ?uri <http://cambridgesemantics.com/ontologies/Graphmarts#enabled> {OLD_STATE} .
            }
        }
        INSERT {
            GRAPH ?uri {
                ?uri <http://cambridgesemantics.com/ontologies/Graphmarts#enabled> {NEW_STATE} .
            }
        }

        WHERE {
            { SELECT DISTINCT ?uri WHERE {
                GRAPH ?gmart {
                    ?gmart <http://openanzo.org/ontologies/2008/07/Anzo#defaultNamedGraph> ?uri .
                }
            }}

            GRAPH ?uri {
                ?uri <http://cambridgesemantics.com/ontologies/Graphmarts#enabled> {OLD_STATE} .
            }

            {VALUES_GMART}
            {VALUES_URIS}
        }
        """  # noqa

        if should_enable:
            old_state_sub = "false"
            new_state_sub = "true"
        else:
            old_state_sub = "true"
            new_state_sub = "false"

        if uris:
            encoded_uris = [f"(<{uri}>)" for uri in uris]
            layers_sub = "VALUES (?uri) { "
            layers_sub += " ".join(encoded_uris)
            layers_sub += " } "
        else:
            layers_sub = ""

        if uris:
            uri_values = self._make_values_clause("?uri", uris)
        else:
            uri_values = ""

        gmart_sub = f"VALUES (?gmart) {{ ( <{self.graphmart_uri}> ) }}"

        query = query_base.replace("{VALUES_GMART}", gmart_sub)
        query = query.replace("{VALUES_URIS}", layers_sub)
        query = query.replace("{OLD_STATE}", old_state_sub)
        query = query.replace("{NEW_STATE}", new_state_sub)
        return query

    def _build_activate_request(self, azg_uri: str = "") -> QuadStore:
        sub = "http://openanzo.org/semanticServices#graphmartRequest"
        graph = "http://openanzo.org/semanticServices#graphmartRequest"

        type_obj = "http://cambridgesemantics.com/ontologies/Graphmarts#DeployGraphmartRequest"  # noqa
        type_quad = Quad(sub, TYPE_PRED, type_obj, graph)

        block_pred = "http://cambridgesemantics.com/ontologies/Graphmarts#blockTillCreated"  # noqa
        block_obj = "true"
        block_quad = Quad(sub, block_pred, block_obj, graph, obj_type="literal")  # noqa

        gmart_pred = "http://cambridgesemantics.com/ontologies/Graphmarts#graphmart"  # noqa
        gmart_quad = Quad(sub, gmart_pred, self.graphmart_uri, graph)
        quads = {type_quad, block_quad, gmart_quad}

        if azg_uri:
            azg_pred = "http://cambridgesemantics.com/ontologies/Graphmarts#graphQueryEngineUri"  # noqa
            quads.add(Quad(sub, azg_pred, azg_uri, graph))

        return QuadStore(quads)

    def _build_refresh_request(self, layers: List[str] = None) -> QuadStore:
        sub = "http://openanzo.org/semanticServices#graphmartRequest"
        graph = "http://openanzo.org/semanticServices#graphmartRequest"

        type_obj = "http://cambridgesemantics.com/ontologies/Graphmarts#GraphmartRequest"  # noqa
        type_quad = Quad(sub, TYPE_PRED, type_obj, graph)

        gmart_pred = "http://cambridgesemantics.com/ontologies/Graphmarts#graphmart"  # noqa
        gmart_quad = Quad(sub, gmart_pred, self.graphmart_uri, graph)

        quads = {type_quad, gmart_quad}

        layers = layers if layers else []
        for layer in layers:
            layer_pred = "http://cambridgesemantics.com/ontologies/Graphmarts#graphmartChildUri"  # noqa
            layer_quad = Quad(sub, layer_pred, layer, graph)
            quads.add(layer_quad)

        return QuadStore(quads)

    def _build_deactivate_request(self) -> QuadStore:
        sub = "http://openanzo.org/semanticServices#graphmartRequest"
        graph = "http://openanzo.org/semanticServices#graphmartRequest"

        type_objs = [
            "http://cambridgesemantics.com/ontologies/cloud/workflow/WorkflowRequest",  # noqa
            "http://cambridgesemantics.com/ontologies/cloud/workflow/graphmart/WorkflowGMRequest",  # noqa
            "http://openanzo.org/ontologies/2008/2007/SemanticService#ServiceRequest"  # noqa
        ]

        gmart_pred = "http://cambridgesemantics.com/ontologies/cloud/workflow/graphmart/graphmart"  # noqa

        quads = {
            Quad(sub, TYPE_PRED, type_obj, graph) for type_obj in type_objs
        }

        gmart_quad = Quad(sub, gmart_pred, self.graphmart_uri, graph)
        quads.add(gmart_quad)
        return QuadStore(quads)

    def _build_dynamic_activate_request(self, azg_launch_config: str = "", azg_version:str = "", azg_size: str = "") -> QuadStore:
        sub = "http://openanzo.org/semanticServices#graphmartRequest"
        graph = "http://openanzo.org/semanticServices#graphmartRequest"

        type_objs = [
            "http://http://cambridgesemantics.com/ontologies/cloud/workflow/WorkflowCloudDeployAZG",  # noqa
            "http://cambridgesemantics.com/ontologies/cloud/workflow/WorkflowRequest",  # noqa
            "http://cambridgesemantics.com/ontologies/cloud/workflow/graphmart/WorkflowGMRequest"  # noqa
        ]
        
        gmart_pred = "http://cambridgesemantics.com/ontologies/cloud/workflow/graphmart/graphmart"  # noqa
        gmart_quad = Quad(sub, gmart_pred, self.graphmart_uri, graph)
        quads = {
            Quad(sub, TYPE_PRED, type_obj, graph) for type_obj in type_objs
        }
        quads.add(gmart_quad)

        selected_azg_pred = "http://cambridgesemantics.com/ontologies/cloud/workflow/selectedAZG"
        
        # As of Anzo 5.3.10, this (selected_azg_pred) is a required predicate.
        quads.add(Quad(sub, selected_azg_pred, "http://moreinfo/spinUp", graph))
        
        if azg_launch_config:
            launch_config_pred = "http://cambridgesemantics.com/ontologies/cloud/workflow/selectedAZGLaunchConfiguration" #noqa
            launch_config_quad = Quad(sub, launch_config_pred, azg_launch_config, graph)
            quads.add(launch_config_quad)
            
        if azg_version:
            version_pred = "http://cambridgesemantics.com/ontologies/cloud/workflow/selectedAZGVersion"  # noqa
            version_quad = Quad(sub, version_pred, azg_version, graph, obj_type="literal")
            quads.add(version_quad)
            
        if azg_size:
            cluster_size_pred = "http://cambridgesemantics.com/ontologies/cloud/workflow/selectedAZGClusterSize"  # noqa
            cluster_size_quad = Quad(sub, cluster_size_pred, azg_size, graph, obj_type="literal", obj_data_type="http://www.w3.org/2001/XMLSchema#int")
            quads.add(cluster_size_quad)
            
        
        return QuadStore(quads)
