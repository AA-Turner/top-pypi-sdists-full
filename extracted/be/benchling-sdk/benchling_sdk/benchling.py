"""Provides the Benchling class, which is the main interface for accessing Benchling's API functionality."""
from __future__ import annotations

from functools import cached_property
import re
from typing import Optional, Protocol, TYPE_CHECKING
import urllib.parse

from benchling_api_client.v2.benchling_client import AuthorizationMethod, BenchlingApiClient
from benchling_api_client.v2.stable.client import Client
import httpx

from benchling_sdk.helpers.retry_helpers import RetryStrategy

if TYPE_CHECKING:
    from benchling_sdk.services.v2.stable.aa_sequence_service import AaSequenceService
    from benchling_sdk.services.v2.stable.api_service import ApiService
    from benchling_sdk.services.v2.stable.app_service import AppService
    from benchling_sdk.services.v2.stable.assay_result_service import AssayResultService
    from benchling_sdk.services.v2.stable.assay_run_service import AssayRunService
    from benchling_sdk.services.v2.stable.blob_service import BlobService
    from benchling_sdk.services.v2.stable.box_service import BoxService
    from benchling_sdk.services.v2.stable.codon_usage_table_service import CodonUsageTableService
    from benchling_sdk.services.v2.stable.container_service import ContainerService
    from benchling_sdk.services.v2.stable.custom_entity_service import CustomEntityService
    from benchling_sdk.services.v2.stable.custom_notation_service import CustomNotationService
    from benchling_sdk.services.v2.stable.dna_alignments_service import DnaAlignmentsService
    from benchling_sdk.services.v2.stable.dna_oligo_service import DnaOligoService
    from benchling_sdk.services.v2.stable.dna_sequence_service import DnaSequenceService
    from benchling_sdk.services.v2.stable.dropdown_service import DropdownService
    from benchling_sdk.services.v2.stable.entity_service import EntityService
    from benchling_sdk.services.v2.stable.entry_service import EntryService
    from benchling_sdk.services.v2.stable.enzyme_service import EnzymeService
    from benchling_sdk.services.v2.stable.event_service import EventService
    from benchling_sdk.services.v2.stable.export_service import ExportService
    from benchling_sdk.services.v2.stable.feature_library_service import FeatureLibraryService
    from benchling_sdk.services.v2.stable.folder_service import FolderService
    from benchling_sdk.services.v2.stable.instrument_query_service import InstrumentQueryService
    from benchling_sdk.services.v2.stable.inventory_service import InventoryService
    from benchling_sdk.services.v2.stable.lab_automation_service import LabAutomationService
    from benchling_sdk.services.v2.stable.label_template_service import LabelTemplateService
    from benchling_sdk.services.v2.stable.location_service import LocationService
    from benchling_sdk.services.v2.stable.mixture_service import MixtureService
    from benchling_sdk.services.v2.stable.molecule_service import MoleculeService
    from benchling_sdk.services.v2.stable.monomer_service import MonomerService
    from benchling_sdk.services.v2.stable.nucleotide_alignments_service import NucleotideAlignmentsService
    from benchling_sdk.services.v2.stable.oligo_service import OligoService
    from benchling_sdk.services.v2.stable.organization_service import OrganizationService
    from benchling_sdk.services.v2.stable.plate_service import PlateService
    from benchling_sdk.services.v2.stable.printer_service import PrinterService
    from benchling_sdk.services.v2.stable.project_service import ProjectService
    from benchling_sdk.services.v2.stable.registry_service import RegistryService
    from benchling_sdk.services.v2.stable.request_service import RequestService
    from benchling_sdk.services.v2.stable.rna_oligo_service import RnaOligoService
    from benchling_sdk.services.v2.stable.rna_sequence_service import RnaSequenceService
    from benchling_sdk.services.v2.stable.schema_service import SchemaService
    from benchling_sdk.services.v2.stable.task_service import TaskService
    from benchling_sdk.services.v2.stable.team_service import TeamService
    from benchling_sdk.services.v2.stable.user_service import UserService
    from benchling_sdk.services.v2.stable.warehouse_service import WarehouseService
    from benchling_sdk.services.v2.stable.workflow_flowchart_config_version_service import (
        WorkflowFlowchartConfigVersionService,
    )
    from benchling_sdk.services.v2.stable.workflow_flowchart_service import WorkflowFlowchartService
    from benchling_sdk.services.v2.stable.workflow_output_service import WorkflowOutputService
    from benchling_sdk.services.v2.stable.workflow_task_group_service import WorkflowTaskGroupService
    from benchling_sdk.services.v2.stable.workflow_task_service import WorkflowTaskService
    from benchling_sdk.services.v2_service import V2Service


