# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

import logging
import time
import signal
from enum import Enum
from uuid import uuid4

from .quad_store import Quad, QuadStore

logger = logging.getLogger(__name__)


class Timeout:
    """
    Helper class for timeouts

    Example usage:
        try:
            with Timeout(seconds=5, error_message="tsup"):
                print("printed")
                time.sleep(10)
                print("never printed")
        except TimeoutError as e:
            print(str(e))
        print("after")
    ```
    """

    def __init__(self, seconds=1, error_message="Timeout") -> None:
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame) -> None:
        raise TimeoutError(self.error_message)

    def __enter__(self) -> None:
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)


class OrchestrationState(Enum):
    SUCCESS = "SUCCESS"             # success means succeess!
    FAIL = "FAIL"                   # fail indicates the IM sent back a failed state
    INACTIVE = "INACTIVE"           # inactive means that the IM isn't running or hasn't run recently
    IN_PROGRESS = "IN_PROGRESS"     # in_progress means that IM is currently running
    ERROR = "ERROR"                 # error indicates there was some internal error, preventing either a success or failure


class IngestionComponentStatus:
    name_pred = "http://openanzo.org/ontologies/2008/07/ASDL/IngestManager#componentName"  # noqa
    status_pred = "http://openanzo.org/ontologies/2008/07/ASDL/IngestManager#componentStatus"  # noqa
    succeeded_pred = "http://openanzo.org/ontologies/2008/07/ASDL/IngestManager#componentSucceeded"  # noqa
    index_pred = "http://openanzo.org/ontologies/2008/07/ASDL/IngestManager#index"  # noqa
    start_time_pred = "http://openanzo.org/ontologies/2008/07/ASDL/IngestManager#ingestStartTime"  # noqa
    end_time_pred = "http://openanzo.org/ontologies/2008/07/ASDL/IngestManager#ingestEndTime"  # noqa
    percent_complete_pred = "http://openanzo.org/ontologies/2008/07/ASDL/IngestManager#percentComplete"  # noqa

    true_string = "true"

    def __init__(self, uri: str, name: str,
                 status: str, did_succeed: bool,
                 start_time: str, end_time: str,
                 index: str, percent_complete: str) -> None:

        self.uri = uri
        self.name = name
        self.status = status
        self.did_succeed = did_succeed
        self.start_time = start_time
        self.end_time = end_time
        self.index = index
        self.percent_complete = percent_complete

    @staticmethod
    def from_quadstore(quadstore, uri):

        def get_featured_quad(quadstore, pred):
            """Given a quadstore and a predicate, returns
            the object of the statement with the predicate
            if there is one, returns the empty
            string if there's no predicate and raises
            an error if there's more than one statement
            with the predicate
            """

            quads = quadstore.filter(predicate=pred).as_list()
            if len(quads) == 0:
                result = ""
            elif len(quads) == 1:
                result = quads[0].obj
            else:
                raise RuntimeError("Unable to determine the name of the "
                                   "ingestion component")
            return result

        name = get_featured_quad(quadstore, IngestionComponentStatus.name_pred)
        status = get_featured_quad(quadstore, IngestionComponentStatus.status_pred)
        start_time = get_featured_quad(quadstore, IngestionComponentStatus.start_time_pred)
        end_time = get_featured_quad(quadstore, IngestionComponentStatus.end_time_pred)
        index = get_featured_quad(quadstore, IngestionComponentStatus.index_pred)
        percent_complete = get_featured_quad(quadstore, IngestionComponentStatus.percent_complete_pred)

        success_quad_pred = IngestionComponentStatus.succeeded_pred
        succeeded_quads = quadstore.filter(predicate=success_quad_pred).as_list()
        if len(succeeded_quads) != 1:
            did_succeed = False
        else:
            did_succeed = succeeded_quads[0].obj == IngestionComponentStatus.true_string

        return IngestionComponentStatus(uri, name, status, did_succeed, start_time, end_time, index, percent_complete)

    def __eq__(self, other):
        return (
            self.uri, self.name, self.status, self.did_succeed,
            self.start_time, self.end_time, self.index,
            self.percent_complete
        ) == (
            other.uri, other.name, other.status, other.did_succeed,
            other.start_time, other.end_time, other.index,
            other.percent_complete
        )

    def __str__(self):
        return f"<IngestionComponentStatus name='{self.name}' status='{self.status}' did_succeed='{self.did_succeed}' start_time='{self.start_time}' end_time='{self.end_time}' index='{self.index}' percent_complete='{self.percent_complete}'>"

    def __repr__(self):
        return str(self)


