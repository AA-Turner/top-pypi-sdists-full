from __future__ import annotations

from os import PathLike
from typing import Any
from pathlib import Path
from collections.abc import Callable, Iterable
from typing_extensions import Literal

from .._types import Omit, omit
from ..types.protein import (
    design_start_params as protein_design_start_params,
    library_screen_start_params as protein_library_screen_start_params,
)
from ..types.predictions import adme_start_params, structure_and_binding_start_params
from ..experiments._state import DownloadMode
from ..types.small_molecule import (
    design_start_params as small_molecule_design_start_params,
    library_screen_start_params as small_molecule_library_screen_start_params,
)
from ..resources.protein.design import DesignResource as ProteinDesignResource
from ..resources.predictions.adme import AdmeResource
from ..resources.small_molecule.design import DesignResource as SmallMoleculeDesignResource
from ..resources.protein.library_screen import LibraryScreenResource as ProteinLibraryScreenResource
from ..resources.small_molecule.library_screen import LibraryScreenResource as SmallMoleculeLibraryScreenResource
from ..resources.predictions.structure_and_binding import StructureAndBindingResource

_installed = False
CUSTOM_METHOD_MARKER = "__boltz_api_custom_method__"


def install_resource_run_methods() -> None:
    global _installed
    if _installed:
        return

    _install_method(StructureAndBindingResource, "run", _run_structure_and_binding)
    _install_method(AdmeResource, "run", _run_adme)
    _install_method(ProteinDesignResource, "run", _run_protein_design)
    _install_method(ProteinLibraryScreenResource, "run", _run_protein_library_screen)
    _install_method(SmallMoleculeDesignResource, "run", _run_small_molecule_design)
    _install_method(SmallMoleculeLibraryScreenResource, "run", _run_small_molecule_library_screen)

    _installed = True


def _custom_method(method: Callable[..., Path]) -> Callable[..., Path]:
    setattr(method, CUSTOM_METHOD_MARKER, True)
    return method


def _install_method(resource_class: type[Any], name: str, method: Callable[..., Path]) -> None:
    setattr(resource_class, name, method)


@_custom_method
def _run_structure_and_binding(
    self: StructureAndBindingResource,
    *,
    input: structure_and_binding_start_params.Input,
    model: Literal["boltz-2.1"],
    root_dir: str | PathLike[str] = "boltz-experiments",
    name: str | None = None,
    workspace_id: str | Omit = omit,
    quiet: bool = False,
    poll_interval_seconds: float = 5.0,
) -> Path:
    """Start a structure-and-binding prediction, wait for completion, and download results."""
    return self._client.experiments.run_prediction(
        entities=input["entities"],
        model=model,
        binding=input.get("binding"),
        bonds=input.get("bonds"),
        constraints=input.get("constraints"),
        model_options=input.get("model_options"),
        num_samples=input.get("num_samples"),
        templates=input.get("templates"),
        root_dir=root_dir,
        name=name,
        workspace_id=_workspace_id_or_none(workspace_id),
        quiet=quiet,
        poll_interval_seconds=poll_interval_seconds,
    )


@_custom_method
def _run_adme(
    self: AdmeResource,
    *,
    input: adme_start_params.Input,
    model: Literal["adme-v1"],
    root_dir: str | PathLike[str] = "boltz-experiments",
    name: str | None = None,
    workspace_id: str | Omit = omit,
    quiet: bool = False,
    poll_interval_seconds: float = 5.0,
) -> Path:
    """Start an ADME prediction, wait for completion, and persist results."""
    return self._client.experiments.run_adme(
        input=input,
        model=model,
        root_dir=root_dir,
        name=name,
        workspace_id=_workspace_id_or_none(workspace_id),
        quiet=quiet,
        poll_interval_seconds=poll_interval_seconds,
    )


