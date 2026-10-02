from __future__ import annotations

import uuid
from os import PathLike
from typing import TypeVar
from pathlib import Path
from collections.abc import Iterable
from typing_extensions import Literal, TypedDict

from ._state import (
    DOWNLOAD_MODE_EVERYTHING,
    RunType,
    RunMetadata,
    DownloadMode,
    load_metadata,
    save_metadata,
    ensure_directory_ready,
    normalize_download_mode,
)
from ._types import SmallMoleculeTarget
from ._engine import (
    ExperimentEngine,
    PipelineDefinition,
    PredictionDefinition,
    unsupported_stop,
)
from ._errors import ExperimentError
from .._client import Boltz
from ._progress import build_progress_sink
from ._normalize import (
    PredictionBondInput,
    PredictionModelInput,
    PredictionEntityInput,
    PredictionBindingInput,
    PredictionTemplateInput,
    ProteinDesignTargetInput,
    PredictionConstraintInput,
    PredictionModelOptionsInput,
    ProteinLibraryScreenTargetInput,
    ProteinDesignBinderSpecificationInput,
    normalize_prediction_request,
    normalize_protein_design_request,
    normalize_small_molecule_design_request,
    normalize_protein_library_screen_request,
    normalize_small_molecule_library_screen_request,
)
from ..pagination import SyncCursorPage
from ._addressing import metadata_path, resolve_create_run_dir, resolve_existing_run_dir
from ._fingerprint import fingerprint_payload
from ..types.protein import (
    design_start_params as protein_design_start_params,
    design_stop_response as protein_design_stop_response,
    design_start_response as protein_design_start_response,
    design_retrieve_response as protein_design_retrieve_response,
    library_screen_start_params as protein_library_screen_start_params,
    design_list_results_response as protein_design_list_results_response,
    library_screen_stop_response as protein_library_screen_stop_response,
    library_screen_start_response as protein_library_screen_start_response,
    library_screen_retrieve_response as protein_library_screen_retrieve_response,
    library_screen_list_results_response as protein_library_screen_list_results_response,
)
from ..types.predictions import (
    adme_start_params,
    adme_start_response,
    adme_retrieve_response,
    structure_and_binding_start_params,
    structure_and_binding_start_response,
    structure_and_binding_retrieve_response,
)
from ..types.small_molecule import (
    design_start_params as small_molecule_design_start_params,
    design_stop_response as small_molecule_design_stop_response,
    design_start_response as small_molecule_design_start_response,
    design_retrieve_response as small_molecule_design_retrieve_response,
    library_screen_start_params as small_molecule_library_screen_start_params,
    design_list_results_response as small_molecule_design_list_results_response,
    library_screen_stop_response as small_molecule_library_screen_stop_response,
    library_screen_start_response as small_molecule_library_screen_start_response,
    library_screen_retrieve_response as small_molecule_library_screen_retrieve_response,
    library_screen_list_results_response as small_molecule_library_screen_list_results_response,
)


class _WorkspaceKwargs(TypedDict, total=False):
    workspace_id: str


class _WorkspaceAfterKwargs(TypedDict, total=False):
    workspace_id: str
    after_id: str


class _SmallMoleculeDesignStartKwargs(TypedDict, total=False):
    chemical_space: Literal["enamine_real"]
    molecule_filters: small_molecule_design_start_params.MoleculeFilters
    workspace_id: str


class _SmallMoleculeLibraryScreenStartKwargs(TypedDict, total=False):
    molecule_filters: small_molecule_library_screen_start_params.MoleculeFilters
    workspace_id: str


_PipelinePayloadT = TypeVar("_PipelinePayloadT")