class BenchlingApiClientDecorator(Protocol):
    """
    For customizing a BenchlingApiClient client, which gives access to the underlying HTTPX layer.

    Functions implementing this Protocol will receive the default BenchlingApiClient and may mutate specific
    attributes, returning the updated BenchlingApiClient.

    A common use case for this is extending the default HTTP timeout:

    def higher_timeout_client(client: BenchlingApiClient) -> BenchlingApiClient: return client.with_timeout(180)
    """

    def __call__(self, client: BenchlingApiClient) -> BenchlingApiClient:
        """
        Customize a BenchlingApiClient and return the updated client.

        :param client: The underlying API client with default configuration
        :type client: BenchlingApiClient
        :return: The updated client
        :rtype: BenchlingApiClient
        """
        pass


_DEFAULT_BASE_PATH = "/api/v2"
_DEFAULT_RETRY_STRATEGY = RetryStrategy()


class Benchling:
    """
    A facade for interactions with the Benchling platform.

    Methods are organized into namespaces which generally correspond to Resources in Benchling's public API doc.

    See https://benchling.com/api/reference
    """

    _client: Client
    _retry_strategy: RetryStrategy
    _v2_service: Optional[V2Service]

    def __init__(
        self,
        url: str,
        auth_method: AuthorizationMethod,
        base_path: Optional[str] = _DEFAULT_BASE_PATH,
        retry_strategy: Optional[RetryStrategy] = _DEFAULT_RETRY_STRATEGY,
        client_decorator: Optional[BenchlingApiClientDecorator] = None,
        httpx_client: Optional[httpx.Client] = None,
    ):
        """
        Initialize Benchling.

        :param url: A server URL (host and optional port) including scheme such as https://benchling.com
        :param auth_method: A provider of an HTTP Authorization header for usage with the Benchling API. Pass an
                            instance of benchling_sdk.auth.api_key_auth.ApiKeyAuth with a valid Benchling API token for
                            authentication and authorization through HTTP Basic Authentication, or a client_id and
                            client_secret pair with benchling_sdk.auth.client_credentials_oauth2.ClientCredentialsOAuth2
                            for authentication and authorization through OAuth2 client_credentials Bearer token flow.
        :param base_path: If provided, will append to the host. Otherwise, assumes the V2 API. This is
                          a workaround until the generated client supports the servers block. See BNCH-15422
        :param retry_strategy: An optional retry strategy for retrying HTTP calls on failure. Setting to None
                               will disable retries
        :param client_decorator: An optional function that accepts a BenchlingApiClient configured with
                                 default settings and mutates its state as desired
        :param httpx_client: An optional httpx Client which will be used to execute HTTP calls. The Client can be used
                             to modify the behavior of the HTTP calls made to Benchling through means such as adding
                             proxies and certificates or introducing retry logic for transport-level errors.
        """
        full_url = self._format_url(url, base_path)
        if not httpx_client:
            httpx_client = httpx.Client()
        client = BenchlingApiClient(
            httpx_client=httpx_client, base_url=full_url, auth_method=auth_method, timeout=10
        )
        # No public constructor for these and we don't want to subclass and copy the logic
        client._package = "benchling-sdk"
        client._user_agent = "BenchlingSDK"
        if client_decorator:
            client = client_decorator(client)
        self._client = client
        if retry_strategy is None:
            retry_strategy = RetryStrategy.no_retries()
        self._retry_strategy = retry_strategy
        self._v2_service = None

    @property
    def client(self) -> Client:
        """
        Provide access to the underlying generated Benchling Client.

        Should generally not be used except for advanced use cases which may not be well supported by the SDK itself.
        """
        return self._client

    @cached_property
    def v2(self) -> V2Service:
        """
        V2.

        Namespace containing support for the V2 Benchling API.
        """
        from benchling_sdk.services.v2_service import V2Service

        return V2Service(self._client, retry_strategy=self._retry_strategy)

    # ------------------------------------------------------------------------------------
    # Kept for compatibility and ease of access. New services should be added in services.v2.stable and
    # then referenced here as aliases
    # ------------------------------------------------------------------------------------

    @property
    def aa_sequences(self) -> AaSequenceService:
        """
        AA Sequences.

        AA Sequences are the working units of cells that make everything run (they help make structures, catalyze
        reactions and allow for signaling - a kind of internal cell communication). On Benchling, these are comprised
        of a string of amino acids and collections of other attributes, such as annotations.

        See https://benchling.com/api/reference#/AA%20Sequences
        """
        return self.v2.stable.aa_sequences

    @property
    def api(self) -> ApiService:
        """
        Make custom API calls with the underlying BenchlingApiClient.

        A common use case for this is making calls to API endpoints which may not yet be supported in the current SDK
        release. It's capable of making more "generic" calls utilizing our authorization scheme, as well as supporting
        some simple serialization and deserialization for custom models.
        """
        return self.v2.stable.api

    @property
    def apps(self) -> AppService:
        """
        Apps.

        Apps provide a framework for you to customize your teams’ experiences on
        Benchling with custom applications.

        See https://benchling.com/api/reference#/Apps
        and https://docs.benchling.com/docs/getting-started-benchling-apps
        """  # noqa:RUF002  # Ruff gets confused by a trailing apostrophe with a plural noun
        return self.v2.stable.apps

    @property
    def assay_results(self) -> AssayResultService:
        """
        Assay Results.

        Results represent the output of assays that have been performed. You can customize the schemas of results to
        fit your needs. Results can link to runs, batches, and other types.

        See https://benchling.com/api/reference#/Assay%20Results
        """
        return self.v2.stable.assay_results

    @property
    def assay_runs(self) -> AssayRunService:
        """
        Assay Runs.

        Runs capture the details / parameters of a run that was performed. Results are usually nested under a run.

        See https://benchling.com/api/reference#/Assay%20Runs
        """
        return self.v2.stable.assay_runs

    @property
    def blobs(self) -> BlobService:
        """
        Blobs.

        Blobs are opaque files that can be linked to other items in Benchling, like assay runs or results. For example,
        you can upload a blob, then upload an assay result that links to that blob by ID. The blob will then appear as
        part of the assay result in the Benchling web UI.

        See https://benchling.com/api/reference#/Blobs
        """
        return self.v2.stable.blobs

    @property
    def boxes(self) -> BoxService:
        """
        Boxes.

        Boxes are a structured storage type, consisting of a grid of positions that can each hold one container. Unlike
        locations, there are a maximum number of containers that a box can hold (one per position).

        Boxes are all associated with schemas, which define the type of the box (e.g. "10x10 Cryo Box") along with the
        fields that are tracked and the dimensions of the box.

        Like all storage, every Box has a barcode that is unique across the registry.

        See https://benchling.com/api/reference#/Boxes
        """
        return self.v2.stable.boxes

    @property
    def codon_usage_tables(self) -> CodonUsageTableService:
        """
        Codon Usage Tables.

        Benchling curates codon usage data for a variety of organisms to support operations such as Codon
        Optimization and Back Translation.

        See https://benchling.com/api/reference#/Codon%20Usage%20Tables
        """
        return self.v2.stable.codon_usage_tables

    @property
    def containers(self) -> ContainerService:
        """
        Containers.

        Containers are the backbone of sample management in Benchling. They represent physical containers, such as
        tubes or wells, that hold quantities of biological samples (represented by the batches inside the container).
        The container itself tracks its total volume, and the concentration of every batch inside of it.

        Containers are all associated with schemas, which define the type of the container (e.g. "Tube") along with the
        fields that are tracked.

        Like all storage, every container has a barcode that is unique across the registry.

        See https://benchling.com/api/reference#/Containers
        """
        return self.v2.stable.containers

    @property
    def custom_entities(self) -> CustomEntityService:
        """
        Custom Entities.

        Benchling supports custom entities for biological entities that are neither sequences or proteins. Custom
        entities must have an entity schema set and can have both schema fields and custom fields.

        See https://benchling.com/api/reference#/Custom%20Entities
        """
        return self.v2.stable.custom_entities

    @property
    def custom_notations(self) -> CustomNotationService:
        """
        Custom Notations.

        Benchling allows users to configure their own fully-custom string representation formats for import/export
        of nucleotide sequences (including chemical modifications).

        See https://benchling.com/api/reference#/Custom%20Notations
        """
        return self.v2.stable.custom_notations

    @property
    def dna_alignments(self) -> DnaAlignmentsService:
        """
        DNA Alignments.

        A DNA alignment is a Benchling object representing an alignment of multiple DNA sequences.

        See https://benchling.com/api/reference#/DNA%20Alignments
        """
        return self.v2.stable.dna_alignments

    @property
    def dna_oligos(self) -> DnaOligoService:
        """
        DNA Oligos.

        DNA Oligos are short linear DNA sequences that can be attached as primers to full DNA sequences. Just like other
        entities, they support schemas, tags, and aliases.

        See https://benchling.com/api/reference#/DNA%20Oligos
        """
        return self.v2.stable.dna_oligos

    @property
    def dna_sequences(self) -> DnaSequenceService:
        """
        DNA Sequences.

        DNA sequences are the bread and butter of the Benchling Molecular Biology suite. On Benchling, these are
        comprised of a string of nucleotides and collections of other attributes, such as annotations and primers.

        See https://benchling.com/api/reference#/DNA%20Sequences
        """
        return self.v2.stable.dna_sequences

    @property
    def rna_sequences(self) -> RnaSequenceService:
        """
        RNA Sequences.

        Chains of linear, single stranded RNA that support most capabilities and attributes of DNA Sequences.

        See https://benchling.com/api/reference#/RNA%20Sequences
        """
        return self.v2.stable.rna_sequences

    @property
    def dropdowns(self) -> DropdownService:
        """
        Dropdowns.

        Dropdowns are registry-wide enums. Use dropdowns to standardize on spelling and naming conventions, especially
        for important metadata like resistance markers.

        See https://benchling.com/api/reference#/Dropdowns
        """
        return self.v2.stable.dropdowns

    @property
    def entities(self) -> EntityService:
        """
        Entities.

        Entities include DNA and AA sequences, oligos, molecules, custom entities, and
        other biological objects in Benchling. Entities support schemas, tags, and aliases,
        and can be registered.

        See https://benchling.com/api/reference#/Entities
        """
        return self.v2.stable.entities

    @property
    def entries(self) -> EntryService:
        """
        Entries.

        Entries are rich text documents that allow you to capture all of your experimental data in one place.

        See https://benchling.com/api/reference#/Entries
        """
        return self.v2.stable.entries

    @property
    def enzymes(self) -> EnzymeService:
        """
        Enzymes.

        Restriction enzymes are curated by Benchling for operations such as Digests and Codon Optimization.

        See https://benchling.com/api/reference#/Enzymes
        """
        return self.v2.stable.enzymes

    @property
    def events(self) -> EventService:
        """
        Events.

        The Events system allows external services to subscribe to events that are triggered in Benchling (e.g. plasmid
        registration, request submission, etc).

        See https://benchling.com/api/reference#/Events
        """
        return self.v2.stable.events

    @property
    def exports(self) -> ExportService:
        """
        Exports.

        Export a Notebook Entry.

        See https://benchling.com/api/reference#/Exports
        """
        return self.v2.stable.exports

    @property
    def feature_libraries(self) -> FeatureLibraryService:
        """
        Feature Libraries.

        Feature Libraries are collections of shared canonical patterns that can be used to generate
        annotations on matching regions of DNA Sequences or AA Sequences.

        See https://benchling.com/api/reference#/Feature%20Libraries
        """
        return self.v2.stable.feature_libraries

    @property
    def folders(self) -> FolderService:
        """
        Folders.

        Manage folder objects.

        See https://benchling.com/api/reference#/Folders
        """
        return self.v2.stable.folders

    @property
    def instrument_queries(self) -> InstrumentQueryService:
        """
        Instrument Queries.

        Instrument Queries are used to query the instrument service.

        See https://benchling.com/api/reference#/Instrument%20Queries
        """
        return self.v2.stable.instrument_queries

    @property
    def inventory(self) -> InventoryService:
        """
        Inventory.

        Manage inventory wide objects.

        See https://benchling.com/api/reference#/Inventory
        """
        return self.v2.stable.inventory

    @property
    def lab_automation(self) -> LabAutomationService:
        """
        Lab Automation.

        Lab Automation endpoints support integration with lab instruments, and liquid handlers to create samples or
        results, and capture transfers between containers at scale.

        See https://benchling.com/api/reference#/Lab%20Automation
        """
        return self.v2.stable.lab_automation

    @property
    def label_templates(self) -> LabelTemplateService:
        """
        Label Templates.

        List label templates.

        See https://benchling.com/api/reference#/Label%20Templates
        """
        return self.v2.stable.label_templates

    @property
    def locations(self) -> LocationService:
        """
        Locations.

        Manage locations objects. Like all storage, every Location has a barcode that is unique across the registry.

        See https://benchling.com/api/reference#/Locations
        """
        return self.v2.stable.locations

    @property
    def mixtures(self) -> MixtureService:
        """
        Mixtures.

        Mixtures are solutions comprised of multiple ingredients where the exact quantities of each ingredient are
        important to track. Each ingredient is uniquely identified by its component entity.

        See https://benchling.com/api/reference#/Mixtures
        """
        return self.v2.stable.mixtures

    @property
    def monomers(self) -> MonomerService:
        """
        Monomers.

        Monomers are chemical building blocks with specified structures used to compose modified
        nucleotides. Note that monomer write endpoints require tenant admin permissions.

        See https://benchling.com/api/reference#/Monomers
        """
        return self.v2.stable.monomers

    @property
    def molecules(self) -> MoleculeService:
        """
        Molecules.

        Molecules are groups of atoms held together by bonds, representing entities smaller than DNA
        Sequences and AA Sequences. Just like other entities, they support schemas, tags, and aliases.

        See https://benchling.com/api/reference#/Molecules
        """
        return self.v2.stable.molecules

    @property
    def nucleotide_alignments(self) -> NucleotideAlignmentsService:
        """
        Nucleotide Alignments.

        A Nucleotide Alignment is a Benchling object representing an alignment of multiple DNA and/or RNA sequences.

        See https://benchling.com/api/reference#/Nucleotide%20Alignments
        """
        return self.v2.stable.nucleotide_alignments

    @property
    def oligos(self) -> OligoService:
        """
        Oligos.

        Oligos are short linear DNA sequences that can be attached as primers to full DNA sequences. Just like other
        entities, they support schemas, tags, and aliases.

        Please migrate to the corresponding DNA Oligos endpoints so that we can support RNA Oligos.

        See https://benchling.com/api/reference#/Oligos
        """
        return self.v2.stable.oligos

    @property
    def organizations(self) -> OrganizationService:
        """
        Organizations.

        View organization objects.

        See https://benchling.com/api/reference#/Organizations
        """
        return self.v2.stable.organizations

    @property
    def plates(self) -> PlateService:
        """
        Plates.

        Plates are a structured storage type, grids of wells that each function like containers. Plates come in two
        types: a traditional "fixed" type, where the wells cannot move, and a "matrix" type. A matrix plate has similar
        functionality to a box, where the containers inside can be moved around and removed altogether.

        Plates are all associated with schemas, which define the type of the plate (e.g. "96 Well Plate") along with
        the fields that are tracked, the dimensions of the plate, and whether or not the plate is a matrix plate or a
        traditional well plate.

        Like all storage, every Plate has a barcode that is unique across the registry.

        See https://benchling.com/api/reference#/Plates
        """
        return self.v2.stable.plates

    @property
    def printers(self) -> PrinterService:
        """
        Printers.

        List printers.

        See https://benchling.com/api/reference#/Printers
        """
        return self.v2.stable.printers

    @property
    def projects(self) -> ProjectService:
        """
        Projects.

        Manage project objects.

        See https://benchling.com/api/reference#/Projects
        """
        return self.v2.stable.projects

    @property
    def registry(self) -> RegistryService:
        """
        Registry.

        Manage registry objects.

        See https://benchling.com/api/reference#/Registry
        """
        return self.v2.stable.registry

    @property
    def requests(self) -> RequestService:
        """
        Requests.

        Requests allow scientists and teams to collaborate around experimental assays and workflows.

        See https://benchling.com/api/reference#/Requests
        """
        return self.v2.stable.requests

    @property
    def rna_oligos(self) -> RnaOligoService:
        """
        RNA Oligos.

        RNA Oligos are short linear RNA sequences that can be attached as primers to full DNA sequences. Just like other
        entities, they support schemas, tags, and aliases.

        See https://benchling.com/api/reference#/RNA%20Oligos
        """
        return self.v2.stable.rna_oligos

    @property
    def schemas(self) -> SchemaService:
        """
        Schemas.

        Schemas represent custom configuration of objects in Benchling. See https://docs.benchling.com/docs/schemas in
        our documentation on how Schemas impact our developers

        See https://benchling.com/api/reference#/Schemas
        """
        return self.v2.stable.schemas

    @property
    def tasks(self) -> TaskService:
        """
        Tasks.

        Endpoints that perform expensive computations launch long-running tasks. These endpoints return the task ID (a
        UUID) in the response body.

        After launching a task, periodically invoke the Get a task endpoint with the task UUID (e.g., every 10
        seconds), until the status is no longer RUNNING.

        You can access a task for up to 30 minutes after its completion, after which its data will no longer be
        available.

        See https://benchling.com/api/reference#/Tasks
        """
        return self.v2.stable.tasks

    @property
    def teams(self) -> TeamService:
        """
        Teams.

        View team objects.

        See https://benchling.com/api/reference#/Teams
        """
        return self.v2.stable.teams

    @property
    def users(self) -> UserService:
        """
        Benchling users.

        See https://benchling.com/api/reference#/Users
        """
        return self.v2.stable.users

    @property
    def warehouse(self) -> WarehouseService:
        """
        Warehouse.

        Manage warehouse credentials.

        See https://benchling.com/api/reference#/Warehouse
        """
        return self.v2.stable.warehouse

    @property
    def workflow_flowcharts(self) -> WorkflowFlowchartService:
        """
        Workflow Flowcharts.

        Workflow flowcharts represent the nodes and edges that a flowchart is comprised of.

        See https://benchling.com/api/reference#/Workflow%20Flowcharts
        """
        return self.v2.stable.workflow_flowcharts

    @property
    def workflow_flowchart_config_versions(self) -> WorkflowFlowchartConfigVersionService:
        """
        Workflow Flowchart Config Versions.

        Workflow flowchart config versions are versioned graphs of flowchart configurations.

        See https://benchling.com/api/reference#/Workflow%20Flowchart%20Config%20Versions
        """
        return self.v2.stable.workflow_flowchart_config_versions

    @property
    def workflow_outputs(self) -> WorkflowOutputService:
        """
        Workflow Outputs.

        Workflow outputs are outputs of a workflow task.

        See https://benchling.com/api/reference#/Workflow%20Outputs
        """
        return self.v2.stable.workflow_outputs

    @property
    def workflow_task_groups(self) -> WorkflowTaskGroupService:
        """
        Workflow Tasks Groups.

        Workflow task groups are groups of workflow tasks of the same schema.

        See https://benchling.com/api/reference#/Workflow%20Task%20Groups
        """
        return self.v2.stable.workflow_task_groups

    @property
    def workflow_tasks(self) -> WorkflowTaskService:
        """
        Workflow Tasks.

        Workflow tasks encapsulate a single unit of work.

        See https://benchling.com/api/reference#/Workflow%20Tasks
        """
        return self.v2.stable.workflow_tasks

    @staticmethod
    def _format_url(url: str, base_path: Optional[str]) -> str:
        """Format a user provided URL to remove unneeded slashes."""
        if base_path:
            joined_url = urllib.parse.urljoin(url, base_path)
            # Strip any trailing slashes, the API client will lead with them
            joined_url = re.sub(r"/+$", "", joined_url)
            return joined_url
        return url
