from __future__ import annotations

from typing import Any, cast
from pathlib import Path

from boltz_api import Boltz

client = Boltz(api_key="test")

adme_path: Path = client.predictions.adme.run(
    input={"molecules": []},
    model="adme-v1",
)
prediction_path: Path = client.predictions.structure_and_binding.run(
    input=cast(Any, {"entities": []}),
    model="boltz-2.1",
)
protein_design_path: Path = client.protein.design.run(
    binder_specification=cast(Any, {}),
    num_proteins=1,
    target=cast(Any, {}),
)
protein_design_uniformly_sampled_path: Path = client.protein.design.run(
    binder_specification={
        "type": "uniformly_sampled_specifications",
        "binder_specifications": [{"type": "boltz_curated", "binder": "boltz_nanobody"}],
    },
    num_proteins=1,
    target=cast(Any, {}),
)
protein_screen_path: Path = client.protein.library_screen.run(
    proteins=[],
    target=cast(Any, {}),
)
small_molecule_design_path: Path = client.small_molecule.design.run(
    num_molecules=1,
    target=cast(Any, {}),
)
small_molecule_screen_path: Path = client.small_molecule.library_screen.run(
    molecules=[],
    target=cast(Any, {}),
)