class ExperimentsNamespace:
    def __init__(self, client: Boltz) -> None:
        self._client = client

        self._prediction_definition: PredictionDefinition[
            structure_and_binding_start_params.StructureAndBindingStartParams
        ] = PredictionDefinition(
            run_type="prediction",
            start_call=self._prediction_start_call,
            retrieve_call=self._prediction_retrieve_call,
        )
        self._adme_prediction_definition: PredictionDefinition[adme_start_params.AdmeStartParams] = (
            PredictionDefinition(
                run_type="adme",
                start_call=self._adme_start_call,
                retrieve_call=self._adme_retrieve_call,
                materialize_archive=False,
            )
        )
        self._protein_design_definition: PipelineDefinition[protein_design_start_params.ProteinDesignRunInput] = (
            PipelineDefinition(
                run_type="protein_design",
                start_call=self._protein_design_start_call,
                retrieve_call=self._protein_design_retrieve_call,
                list_results_call=self._protein_design_list_results_call,
                stop_call=self._protein_design_stop_call,
            )
        )
        self._protein_library_screen_definition: PipelineDefinition[
            protein_library_screen_start_params.LibraryScreenStartParams
        ] = PipelineDefinition(
            run_type="protein_library_screen",
            start_call=self._protein_library_screen_start_call,
            retrieve_call=self._protein_library_screen_retrieve_call,
            list_results_call=self._protein_library_screen_list_results_call,
            stop_call=self._protein_library_screen_stop_call,
        )
        self._small_molecule_design_definition: PipelineDefinition[
            small_molecule_design_start_params.DesignStartParams
        ] = PipelineDefinition(
            run_type="small_molecule_design",
            start_call=self._small_molecule_design_start_call,
            retrieve_call=self._small_molecule_design_retrieve_call,
            list_results_call=self._small_molecule_design_list_results_call,
            stop_call=self._small_molecule_design_stop_call,
        )
        self._small_molecule_library_screen_definition: PipelineDefinition[
            small_molecule_library_screen_start_params.LibraryScreenStartParams
        ] = PipelineDefinition(
            run_type="small_molecule_library_screen",
            start_call=self._small_molecule_library_screen_start_call,
            retrieve_call=self._small_molecule_library_screen_retrieve_call,
            list_results_call=self._small_molecule_library_screen_list_results_call,
            stop_call=self._small_molecule_library_screen_stop_call,
        )

    def run_structure_and_binding(
        self,
        *,
        entities: Iterable[PredictionEntityInput],
        model: PredictionModelInput,
        binding: PredictionBindingInput | None = None,
        bonds: Iterable[PredictionBondInput] | None = None,
        constraints: Iterable[PredictionConstraintInput] | None = None,
        model_options: PredictionModelOptionsInput | None = None,
        num_samples: int | None = None,
        templates: Iterable[PredictionTemplateInput] | None = None,
        root_dir: str | PathLike[str] = "boltz-experiments",
        name: str | None = None,
        workspace_id: str | None = None,
        quiet: bool = False,
        poll_interval_seconds: float = 5.0,
    ) -> Path:
        return self.run_prediction(
            entities=entities,
            model=model,
            binding=binding,
            bonds=bonds,
            constraints=constraints,
            model_options=model_options,
            num_samples=num_samples,
            templates=templates,
            root_dir=root_dir,
            name=name,
            workspace_id=workspace_id,
            quiet=quiet,
            poll_interval_seconds=poll_interval_seconds,
        )

    def start_structure_and_binding(
        self,
        *,
        entities: Iterable[PredictionEntityInput],
        model: PredictionModelInput,
        binding: PredictionBindingInput | None = None,
        bonds: Iterable[PredictionBondInput] | None = None,
        constraints: Iterable[PredictionConstraintInput] | None = None,
        model_options: PredictionModelOptionsInput | None = None,
        num_samples: int | None = None,
        templates: Iterable[PredictionTemplateInput] | None = None,
        root_dir: str | PathLike[str] = "boltz-experiments",
        name: str | None = None,
        workspace_id: str | None = None,
        quiet: bool = False,
        poll_interval_seconds: float = 5.0,
    ) -> Path:
        return self.start_prediction(
            entities=entities,
            model=model,
            binding=binding,
            bonds=bonds,
            constraints=constraints,
            model_options=model_options,
            num_samples=num_samples,
            templates=templates,
            root_dir=root_dir,
            name=name,
            workspace_id=workspace_id,
            quiet=quiet,
            poll_interval_seconds=poll_interval_seconds,
        )

    def predict_structure_and_binding(
        self,
        *,
        entities: Iterable[PredictionEntityInput],
        model: PredictionModelInput,
        binding: PredictionBindingInput | None = None,
        bonds: Iterable[PredictionBondInput] | None = None,
        constraints: Iterable[PredictionConstraintInput] | None = None,
        model_options: PredictionModelOptionsInput | None = None,
        num_samples: int | None = None,
        templates: Iterable[PredictionTemplateInput] | None = None,
        root_dir: str | PathLike[str] = "boltz-experiments",
        name: str | None = None,
        workspace_id: str | None = None,
        quiet: bool = False,
        poll_interval_seconds: float = 5.0,
    ) -> Path:
        return self.run_structure_and_binding(
            entities=entities,
            model=model,
            binding=binding,
            bonds=bonds,
            constraints=constraints,
            model_options=model_options,
            num_samples=num_samples,
            templates=templates,
            root_dir=root_dir,
            name=name,
            workspace_id=workspace_id,
            quiet=quiet,
            poll_interval_seconds=poll_interval_seconds,
        )

    def run_prediction(
        self,
        *,
        entities: Iterable[PredictionEntityInput],
        model: PredictionModelInput,
        binding: PredictionBindingInput | None = None,
        bonds: Iterable[PredictionBondInput] | None = None,
        constraints: Iterable[PredictionConstraintInput] | None = None,
        model_options: PredictionModelOptionsInput | None = None,
        num_samples: int | None = None,
        templates: Iterable[PredictionTemplateInput] | None = None,
        root_dir: str | PathLike[str] = "boltz-experiments",
        name: str | None = None,
        workspace_id: str | None = None,
        quiet: bool = False,
        poll_interval_seconds: float = 5.0,
    ) -> Path:
        run_dir = self.start_prediction(
            entities=entities,
            model=model,
            binding=binding,
            bonds=bonds,
            constraints=constraints,
            model_options=model_options,
            num_samples=num_samples,
            templates=templates,
            root_dir=root_dir,
            name=name,
            workspace_id=workspace_id,
            quiet=quiet,
            poll_interval_seconds=poll_interval_seconds,
        )
        return self.wait_and_download(run_dir=run_dir, quiet=quiet, poll_interval_seconds=poll_interval_seconds)

    def start_prediction(
        self,
        *,
        entities: Iterable[PredictionEntityInput],
        model: PredictionModelInput,
        binding: PredictionBindingInput | None = None,
        bonds: Iterable[PredictionBondInput] | None = None,
        constraints: Iterable[PredictionConstraintInput] | None = None,
        model_options: PredictionModelOptionsInput | None = None,
        num_samples: int | None = None,
        templates: Iterable[PredictionTemplateInput] | None = None,
        root_dir: str | PathLike[str] = "boltz-experiments",
        name: str | None = None,
        workspace_id: str | None = None,
        quiet: bool = False,
        poll_interval_seconds: float = 5.0,
    ) -> Path:
        del poll_interval_seconds
        payload = normalize_prediction_request(
            entities=entities,
            model=model,
            binding=binding,
            bonds=bonds,
            constraints=constraints,
            model_options=model_options,
            num_samples=num_samples,
            templates=templates,
        )
        return self._start_prediction(
            payload=payload,
            root_dir=root_dir,
            name=name,
            workspace_id=workspace_id,
            quiet=quiet,
        )

    def run_adme(
        self,
        *,
        input: adme_start_params.Input,
        model: Literal["adme-v1"],
        root_dir: str | PathLike[str] = "boltz-experiments",
        name: str | None = None,
        workspace_id: str | None = None,
        quiet: bool = False,
        poll_interval_seconds: float = 5.0,
    ) -> Path:
        run_dir = self.start_adme(
            input=input,
            model=model,
            root_dir=root_dir,
            name=name,
            workspace_id=workspace_id,
            quiet=quiet,
            poll_interval_seconds=poll_interval_seconds,
        )
        return self.wait_and_download(run_dir=run_dir, quiet=quiet, poll_interval_seconds=poll_interval_seconds)

    def start_adme(
        self,
        *,
        input: adme_start_params.Input,
        model: Literal["adme-v1"],
        root_dir: str | PathLike[str] = "boltz-experiments",
        name: str | None = None,
        workspace_id: str | None = None,
        quiet: bool = False,
        poll_interval_seconds: float = 5.0,
    ) -> Path:
        del poll_interval_seconds
        payload: adme_start_params.AdmeStartParams = {"input": input, "model": model}
        return self._start_adme(
            payload=payload,
            root_dir=root_dir,
            name=name,
            workspace_id=workspace_id,
            quiet=quiet,
        )

    def run_protein_design(
        self,
        *,
        binder_specification: ProteinDesignBinderSpecificationInput,
        num_proteins: int,
        target: ProteinDesignTargetInput,
        root_dir: str | PathLike[str] = "boltz-experiments",
        name: str | None = None,
        workspace_id: str | None = None,
        download_mode: DownloadMode | str | None = None,
        quiet: bool = False,
        poll_interval_seconds: float = 5.0,
    ) -> Path:
        run_dir = self.start_protein_design(
            binder_specification=binder_specification,
            num_proteins=num_proteins,
            target=target,
            root_dir=root_dir,
            name=name,
            workspace_id=workspace_id,
            download_mode=download_mode,
            quiet=quiet,
            poll_interval_seconds=poll_interval_seconds,
        )
        return self.wait_and_download(
            run_dir=run_dir,
            download_mode=download_mode,
            quiet=quiet,
            poll_interval_seconds=poll_interval_seconds,
        )

    def start_protein_design(
        self,
        *,
        binder_specification: ProteinDesignBinderSpecificationInput,
        num_proteins: int,
        target: ProteinDesignTargetInput,
        root_dir: str | PathLike[str] = "boltz-experiments",
        name: str | None = None,
        workspace_id: str | None = None,
        download_mode: DownloadMode | str | None = None,
        quiet: bool = False,
        poll_interval_seconds: float = 5.0,
    ) -> Path:
        del poll_interval_seconds
        payload = normalize_protein_design_request(
            binder_specification=binder_specification,
            num_proteins=num_proteins,
            target=target,
        )
        return self._start_pipeline(
            definition=self._protein_design_definition,
            payload=payload,
            root_dir=root_dir,
            name=name,
            workspace_id=workspace_id,
            download_mode=download_mode,
            quiet=quiet,
        )

    def run_protein_library_screen(
        self,
        *,
        proteins: Iterable[protein_library_screen_start_params.Protein],
        target: ProteinLibraryScreenTargetInput,
        root_dir: str | PathLike[str] = "boltz-experiments",
        name: str | None = None,
        workspace_id: str | None = None,
        download_mode: DownloadMode | str | None = None,
        quiet: bool = False,
        poll_interval_seconds: float = 5.0,
    ) -> Path:
        run_dir = self.start_protein_library_screen(
            proteins=proteins,
            target=target,
            root_dir=root_dir,
            name=name,
            workspace_id=workspace_id,
            download_mode=download_mode,
            quiet=quiet,
            poll_interval_seconds=poll_interval_seconds,
        )
        return self.wait_and_download(
            run_dir=run_dir,
            download_mode=download_mode,
            quiet=quiet,
            poll_interval_seconds=poll_interval_seconds,
        )

    def start_protein_library_screen(
        self,
        *,
        proteins: Iterable[protein_library_screen_start_params.Protein],
        target: ProteinLibraryScreenTargetInput,
        root_dir: str | PathLike[str] = "boltz-experiments",
        name: str | None = None,
        workspace_id: str | None = None,
        download_mode: DownloadMode | str | None = None,
        quiet: bool = False,
        poll_interval_seconds: float = 5.0,
    ) -> Path:
        del poll_interval_seconds
        payload = normalize_protein_library_screen_request(
            proteins=proteins,
            target=target,
        )
        return self._start_pipeline(
            definition=self._protein_library_screen_definition,
            payload=payload,
            root_dir=root_dir,
            name=name,
            workspace_id=workspace_id,
            download_mode=download_mode,
            quiet=quiet,
        )

    def run_small_molecule_design(
        self,
        *,
        num_molecules: int,
        target: SmallMoleculeTarget,
        chemical_space: Literal["enamine_real"] | None = None,
        molecule_filters: small_molecule_design_start_params.MoleculeFilters | None = None,
        root_dir: str | PathLike[str] = "boltz-experiments",
        name: str | None = None,
        workspace_id: str | None = None,
        download_mode: DownloadMode | str | None = None,
        quiet: bool = False,
        poll_interval_seconds: float = 5.0,
    ) -> Path:
        run_dir = self.start_small_molecule_design(
            num_molecules=num_molecules,
            target=target,
            chemical_space=chemical_space,
            molecule_filters=molecule_filters,
            root_dir=root_dir,
            name=name,
            workspace_id=workspace_id,
            download_mode=download_mode,
            quiet=quiet,
            poll_interval_seconds=poll_interval_seconds,
        )
        return self.wait_and_download(
            run_dir=run_dir,
            download_mode=download_mode,
            quiet=quiet,
            poll_interval_seconds=poll_interval_seconds,
        )

    def start_small_molecule_design(
        self,
        *,
        num_molecules: int,
        target: SmallMoleculeTarget,
        chemical_space: Literal["enamine_real"] | None = None,
        molecule_filters: small_molecule_design_start_params.MoleculeFilters | None = None,
        root_dir: str | PathLike[str] = "boltz-experiments",
        name: str | None = None,
        workspace_id: str | None = None,
        download_mode: DownloadMode | str | None = None,
        quiet: bool = False,
        poll_interval_seconds: float = 5.0,
    ) -> Path:
        del poll_interval_seconds
        payload = normalize_small_molecule_design_request(
            num_molecules=num_molecules,
            target=target,
            chemical_space=chemical_space,
            molecule_filters=molecule_filters,
        )
        return self._start_pipeline(
            definition=self._small_molecule_design_definition,
            payload=payload,
            root_dir=root_dir,
            name=name,
            workspace_id=workspace_id,
            download_mode=download_mode,
            quiet=quiet,
        )

    def run_small_molecule_library_screen(
        self,
        *,
        molecules: Iterable[small_molecule_library_screen_start_params.Molecule],
        target: SmallMoleculeTarget,
        molecule_filters: small_molecule_library_screen_start_params.MoleculeFilters | None = None,
        root_dir: str | PathLike[str] = "boltz-experiments",
        name: str | None = None,
        workspace_id: str | None = None,
        download_mode: DownloadMode | str | None = None,
        quiet: bool = False,
        poll_interval_seconds: float = 5.0,
    ) -> Path:
        run_dir = self.start_small_molecule_library_screen(
            molecules=molecules,
            target=target,
            molecule_filters=molecule_filters,
            root_dir=root_dir,
            name=name,
            workspace_id=workspace_id,
            download_mode=download_mode,
            quiet=quiet,
            poll_interval_seconds=poll_interval_seconds,
        )
        return self.wait_and_download(
            run_dir=run_dir,
            download_mode=download_mode,
            quiet=quiet,
            poll_interval_seconds=poll_interval_seconds,
        )

    def start_small_molecule_library_screen(
        self,
        *,
        molecules: Iterable[small_molecule_library_screen_start_params.Molecule],
        target: SmallMoleculeTarget,
        molecule_filters: small_molecule_library_screen_start_params.MoleculeFilters | None = None,
        root_dir: str | PathLike[str] = "boltz-experiments",
        name: str | None = None,
        workspace_id: str | None = None,
        download_mode: DownloadMode | str | None = None,
        quiet: bool = False,
        poll_interval_seconds: float = 5.0,
    ) -> Path:
        del poll_interval_seconds
        payload = normalize_small_molecule_library_screen_request(
            molecules=molecules,
            target=target,
            molecule_filters=molecule_filters,
        )
        return self._start_pipeline(
            definition=self._small_molecule_library_screen_definition,
            payload=payload,
            root_dir=root_dir,
            name=name,
            workspace_id=workspace_id,
            download_mode=download_mode,
            quiet=quiet,
        )

    def wait_and_download(
        self,
        *,
        run_dir: str | PathLike[str] | None = None,
        name: str | None = None,
        root_dir: str | PathLike[str] | None = None,
        download_mode: DownloadMode | str | None = None,
        quiet: bool = False,
        poll_interval_seconds: float = 5.0,
    ) -> Path:
        resolved_run_dir = resolve_existing_run_dir(run_dir=run_dir, name=name, root_dir=root_dir)
        metadata = load_metadata(resolved_run_dir)
        engine = ExperimentEngine(client=self._client, sink=build_progress_sink(quiet=quiet))
        normalized_download_mode = None if download_mode is None else normalize_download_mode(download_mode)

        if metadata.run_type == "prediction":
            if normalized_download_mode not in {None, DOWNLOAD_MODE_EVERYTHING}:
                raise ExperimentError("`download_mode` only supports pipeline run IDs")
            return engine.wait_for_prediction(
                definition=self._prediction_definition,
                run_dir=resolved_run_dir,
                poll_interval_seconds=poll_interval_seconds,
            )
        if metadata.run_type == "adme":
            if normalized_download_mode not in {None, DOWNLOAD_MODE_EVERYTHING}:
                raise ExperimentError("`download_mode` only supports pipeline run IDs")
            return engine.wait_for_prediction(
                definition=self._adme_prediction_definition,
                run_dir=resolved_run_dir,
                poll_interval_seconds=poll_interval_seconds,
            )
        if metadata.run_type == "protein_design":
            return engine.wait_for_pipeline(
                definition=self._protein_design_definition,
                run_dir=resolved_run_dir,
                poll_interval_seconds=poll_interval_seconds,
                download_mode=normalized_download_mode,
            )
        if metadata.run_type == "protein_library_screen":
            return engine.wait_for_pipeline(
                definition=self._protein_library_screen_definition,
                run_dir=resolved_run_dir,
                poll_interval_seconds=poll_interval_seconds,
                download_mode=normalized_download_mode,
            )
        if metadata.run_type == "small_molecule_design":
            return engine.wait_for_pipeline(
                definition=self._small_molecule_design_definition,
                run_dir=resolved_run_dir,
                poll_interval_seconds=poll_interval_seconds,
                download_mode=normalized_download_mode,
            )
        return engine.wait_for_pipeline(
            definition=self._small_molecule_library_screen_definition,
            run_dir=resolved_run_dir,
            poll_interval_seconds=poll_interval_seconds,
            download_mode=normalized_download_mode,
        )

    def download_results(
        self,
        *,
        id: str | None = None,
        run_dir: str | PathLike[str] | None = None,
        name: str | None = None,
        root_dir: str | PathLike[str] = "boltz-experiments",
        workspace_id: str | None = None,
        download_mode: DownloadMode | str | None = None,
        quiet: bool = False,
        poll_interval_seconds: float = 5.0,
    ) -> Path:
        resolved_run_dir = _resolve_download_results_run_dir(
            id=id,
            run_dir=run_dir,
            name=name,
            root_dir=root_dir,
        )
        requested_download_mode = None if download_mode is None else normalize_download_mode(download_mode)
        metadata_file = metadata_path(resolved_run_dir)

        if metadata_file.exists():
            metadata = load_metadata(resolved_run_dir)
            _reconcile_download_results_metadata(
                metadata=metadata,
                run_id=id,
                workspace_id=workspace_id,
                download_mode=requested_download_mode,
            )
        else:
            if id is None:
                raise ValueError("`id` is required when creating a download results run directory")
            run_type = infer_run_type(id)
            mode = requested_download_mode or DOWNLOAD_MODE_EVERYTHING
            if run_type in {"prediction", "adme"} and mode != DOWNLOAD_MODE_EVERYTHING:
                raise ExperimentError("`download_mode` only supports pipeline run IDs")

            ensure_directory_ready(resolved_run_dir)
            metadata = RunMetadata.create(
                name=resolved_run_dir.name,
                run_type=run_type,
                download_mode=mode,
                request_fingerprint=_download_results_fingerprint(id=id, workspace_id=workspace_id),
                idempotency_key=f"exp_{uuid.uuid4().hex}",
            )
            metadata.remote.run_id = id
            metadata.remote.workspace_id = workspace_id

        save_metadata(resolved_run_dir, metadata)
        return self.wait_and_download(
            run_dir=resolved_run_dir,
            download_mode=requested_download_mode,
            quiet=quiet,
            poll_interval_seconds=poll_interval_seconds,
        )

    def stop(
        self,
        *,
        run_dir: str | PathLike[str] | None = None,
        name: str | None = None,
        root_dir: str | PathLike[str] | None = None,
        quiet: bool = False,
    ) -> Path:
        resolved_run_dir = resolve_existing_run_dir(run_dir=run_dir, name=name, root_dir=root_dir)
        metadata = load_metadata(resolved_run_dir)
        engine = ExperimentEngine(client=self._client, sink=build_progress_sink(quiet=quiet))

        if metadata.run_type in {"prediction", "adme"}:
            unsupported_stop(metadata.run_type)
        if metadata.run_type == "protein_design":
            return engine.stop_pipeline(definition=self._protein_design_definition, run_dir=resolved_run_dir)
        if metadata.run_type == "protein_library_screen":
            return engine.stop_pipeline(
                definition=self._protein_library_screen_definition,
                run_dir=resolved_run_dir,
            )
        if metadata.run_type == "small_molecule_design":
            return engine.stop_pipeline(
                definition=self._small_molecule_design_definition,
                run_dir=resolved_run_dir,
            )
        return engine.stop_pipeline(
            definition=self._small_molecule_library_screen_definition,
            run_dir=resolved_run_dir,
        )

    def _start_prediction(
        self,
        *,
        payload: structure_and_binding_start_params.StructureAndBindingStartParams,
        root_dir: str | PathLike[str],
        name: str | None,
        workspace_id: str | None,
        quiet: bool,
    ) -> Path:
        run_dir = resolve_create_run_dir(root_dir, name)
        engine = ExperimentEngine(client=self._client, sink=build_progress_sink(quiet=quiet))
        return engine.start_prediction(
            definition=self._prediction_definition,
            run_dir=run_dir,
            request_payload=payload,
            request_fingerprint=fingerprint_payload(payload),
            workspace_id=workspace_id,
        )

    def _start_adme(
        self,
        *,
        payload: adme_start_params.AdmeStartParams,
        root_dir: str | PathLike[str],
        name: str | None,
        workspace_id: str | None,
        quiet: bool,
    ) -> Path:
        run_dir = resolve_create_run_dir(root_dir, name)
        engine = ExperimentEngine(client=self._client, sink=build_progress_sink(quiet=quiet))
        return engine.start_prediction(
            definition=self._adme_prediction_definition,
            run_dir=run_dir,
            request_payload=payload,
            request_fingerprint=fingerprint_payload(payload),
            workspace_id=workspace_id,
        )

    def _start_pipeline(
        self,
        *,
        definition: PipelineDefinition[_PipelinePayloadT],
        payload: _PipelinePayloadT,
        root_dir: str | PathLike[str],
        name: str | None,
        workspace_id: str | None,
        download_mode: DownloadMode | str | None,
        quiet: bool,
    ) -> Path:
        run_dir = resolve_create_run_dir(root_dir, name)
        engine = ExperimentEngine(client=self._client, sink=build_progress_sink(quiet=quiet))
        return engine.start_pipeline(
            definition=definition,
            run_dir=run_dir,
            request_payload=payload,
            request_fingerprint=fingerprint_payload(payload),
            workspace_id=workspace_id,
            download_mode=None if download_mode is None else normalize_download_mode(download_mode),
        )

    @staticmethod
    def _prediction_start_call(
        client: Boltz,
        payload: structure_and_binding_start_params.StructureAndBindingStartParams,
        key: str,
        workspace_id: str | None,
    ) -> structure_and_binding_start_response.StructureAndBindingStartResponse:
        return client.predictions.structure_and_binding.start(
            input=payload["input"],
            model=payload["model"],
            idempotency_key=key,
            **_workspace_kwargs(workspace_id),
        )

    @staticmethod
    def _prediction_retrieve_call(
        client: Boltz,
        run_id: str,
        workspace_id: str | None,
    ) -> structure_and_binding_retrieve_response.StructureAndBindingRetrieveResponse:
        return client.predictions.structure_and_binding.retrieve(run_id, **_workspace_kwargs(workspace_id))

    @staticmethod
    def _adme_start_call(
        client: Boltz,
        payload: adme_start_params.AdmeStartParams,
        key: str,
        workspace_id: str | None,
    ) -> adme_start_response.AdmeStartResponse:
        return client.predictions.adme.start(
            input=payload["input"],
            model=payload["model"],
            idempotency_key=key,
            **_workspace_kwargs(workspace_id),
        )

    @staticmethod
    def _adme_retrieve_call(
        client: Boltz,
        run_id: str,
        workspace_id: str | None,
    ) -> adme_retrieve_response.AdmeRetrieveResponse:
        return client.predictions.adme.retrieve(run_id, **_workspace_kwargs(workspace_id))

    @staticmethod
    def _protein_design_start_call(
        client: Boltz,
        payload: protein_design_start_params.ProteinDesignRunInput,
        key: str,
        workspace_id: str | None,
    ) -> protein_design_start_response.DesignStartResponse:
        return client.protein.design.start(
            binder_specification=payload["binder_specification"],
            num_proteins=payload["num_proteins"],
            target=payload["target"],
            idempotency_key=key,
            **_workspace_kwargs(workspace_id),
        )

    @staticmethod
    def _protein_design_retrieve_call(
        client: Boltz,
        run_id: str,
        workspace_id: str | None,
    ) -> protein_design_retrieve_response.DesignRetrieveResponse:
        return client.protein.design.retrieve(run_id, **_workspace_kwargs(workspace_id))

    @staticmethod
    def _protein_design_list_results_call(
        client: Boltz,
        run_id: str,
        workspace_id: str | None,
        limit: int,
        after_id: str | None,
    ) -> SyncCursorPage[protein_design_list_results_response.DesignListResultsResponse]:
        return client.protein.design.list_results(
            run_id,
            limit=limit,
            **_workspace_after_kwargs(workspace_id, after_id),
        )

    @staticmethod
    def _protein_design_stop_call(
        client: Boltz,
        run_id: str,
    ) -> protein_design_stop_response.DesignStopResponse:
        return client.protein.design.stop(run_id)

    @staticmethod
    def _protein_library_screen_start_call(
        client: Boltz,
        payload: protein_library_screen_start_params.LibraryScreenStartParams,
        key: str,
        workspace_id: str | None,
    ) -> protein_library_screen_start_response.LibraryScreenStartResponse:
        return client.protein.library_screen.start(
            proteins=payload["proteins"],
            target=payload["target"],
            idempotency_key=key,
            **_workspace_kwargs(workspace_id),
        )

    @staticmethod
    def _protein_library_screen_retrieve_call(
        client: Boltz,
        run_id: str,
        workspace_id: str | None,
    ) -> protein_library_screen_retrieve_response.LibraryScreenRetrieveResponse:
        return client.protein.library_screen.retrieve(run_id, **_workspace_kwargs(workspace_id))

    @staticmethod
    def _protein_library_screen_list_results_call(
        client: Boltz,
        run_id: str,
        workspace_id: str | None,
        limit: int,
        after_id: str | None,
    ) -> SyncCursorPage[protein_library_screen_list_results_response.LibraryScreenListResultsResponse]:
        return client.protein.library_screen.list_results(
            run_id,
            limit=limit,
            **_workspace_after_kwargs(workspace_id, after_id),
        )

    @staticmethod
    def _protein_library_screen_stop_call(
        client: Boltz,
        run_id: str,
    ) -> protein_library_screen_stop_response.LibraryScreenStopResponse:
        return client.protein.library_screen.stop(run_id)

    @staticmethod
    def _small_molecule_design_start_call(
        client: Boltz,
        payload: small_molecule_design_start_params.DesignStartParams,
        key: str,
        workspace_id: str | None,
    ) -> small_molecule_design_start_response.DesignStartResponse:
        return client.small_molecule.design.start(
            num_molecules=payload["num_molecules"],
            target=payload["target"],
            idempotency_key=key,
            **_small_molecule_design_start_kwargs(payload, workspace_id),
        )

    @staticmethod
    def _small_molecule_design_retrieve_call(
        client: Boltz,
        run_id: str,
        workspace_id: str | None,
    ) -> small_molecule_design_retrieve_response.DesignRetrieveResponse:
        return client.small_molecule.design.retrieve(run_id, **_workspace_kwargs(workspace_id))

    @staticmethod
    def _small_molecule_design_list_results_call(
        client: Boltz,
        run_id: str,
        workspace_id: str | None,
        limit: int,
        after_id: str | None,
    ) -> SyncCursorPage[small_molecule_design_list_results_response.DesignListResultsResponse]:
        return client.small_molecule.design.list_results(
            run_id,
            limit=limit,
            **_workspace_after_kwargs(workspace_id, after_id),
        )

    @staticmethod
    def _small_molecule_design_stop_call(
        client: Boltz,
        run_id: str,
    ) -> small_molecule_design_stop_response.DesignStopResponse:
        return client.small_molecule.design.stop(run_id)

    @staticmethod
    def _small_molecule_library_screen_start_call(
        client: Boltz,
        payload: small_molecule_library_screen_start_params.LibraryScreenStartParams,
        key: str,
        workspace_id: str | None,
    ) -> small_molecule_library_screen_start_response.LibraryScreenStartResponse:
        return client.small_molecule.library_screen.start(
            molecules=payload["molecules"],
            target=payload["target"],
            idempotency_key=key,
            **_small_molecule_library_screen_start_kwargs(payload, workspace_id),
        )

    @staticmethod
    def _small_molecule_library_screen_retrieve_call(
        client: Boltz,
        run_id: str,
        workspace_id: str | None,
    ) -> small_molecule_library_screen_retrieve_response.LibraryScreenRetrieveResponse:
        return client.small_molecule.library_screen.retrieve(run_id, **_workspace_kwargs(workspace_id))

    @staticmethod
    def _small_molecule_library_screen_list_results_call(
        client: Boltz,
        run_id: str,
        workspace_id: str | None,
        limit: int,
        after_id: str | None,
    ) -> SyncCursorPage[small_molecule_library_screen_list_results_response.LibraryScreenListResultsResponse]:
        return client.small_molecule.library_screen.list_results(
            run_id,
            limit=limit,
            **_workspace_after_kwargs(workspace_id, after_id),
        )

    @staticmethod
    def _small_molecule_library_screen_stop_call(
        client: Boltz,
        run_id: str,
    ) -> small_molecule_library_screen_stop_response.LibraryScreenStopResponse:
        return client.small_molecule.library_screen.stop(run_id)