class RunStatus:
    """
    A class that provide information about the RunStatus.

    The overall status of the run is stored in self.status.

    Each ingestion component, each of which corresponds to a load service,
    has its status parsed and stored an IngestionComponentStatus object that's
    in the list self.ingestion_components
    """

    TYPE_PRED = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
    ING_COMPONENT_TYPE = "http://openanzo.org/ontologies/2008/07/ASDL/IngestManager#IngestionComponent"
    ING_COMPONENT_PRED = "http://openanzo.org/ontologies/2008/07/ASDL/IngestManager#ingestSucceeded"
    true_string = "true"

    completed_statuses = [
        OrchestrationState.SUCCESS, OrchestrationState.FAIL
    ]

    def __init__(self, status, ingestion_components):
        self.status = status
        self.ingestion_components = ingestion_components

    @staticmethod
    def from_quadstore(quadstore):
        """
        Construct a run status object by parsing a quadstore with results from
        checking the status of an ingestion
        Args:
            quadstore: A quadstore that's the result of a status check of
                an ingestion

        Returns:
            A RunStatus object that's a parsed, easier-to-use form of the
            quadstore
        """

        if len(quadstore) == 0:
            raise ValueError("Unable to parse empty quadstore into RunStatus")

        # First, make a set of the all of the subjects in the quadstore
        # that are of type ingestion componenent. Each load service will
        # correspond to one ingestion component
        ingestion_component_subs = set(
            q.sub for q in
            quadstore.filter(predicate=RunStatus.TYPE_PRED,
                             statement_object=RunStatus.ING_COMPONENT_TYPE)
        )

        # Second, loop over each ingestion component subject and create an
        # ingestion component object
        ing_comps = []
        for ingestion_component_sub in ingestion_component_subs:
            ic_quadstore = quadstore.filter(subject=ingestion_component_sub)
            ing_comp = IngestionComponentStatus.from_quadstore(ic_quadstore, ingestion_component_sub)
            ing_comps.append(ing_comp)

        # Third, determine the overall status of the ingestion
        is_complete_qs = quadstore.filter(predicate=RunStatus.ING_COMPONENT_PRED)
        if len(is_complete_qs) == 0:
            status = OrchestrationState.IN_PROGRESS
        elif len(is_complete_qs) > 1:
            status = OrchestrationState.ERROR
        else:
            if is_complete_qs.as_list()[0].obj == RunStatus.true_string:
                status = OrchestrationState.SUCCESS
            else:
                status = OrchestrationState.FAIL

        return RunStatus(status, ing_comps)

    @property
    def is_complete(self):
        return self.status in self.completed_statuses

    @property
    def was_successful(self):
        return self.status == OrchestrationState.SUCCESS