@_custom_method
def _run_protein_design(
    self: ProteinDesignResource,
    *,
    binder_specification: protein_design_start_params.ProteinDesignRunInputBinderSpecification,
    num_proteins: int,
    target: protein_design_start_params.ProteinDesignRunInputTarget,
    root_dir: str | PathLike[str] = "boltz-experiments",
    name: str | None = None,
    workspace_id: str | Omit = omit,
    download_mode: DownloadMode | str | None = None,
    quiet: bool = False,
    poll_interval_seconds: float = 5.0,
) -> Path:
    """Start a protein design run, wait for completion, and download results."""
    return self._client.experiments.run_protein_design(
        binder_specification=binder_specification,
        num_proteins=num_proteins,
        target=target,
        root_dir=root_dir,
        name=name,
        workspace_id=_workspace_id_or_none(workspace_id),
        download_mode=download_mode,
        quiet=quiet,
        poll_interval_seconds=poll_interval_seconds,
    )


@_custom_method
def _run_protein_library_screen(
    self: ProteinLibraryScreenResource,
    *,
    proteins: Iterable[protein_library_screen_start_params.Protein],
    target: protein_library_screen_start_params.Target,
    root_dir: str | PathLike[str] = "boltz-experiments",
    name: str | None = None,
    workspace_id: str | Omit = omit,
    download_mode: DownloadMode | str | None = None,
    quiet: bool = False,
    poll_interval_seconds: float = 5.0,
) -> Path:
    """Start a protein library screen, wait for completion, and download results."""
    return self._client.experiments.run_protein_library_screen(
        proteins=proteins,
        target=target,
        root_dir=root_dir,
        name=name,
        workspace_id=_workspace_id_or_none(workspace_id),
        download_mode=download_mode,
        quiet=quiet,
        poll_interval_seconds=poll_interval_seconds,
    )


@_custom_method
def _run_small_molecule_design(
    self: SmallMoleculeDesignResource,
    *,
    num_molecules: int,
    target: small_molecule_design_start_params.Target,
    chemical_space: Literal["enamine_real"] | None = None,
    molecule_filters: small_molecule_design_start_params.MoleculeFilters | None = None,
    root_dir: str | PathLike[str] = "boltz-experiments",
    name: str | None = None,
    workspace_id: str | Omit = omit,
    download_mode: DownloadMode | str | None = None,
    quiet: bool = False,
    poll_interval_seconds: float = 5.0,
) -> Path:
    """Start a small-molecule design run, wait for completion, and download results."""
    return self._client.experiments.run_small_molecule_design(
        num_molecules=num_molecules,
        target=target,
        chemical_space=chemical_space,
        molecule_filters=molecule_filters,
        root_dir=root_dir,
        name=name,
        workspace_id=_workspace_id_or_none(workspace_id),
        download_mode=download_mode,
        quiet=quiet,
        poll_interval_seconds=poll_interval_seconds,
    )


@_custom_method
def _run_small_molecule_library_screen(
    self: SmallMoleculeLibraryScreenResource,
    *,
    molecules: Iterable[small_molecule_library_screen_start_params.Molecule],
    target: small_molecule_library_screen_start_params.Target,
    molecule_filters: small_molecule_library_screen_start_params.MoleculeFilters | None = None,
    root_dir: str | PathLike[str] = "boltz-experiments",
    name: str | None = None,
    workspace_id: str | Omit = omit,
    download_mode: DownloadMode | str | None = None,
    quiet: bool = False,
    poll_interval_seconds: float = 5.0,
) -> Path:
    """Start a small-molecule library screen, wait for completion, and download results."""
    return self._client.experiments.run_small_molecule_library_screen(
        molecules=molecules,
        target=target,
        molecule_filters=molecule_filters,
        root_dir=root_dir,
        name=name,
        workspace_id=_workspace_id_or_none(workspace_id),
        download_mode=download_mode,
        quiet=quiet,
        poll_interval_seconds=poll_interval_seconds,
    )


def _workspace_id_or_none(workspace_id: str | Omit) -> str | None:
    if isinstance(workspace_id, Omit):
        return None
    return workspace_id