def _workspace_kwargs(workspace_id: str | None) -> _WorkspaceKwargs:
    kwargs: _WorkspaceKwargs = {}
    if workspace_id is not None:
        kwargs["workspace_id"] = workspace_id
    return kwargs


def _workspace_after_kwargs(workspace_id: str | None, after_id: str | None) -> _WorkspaceAfterKwargs:
    kwargs: _WorkspaceAfterKwargs = {}
    if workspace_id is not None:
        kwargs["workspace_id"] = workspace_id
    if after_id is not None:
        kwargs["after_id"] = after_id
    return kwargs


def _small_molecule_design_start_kwargs(
    payload: small_molecule_design_start_params.DesignStartParams,
    workspace_id: str | None,
) -> _SmallMoleculeDesignStartKwargs:
    kwargs: _SmallMoleculeDesignStartKwargs = {}
    if payload.get("chemical_space") == "enamine_real":
        kwargs["chemical_space"] = "enamine_real"
    if "molecule_filters" in payload:
        kwargs["molecule_filters"] = payload["molecule_filters"]
    if workspace_id is not None:
        kwargs["workspace_id"] = workspace_id
    return kwargs


def _small_molecule_library_screen_start_kwargs(
    payload: small_molecule_library_screen_start_params.LibraryScreenStartParams,
    workspace_id: str | None,
) -> _SmallMoleculeLibraryScreenStartKwargs:
    kwargs: _SmallMoleculeLibraryScreenStartKwargs = {}
    if "molecule_filters" in payload:
        kwargs["molecule_filters"] = payload["molecule_filters"]
    if workspace_id is not None:
        kwargs["workspace_id"] = workspace_id
    return kwargs


