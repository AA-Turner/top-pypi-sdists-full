"""Tests for binding-affinity workflow settings."""

from stjames.workflows.binding_affinity import BindingAffinityWorkflow

PROTEIN_UUID = "1a9f9ed1-932c-4864-9af5-e81d55a3433d"


def test_binding_affinity_settings_discriminator() -> None:
    """Parse each binding-affinity method through the workflow discriminator."""
    sqm = BindingAffinityWorkflow(
        protein=PROTEIN_UUID,
        ligand_residue_name="LIG",
        ligand_smiles=["CCO"],
    )
    gnina = BindingAffinityWorkflow.model_validate(
        {
            "protein": PROTEIN_UUID,
            "ligand_residue_name": "LIG",
            "ligand_smiles": ["CCO"],
            "binding_affinity_settings": {"settings_type": "gnina"},
        }
    )
    aev_plig = BindingAffinityWorkflow.model_validate(
        {
            "protein": PROTEIN_UUID,
            "ligand_residue_name": "LIG",
            "ligand_smiles": ["CCO"],
            "binding_affinity_settings": {"settings_type": "aev_plig"},
        }
    )
    nesso = BindingAffinityWorkflow.model_validate(
        {
            "protein_sequences": ["ACDEFGHIK"],
            "ligand_smiles": ["CCO"],
            "binding_affinity_settings": {"settings_type": "nesso"},
        }
    )

    assert sqm.binding_affinity_settings.settings_type == "single_point_energy"
    assert gnina.binding_affinity_settings.settings_type == "gnina"
    assert gnina.model_dump(mode="json")["binding_affinity_settings"] == {"settings_type": "gnina"}
    assert aev_plig.binding_affinity_settings.settings_type == "aev_plig"
    assert aev_plig.model_dump(mode="json")["binding_affinity_settings"] == {"settings_type": "aev_plig"}
    assert nesso.binding_affinity_settings.settings_type == "nesso"
    assert nesso.model_dump(mode="json")["binding_affinity_settings"] == {"settings_type": "nesso"}
