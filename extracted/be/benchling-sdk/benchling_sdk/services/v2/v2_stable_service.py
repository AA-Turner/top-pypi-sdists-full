from __future__ import annotations

from functools import cached_property
from typing import Optional, TYPE_CHECKING

from benchling_api_client.v2.stable.client import Client

from benchling_sdk.helpers.retry_helpers import RetryStrategy
from benchling_sdk.services.v2.base_service import BaseService

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


class V2StableService(BaseService):
    """
    V2 Stable.

    Namespace containing support for the V2 stable endpoints of the Benchling API.
    """

    def __init__(self, client: Client, retry_strategy: Optional[RetryStrategy] = None):
        """
        Initialize a service.

        :param client: Underlying generated Client.
        :param retry_strategy: Retry strategy for failed HTTP calls
        """
        super().__init__(client, retry_strategy)

    @cached_property
    def aa_sequences(self) -> AaSequenceService:
        """
        AA Sequences.

        AA Sequences are the working units of cells that make everything run (they help make structures, catalyze
        reactions and allow for signaling - a kind of internal cell communication). On Benchling, these are comprised
        of a string of amino acids and collections of other attributes, such as annotations.

        See https://benchling.com/api/reference#/AA%20Sequences
        """
        from .stable.aa_sequence_service import AaSequenceService

        return self._create_service(AaSequenceService)

    @cached_property
    def api(self) -> ApiService:
        """
        Make custom API calls with the underlying BenchlingApiClient.

        A common use case for this is making calls to API endpoints which may not yet be supported in the current SDK
        release. It's capable of making more "generic" calls utilizing our authorization scheme, as well as supporting
        some simple serialization and deserialization for custom models.
        """
        from .stable.api_service import ApiService

        return self._create_service(ApiService)

    @cached_property
    def apps(self) -> AppService:
        """
        Apps.

        Apps provide a framework for you to customize your teams’ experiences on
        Benchling with custom applications.

        See https://benchling.com/api/reference#/Apps
        and https://docs.benchling.com/docs/getting-started-benchling-apps
        """  # noqa:RUF002  # Ruff gets confused by a trailing apostrophe with a plural noun
        from .stable.app_service import AppService

        return self._create_service(AppService)

    @cached_property
    def assay_results(self) -> AssayResultService:
        """
        Assay Results.

        Results represent the output of assays that have been performed. You can customize the schemas of results to
        fit your needs. Results can link to runs, batches, and other types.

        See https://benchling.com/api/reference#/Assay%20Results
        """
        from .stable.assay_result_service import AssayResultService

        return self._create_service(AssayResultService)

    @cached_property
    def assay_runs(self) -> AssayRunService:
        """
        Assay Runs.

        Runs capture the details / parameters of a run that was performed. Results are usually nested under a run.

        See https://benchling.com/api/reference#/Assay%20Runs
        """
        from .stable.assay_run_service import AssayRunService

        return self._create_service(AssayRunService)

    @cached_property
    def blobs(self) -> BlobService:
        """
        Blobs.

        Blobs are opaque files that can be linked to other items in Benchling, like assay runs or results. For example,
        you can upload a blob, then upload an assay result that links to that blob by ID. The blob will then appear as
        part of the assay result in the Benchling web UI.

        See https://benchling.com/api/reference#/Blobs
        """
        from .stable.blob_service import BlobService

        return self._create_service(BlobService)

    @cached_property
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
        from .stable.box_service import BoxService

        return self._create_service(BoxService)

    @cached_property
    def codon_usage_tables(self) -> CodonUsageTableService:
        """
        Codon Usage Tables.

        Benchling curates codon usage data for a variety of organisms to support operations such as Codon
        Optimization and Back Translation.

        See https://benchling.com/api/reference#/Codon%20Usage%20Tables
        """
        from .stable.codon_usage_table_service import CodonUsageTableService

        return self._create_service(CodonUsageTableService)

    @cached_property
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
        from .stable.container_service import ContainerService

        return self._create_service(ContainerService)

    @cached_property
    def custom_entities(self) -> CustomEntityService:
        """
        Custom Entities.

        Benchling supports custom entities for biological entities that are neither sequences or proteins. Custom
        entities must have an entity schema set and can have both schema fields and custom fields.

        See https://benchling.com/api/reference#/Custom%20Entities
        """
        from .stable.custom_entity_service import CustomEntityService

        return self._create_service(CustomEntityService)

    @cached_property
    def custom_notations(self) -> CustomNotationService:
        """
        Custom Notations.

        Benchling allows users to configure their own fully-custom string representation formats for import/export
        of nucleotide sequences (including chemical modifications).

        See https://benchling.com/api/reference#/Custom%20Notations
        """
        from .stable.custom_notation_service import CustomNotationService

        return self._create_service(CustomNotationService)

    @cached_property
    def dna_alignments(self) -> DnaAlignmentsService:
        """
        DNA Alignments.

        A DNA alignment is a Benchling object representing an alignment of multiple DNA sequences.

        See https://benchling.com/api/reference#/DNA%20Alignments
        """
        from .stable.dna_alignments_service import DnaAlignmentsService

        return self._create_service(DnaAlignmentsService)

    @cached_property
    def dna_oligos(self) -> DnaOligoService:
        """
        DNA Oligos.

        DNA Oligos are short linear DNA sequences that can be attached as primers to full DNA sequences. Just like other
        entities, they support schemas, tags, and aliases.

        See https://benchling.com/api/reference#/DNA%20Oligos
        """
        from .stable.dna_oligo_service import DnaOligoService

        return self._create_service(DnaOligoService)

    @cached_property
    def dna_sequences(self) -> DnaSequenceService:
        """
        DNA Sequences.

        DNA sequences are the bread and butter of the Benchling Molecular Biology suite. On Benchling, these are
        comprised of a string of nucleotides and collections of other attributes, such as annotations and primers.

        See https://benchling.com/api/reference#/DNA%20Sequences
        """
        from .stable.dna_sequence_service import DnaSequenceService

        return self._create_service(DnaSequenceService)

    @cached_property
    def rna_sequences(self) -> RnaSequenceService:
        """
        RNA Sequences.

        Chains of linear, single stranded RNA that support most capabilities and attributes of DNA Sequences.

        See https://benchling.com/api/reference#/RNA%20Sequences
        """
        from .stable.rna_sequence_service import RnaSequenceService

        return self._create_service(RnaSequenceService)

    @cached_property
    def dropdowns(self) -> DropdownService:
        """
        Dropdowns.

        Dropdowns are registry-wide enums. Use dropdowns to standardize on spelling and naming conventions, especially
        for important metadata like resistance markers.

        See https://benchling.com/api/reference#/Dropdowns
        """
        from .stable.dropdown_service import DropdownService

        return self._create_service(DropdownService)

    @cached_property
    def entities(self) -> EntityService:
        """
        Entities.

        Entities include DNA and AA sequences, oligos, molecules, custom entities, and
        other biological objects in Benchling. Entities support schemas, tags, and aliases,
        and can be registered.

        See https://benchling.com/api/reference#/Entities
        """
        from .stable.entity_service import EntityService

        return self._create_service(EntityService)

    @cached_property
    def entries(self) -> EntryService:
        """
        Entries.

        Entries are rich text documents that allow you to capture all of your experimental data in one place.

        See https://benchling.com/api/reference#/Entries
        """
        from .stable.entry_service import EntryService

        return self._create_service(EntryService)

    @cached_property
    def enzymes(self) -> EnzymeService:
        """
        Enzymes.

        Restriction enzymes are curated by Benchling for operations such as Digests and Codon Optimization.

        See https://benchling.com/api/reference#/Enzymes
        """
        from .stable.enzyme_service import EnzymeService

        return self._create_service(EnzymeService)

    @cached_property
    def events(self) -> EventService:
        """
        Events.

        The Events system allows external services to subscribe to events that are triggered in Benchling (e.g. plasmid
        registration, request submission, etc).

        See https://benchling.com/api/reference#/Events
        """
        from .stable.event_service import EventService

        return self._create_service(EventService)

    @cached_property
    def exports(self) -> ExportService:
        """
        Exports.

        Export a Notebook Entry.

        See https://benchling.com/api/reference#/Exports
        """
        from .stable.export_service import ExportService

        return self._create_service(ExportService)

    @cached_property
    def feature_libraries(self) -> FeatureLibraryService:
        """
        Feature Libraries.

        Feature Libraries are collections of shared canonical patterns that can be used to generate
        annotations on matching regions of DNA Sequences or AA Sequences.

        See https://benchling.com/api/reference#/Feature%20Libraries
        """
        from .stable.feature_library_service import FeatureLibraryService

        return self._create_service(FeatureLibraryService)

    @cached_property
    def folders(self) -> FolderService:
        """
        Folders.

        Manage folder objects.

        See https://benchling.com/api/reference#/Folders
        """
        from .stable.folder_service import FolderService

        return self._create_service(FolderService)

    @cached_property
    def instrument_queries(self) -> InstrumentQueryService:
        """
        Instrument Queries.

        Instrument Queries are used to query the instrument service.

        See https://benchling.com/api/reference#/Instrument%20Queries
        """
        from .stable.instrument_query_service import InstrumentQueryService

        return self._create_service(InstrumentQueryService)

    @cached_property
    def inventory(self) -> InventoryService:
        """
        Inventory.

        Manage inventory wide objects.

        See https://benchling.com/api/reference#/Inventory
        """
        from .stable.inventory_service import InventoryService

        return self._create_service(InventoryService)

    @cached_property
    def lab_automation(self) -> LabAutomationService:
        """
        Lab Automation.

        Lab Automation endpoints support integration with lab instruments, and liquid handlers to create samples or
        results, and capture transfers between containers at scale.

        See https://benchling.com/api/reference#/Lab%20Automation
        """
        from .stable.lab_automation_service import LabAutomationService

        return self._create_service(LabAutomationService)

    @cached_property
    def label_templates(self) -> LabelTemplateService:
        """
        Label Templates.

        List label templates.

        See https://benchling.com/api/reference#/Label%20Templates
        """
        from .stable.label_template_service import LabelTemplateService

        return self._create_service(LabelTemplateService)

    @cached_property
    def locations(self) -> LocationService:
        """
        Locations.

        Manage locations objects. Like all storage, every Location has a barcode that is unique across the registry.

        See https://benchling.com/api/reference#/Locations
        """
        from .stable.location_service import LocationService

        return self._create_service(LocationService)

    @cached_property
    def mixtures(self) -> MixtureService:
        """
        Mixtures.

        Mixtures are solutions comprised of multiple ingredients where the exact quantities of each ingredient are
        important to track. Each ingredient is uniquely identified by its component entity.

        See https://benchling.com/api/reference#/Mixtures
        """
        from .stable.mixture_service import MixtureService

        return self._create_service(MixtureService)

    @cached_property
    def monomers(self) -> MonomerService:
        """
        Monomers.

        Monomers are chemical building blocks with specified structures used to compose modified
        nucleotides. Note that monomer write endpoints require tenant admin permissions.

        See https://benchling.com/api/reference#/Monomers
        """
        from .stable.monomer_service import MonomerService

        return self._create_service(MonomerService)

    @cached_property
    def molecules(self) -> MoleculeService:
        """
        Molecules.

        Molecules are groups of atoms held together by bonds, representing entities smaller than DNA
        Sequences and AA Sequences. Just like other entities, they support schemas, tags, and aliases.

        See https://benchling.com/api/reference#/Molecules
        """
        from .stable.molecule_service import MoleculeService

        return self._create_service(MoleculeService)

    @cached_property
    def nucleotide_alignments(self) -> NucleotideAlignmentsService:
        """
        Nucleotide Alignments.

        A Nucleotide Alignment is a Benchling object representing an alignment of multiple DNA and/or RNA sequences.

        See https://benchling.com/api/reference#/Nucleotide%20Alignments
        """
        from .stable.nucleotide_alignments_service import NucleotideAlignmentsService

        return self._create_service(NucleotideAlignmentsService)

    @cached_property
    def oligos(self) -> OligoService:
        """
        Oligos.

        Oligos are short linear DNA sequences that can be attached as primers to full DNA sequences. Just like other
        entities, they support schemas, tags, and aliases.

        Please migrate to the corresponding DNA Oligos endpoints so that we can support RNA Oligos.

        See https://benchling.com/api/reference#/Oligos
        """
        from .stable.oligo_service import OligoService

        return self._create_service(OligoService)

    @cached_property
    def organizations(self) -> OrganizationService:
        """
        Organizations.

        View organization objects.

        See https://benchling.com/api/reference#/Organizations
        """
        from .stable.organization_service import OrganizationService

        return self._create_service(OrganizationService)

    @cached_property
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
        from .stable.plate_service import PlateService

        return self._create_service(PlateService)

    @cached_property
    def printers(self) -> PrinterService:
        """
        Printers.

        List printers.

        See https://benchling.com/api/reference#/Printers
        """
        from .stable.printer_service import PrinterService

        return self._create_service(PrinterService)

    @cached_property
    def projects(self) -> ProjectService:
        """
        Projects.

        Manage project objects.

        See https://benchling.com/api/reference#/Projects
        """
        from .stable.project_service import ProjectService

        return self._create_service(ProjectService)

    @cached_property
    def registry(self) -> RegistryService:
        """
        Registry.

        Manage registry objects.

        See https://benchling.com/api/reference#/Registry
        """
        from .stable.registry_service import RegistryService

        return self._create_service(RegistryService)

    @cached_property
    def requests(self) -> RequestService:
        """
        Requests.

        Requests allow scientists and teams to collaborate around experimental assays and workflows.

        See https://benchling.com/api/reference#/Requests
        """
        from .stable.request_service import RequestService

        return self._create_service(RequestService)

    @cached_property
    def rna_oligos(self) -> RnaOligoService:
        """
        RNA Oligos.

        RNA Oligos are short linear RNA sequences that can be attached as primers to full DNA sequences. Just like other
        entities, they support schemas, tags, and aliases.

        See https://benchling.com/api/reference#/RNA%20Oligos
        """
        from .stable.rna_oligo_service import RnaOligoService

        return self._create_service(RnaOligoService)

    @cached_property
    def schemas(self) -> SchemaService:
        """
        Schemas.

        Schemas represent custom configuration of objects in Benchling. See https://docs.benchling.com/docs/schemas in
        our documentation on how Schemas impact our developers

        See https://benchling.com/api/reference#/Schemas
        """
        from .stable.schema_service import SchemaService

        return self._create_service(SchemaService)

    @cached_property
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
        from .stable.task_service import TaskService

        return self._create_service(TaskService)

    @cached_property
    def teams(self) -> TeamService:
        """
        Teams.

        View team objects.

        See https://benchling.com/api/reference#/Teams
        """
        from .stable.team_service import TeamService

        return self._create_service(TeamService)

    @cached_property
    def users(self) -> UserService:
        """
        Benchling users.

        See https://benchling.com/api/reference#/Users
        """
        from .stable.user_service import UserService

        return self._create_service(UserService)

    @cached_property
    def warehouse(self) -> WarehouseService:
        """
        Warehouse.

        Manage warehouse credentials.

        See https://benchling.com/api/reference#/Warehouse
        """
        from .stable.warehouse_service import WarehouseService

        return self._create_service(WarehouseService)

    @cached_property
    def workflow_flowcharts(self) -> WorkflowFlowchartService:
        """
        Workflow Flowcharts.

        Workflow flowcharts represent the nodes and edges that a flowchart is comprised of.

        See https://benchling.com/api/reference#/Workflow%20Flowcharts
        """
        from .stable.workflow_flowchart_service import WorkflowFlowchartService

        return self._create_service(WorkflowFlowchartService)

    @cached_property
    def workflow_flowchart_config_versions(self) -> WorkflowFlowchartConfigVersionService:
        """
        Workflow Flowchart Config Versions.

        Workflow flowchart config versions are versioned graphs of flowchart configurations.

        See https://benchling.com/api/reference#/Workflow%20Flowchart%20Config%20Versions
        """
        from .stable.workflow_flowchart_config_version_service import WorkflowFlowchartConfigVersionService

        return self._create_service(WorkflowFlowchartConfigVersionService)

    @cached_property
    def workflow_outputs(self) -> WorkflowOutputService:
        """
        Workflow Outputs.

        Workflow outputs are outputs of a workflow task.

        See https://benchling.com/api/reference#/Workflow%20Outputs
        """
        from .stable.workflow_output_service import WorkflowOutputService

        return self._create_service(WorkflowOutputService)

    @cached_property
    def workflow_task_groups(self) -> WorkflowTaskGroupService:
        """
        Workflow Tasks Groups.

        Workflow task groups are groups of workflow tasks of the same schema.

        See https://benchling.com/api/reference#/Workflow%20Task%20Groups
        """
        from .stable.workflow_task_group_service import WorkflowTaskGroupService

        return self._create_service(WorkflowTaskGroupService)

    @cached_property
    def workflow_tasks(self) -> WorkflowTaskService:
        """
        Workflow Tasks.

        Workflow tasks encapsulate a single unit of work.

        See https://benchling.com/api/reference#/Workflow%20Tasks
        """
        from .stable.workflow_task_service import WorkflowTaskService

        return self._create_service(WorkflowTaskService)