def infer_run_type(run_id: str) -> RunType:
    if run_id.startswith("adme_pred_"):
        return "adme"
    if run_id.startswith(("sab_pred_", "pred_")):
        return "prediction"
    if run_id.startswith("prot_des_"):
        return "protein_design"
    if run_id.startswith("prot_scr_"):
        return "protein_library_screen"
    if run_id.startswith("sm_des_"):
        return "small_molecule_design"
    if run_id.startswith("sm_scr_"):
        return "small_molecule_library_screen"
    if run_id.startswith(("pres_", "psmp_")):
        raise ExperimentError("Legacy run IDs are not supported by `download_results`")
    raise ExperimentError(f"Unable to infer experiment type from run ID: {run_id!r}")


def _resolve_download_results_run_dir(
    *,
    id: str | None,
    run_dir: str | PathLike[str] | None,
    name: str | None,
    root_dir: str | PathLike[str],
) -> Path:
    if run_dir is not None:
        if name is not None:
            raise ValueError("`name` cannot be provided when `run_dir` is used")
        return _resolve_path(Path(run_dir))
    if name is not None:
        return resolve_create_run_dir(root_dir, name)
    if id is not None:
        return resolve_create_run_dir(root_dir, None, run_id=id)
    raise ValueError("One of `id`, `run_dir`, or `name` must be provided")