class OrchestrationWrapper:
    """A class for interacting with an orchestration service and one of its
    ingest managers

    Usage:
        anzo_client = AnzoClient(
            "anzo.cambridgesemantics.com", "8080", "username", "password"
        )

        osm = OrchestrationWrapper(anzo_client, im_uri, load_services)

        osm.start()
        run_status = osm.block_until_complete(2000)
    """

    TYPE_PRED = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
    LOAD_SERVICE_PRED = "http://openanzo.org/ontologies/2008/07/ASDL/IngestManager#ingestMgrLoadService"

    STATUS_CHECK_OP = "#getIngestManagerStatuses"
    TRIGGER_SERVICE_OP = "#triggerIngestMgr"

    DEFAULT_ORCH_SERVICE_URI = "http://cambridgesemantics.com/service/OrchestrationService"

    def __init__(self, anzo_client, ingest_manager, load_services, orchestration_uri=""):
        """
        Constructs an OrchestrationWrapper object

        Args:
            anzo_client: AnzoClient object for interacting with anzo
            ingest_manager: URI of the ingest manager
            load_services: List of the load service URIs to execute. If the
                list is empty, then the default load services will be executed
            orchestration_uri (optional): URI of the orchestration service.
                In most cases, this does not need to be provided and the default
                will be used.

        Returns:
            An OrchestrationWrapper object
        """

        self.anzo_client = anzo_client
        self.ingest_manager = ingest_manager
        self.load_services = load_services
        self.named_graph = f"urn://ingestManager/{uuid4()}"

        if orchestration_uri:
            self.orchestration_uri = orchestration_uri
        else:
            self.orchestration_uri = self.DEFAULT_ORCH_SERVICE_URI

        self.status_check_uri = self.orchestration_uri + self.STATUS_CHECK_OP
        self.trigger_service_uri = self.orchestration_uri + self.TRIGGER_SERVICE_OP
        self.poll_interval_seconds = 60  # in seconds


    def start(self):
        service_request = self._build_request(
            self.ingest_manager, self.load_services, self.named_graph
        )

        trigger_response = self.anzo_client.execute_semantic_service(
            self.trigger_service_uri, service_request
        )

        if len(trigger_response) == 0:
            raise RuntimeError("Error triggering the ingest manager")

        # TODO: Question -> is there anything to check here?

    def poll_status(self):
        """Polls for the status of the ingestion and returns a RunStatus
        object with the information about the current status

        Returns:
            A RunStatus object
        """

        max_tries = 3
        num_tries = 0
        while num_tries < max_tries:
            try:
                # Build the request and execute the semantic service to poll the
                # ingest manager status.
                service_request = self._build_request(
                    self.ingest_manager, [], self.named_graph
                )

                poll_response = self.anzo_client.execute_semantic_service(
                    self.status_check_uri, service_request
                )
                str_poll_response = str(poll_response)
                msg = (
                    "Response from Ingest Manager status check:"
                    f"\n{str_poll_response}"
                )
                logger.debug(msg)

                # Parse the current status and return it
                run_status = RunStatus.from_quadstore(poll_response)
                return run_status
            except Exception as e:
                logger.warning(
                    "Unable to poll for orchestration service "
                    f"status on attempt {num_tries}"
                )
                logger.exception(e)
                num_tries += 1

        msg = (
            "Unable to poll for orchestration service status "
            f"after {num_tries} attempts"
        )
        logger.error(msg)
        raise RuntimeError(msg)

    def block_until_complete(self, timeout_seconds):
        """
        Blocks the python code until the current run completes. After
        completion, a RunStatus object is returned with information about
        the run.

        Raises a TimeoutError if there's a timeout.

        Args:
            timeout_seconds: The number of seconds to block until timing out

        Returns:
            A RunStatus object with information about the run
        """

        with Timeout(seconds=timeout_seconds):
            run_status = self.poll_status()
            while not run_status.is_complete:
                logger.debug(f"Current status is {run_status.status}. Sleeping.")
                time.sleep(self.poll_interval_seconds)
                run_status = self.poll_status()
            return run_status

    def _build_request(self, ingest_manager, load_services, graph):
        """
        Constructs a request graph for executing semantic services with an
        ingest manager and an optional number of load services.

        No load services can be provided by passing an empty list.

        Example:
            request = self._build_request(
                "urn://im", ["urn://ls1", urn://ls2"], "urn://graph"
            )

        Args:
            ingest_manager: a single uri for an ingest manager
            load_services: a list of load service URIs
            graph: unique named graph for the request

        Returns:
            Quadstore with the request
        """
        # This method will be build up a set of Quads to construct a quadstore
        quads = set()

        # First, add type statements for the Ingest Manager and the Request Graph
        graph_type_objs = [
            "http://openanzo.org/ontologies/2008/07/ASDL/Orchestration#ASDLNode",
            "http://openanzo.org/ontologies/2008/07/RemoteConnection#RemoteAnzoConnectionConfiguration",
            "http://openanzo.org/ontologies/2008/07/System#Credentials",
            "http://openanzo.org/ontologies/2008/07/System#NetworkConnection"
        ]

        im_type_objs = [
            "http://openanzo.org/ontologies/2008/07/ASDL/IngestManager#IngestManagerConfiguration",
            "http://openanzo.org/ontologies/2008/07/ASDL/Orchestration#ASDLNodeController"
        ]

        for type_obj in graph_type_objs:
            quads.add(Quad(graph, self.TYPE_PRED, type_obj, graph))

        for type_obj in im_type_objs:
            quads.add(Quad(ingest_manager, self.TYPE_PRED, type_obj, graph))

        # Second, add a quad pointing to the ingest manager
        quads.add(Quad(
            graph, "http://openanzo.org/ontologies/2008/07/ASDL/Orchestration#controllerServiceConfiguration",
            ingest_manager, graph
        ))

        # Third, if specific load services are specified, then include a quad pointing to each one
        for load_service in load_services:
            quads.add(Quad(
                ingest_manager, self.LOAD_SERVICE_PRED,
                load_service, graph
            ))

        return QuadStore(quads)

    def __str__(self):
        return (
            "<OrchestrationWrapper "
            f"orchestration_uri='{self.orchestration_uri}', "
            f"ingest_manager_uri='{self.ingest_manager}'>"
        )

    def __repr__(self):
        return str(self)