def _reconcile_download_results_metadata(
    *,
    metadata: RunMetadata,
    run_id: str | None,
    workspace_id: str | None,
    download_mode: DownloadMode | None,
) -> None:
    if run_id is not None and metadata.remote.run_id not in {None, run_id}:
        raise ExperimentError(f"Run directory belongs to remote run {metadata.remote.run_id}, not {run_id}")
    if run_id is not None:
        metadata.remote.run_id = run_id

    if workspace_id is not None and metadata.remote.workspace_id not in {None, workspace_id}:
        raise ExperimentError(f"Run directory belongs to workspace {metadata.remote.workspace_id}, not {workspace_id}")
    if workspace_id is not None:
        metadata.remote.workspace_id = workspace_id

    metadata.download_mode = normalize_download_mode(metadata.download_mode)
    if metadata.run_type in {"prediction", "adme"} and metadata.download_mode != DOWNLOAD_MODE_EVERYTHING:
        raise ExperimentError("`download_mode` only supports pipeline run IDs")
    if metadata.run_type in {"prediction", "adme"} and download_mode not in {None, DOWNLOAD_MODE_EVERYTHING}:
        raise ExperimentError("`download_mode` only supports pipeline run IDs")
    if download_mode is not None and metadata.download_mode != download_mode:
        raise ExperimentError(f"Run directory uses download mode {metadata.download_mode}, not {download_mode}")


def _download_results_fingerprint(*, id: str, workspace_id: str | None) -> str:
    workspace = "" if workspace_id is None else workspace_id
    return f"download-results:{id}:{workspace}"


def _resolve_path(path: Path) -> Path:
    expanded = path.expanduser()
    if expanded.is_absolute():
        return expanded
    return (Path.cwd() / expanded).resolve()
