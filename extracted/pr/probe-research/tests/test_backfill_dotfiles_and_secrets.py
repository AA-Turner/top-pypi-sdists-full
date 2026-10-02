"""Dotfiles are counted, and samples are scrubbed before they leave read_head.

Two halves of one change. Admitting dotfiles is what makes the census honest;
scrubbing is what keeps admitting them from shipping credentials, because the
files newly admitted are exactly the ones that carry keys in an ML folder.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from probe.cli import backfill_evidence as ev


def _walk(root: Path):
    warn = ev.WalkWarnings()
    return sorted(str(Path(f.path).relative_to(root)) for f in ev.walk(root, warn=warn)), warn


def test_hydra_config_is_walked_and_counted(tmp_path):
    """The file that NAMES a Hydra experiment. A blanket dotfile skip dropped
    it from the evidence AND from the denominator."""
    (tmp_path / ".hydra").mkdir()
    (tmp_path / ".hydra" / "config.yaml").write_text("experiment: odyssey3-infill\n")
    (tmp_path / "train.py").write_text("print(1)\n")
    found, _warn = _walk(tmp_path)
    assert ".hydra/config.yaml" in found
    assert len(found) == 2, "and it is in the census, not merely readable"


def test_other_meaningful_dotfiles_survive(tmp_path):
    for name in (".condarc", ".dvcignore", ".gitignore"):
        (tmp_path / name).write_text("x\n")
    found, _warn = _walk(tmp_path)
    assert set(found) == {".condarc", ".dvcignore", ".gitignore"}


def test_machine_written_dot_directories_are_still_skipped(tmp_path):
    """What is dropped is now a named decision in SKIP_DIRS, not a side effect
    of the leading character."""
    for d in (".git", ".cache", ".venv", ".ruff_cache"):
        (tmp_path / d).mkdir()
        (tmp_path / d / "junk").write_text("x\n")
    (tmp_path / "real.py").write_text("x\n")
    found, _warn = _walk(tmp_path)
    assert found == ["real.py"]


def test_a_dot_directory_we_admit_is_descended_into(tmp_path):
    (tmp_path / ".dvc").mkdir()
    (tmp_path / ".dvc" / "config").write_text("remote: s3://bucket\n")
    found, _warn = _walk(tmp_path)
    assert ".dvc/config" in found


# -- the scrub ---------------------------------------------------------------


def test_a_wandb_key_in_a_hydra_config_never_reaches_the_sample(tmp_path):
    """The live exposure: evidence goes into an agent prompt and the captured
    transcript, neither of which passes the ingest redaction gate."""
    config = tmp_path / "config.yaml"
    config.write_text(
        "experiment: odyssey3\n"
        "wandb_api_key: 9f8e7d6c5b4a39281706f5e4d3c2b1a099887766\n"
        "batch_size: 32\n"
    )
    head = ev.read_head(str(config))
    assert "9f8e7d6c5b4a39281706f5e4d3c2b1a099887766" not in head
    assert "odyssey3" in head, "the classification signal survives the scrub"
    assert "batch_size: 32" in head


def test_vendor_shaped_tokens_are_caught_by_prefix(tmp_path):
    f = tmp_path / "notes.md"
    f.write_text("keys: ghp_abcdefghijklmnopqrstuvwxyz0123 and AKIA1234567890ABCDEF\n")
    head = ev.read_head(str(f))
    assert "ghp_abcdefghijklmnopqrstuvwxyz0123" not in head
    assert "AKIA1234567890ABCDEF" not in head


def test_ordinary_research_prose_is_not_eaten(tmp_path):
    """A scrub that mangles evidence destroys the classification it protects.
    This is the false-positive guard."""
    f = tmp_path / "README.md"
    original = (
        "# Odyssey 3 Reconstruction\n"
        "Infill baseline for the 1B model replacement. Seeds 0-4, lr 3e-4.\n"
        "See runs/2026-05-14 for the ablation.\n"
    )
    f.write_text(original)
    assert ev.read_head(str(f)) == original.strip()


def test_binary_is_still_rejected_before_any_scrubbing(tmp_path):
    f = tmp_path / "weights.bin"
    f.write_bytes(b"\x00\x01\x02binary")
    assert ev.read_head(str(f)) is None


def test_an_env_file_was_never_sampled_and_still_is_not(tmp_path):
    """Filename filtering would have guarded a door already locked: `.env` is
    TAIL because its suffix is not evidence and its stem is empty."""
    assert ev.tier_for(".env", 100) is ev.Tier.TAIL
    assert ev.tier_for("secrets.env", 100) is ev.Tier.TAIL


# -- the door the sample-scrub does not cover --------------------------------
#
# Scrubbing protects SAMPLES. A file that is never sampled is still walked,
# inherited into a project, manifested and UPLOADED WHOLE -- the upload reads
# bytes off disk and never looks at a sample. So admitting dotfiles had to be
# paired with refusing to walk the ones that are credentials, not with tiering.


@pytest.mark.parametrize(
    "rel",
    [
        ".ssh/id_rsa",
        ".aws/credentials",
        ".gnupg/secring.gpg",
        ".kube/config",
        ".docker/config.json",
        ".config/gh/hosts.yml",
    ],
)
def test_credential_directories_are_never_walked(tmp_path, rel):
    (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / rel).write_text("SECRET")
    (tmp_path / "real.py").write_text("x")
    found, _warn = _walk(tmp_path)
    assert found == ["real.py"], f"{rel} reached the walk, and would be uploaded"


@pytest.mark.parametrize(
    "name",
    [".env", ".envrc", ".netrc", ".git-credentials", ".pypirc", ".npmrc", ".pgpass"],
)
def test_credential_files_are_never_walked(tmp_path, name):
    (tmp_path / name).write_text("TOKEN=live")
    (tmp_path / "real.py").write_text("x")
    found, _warn = _walk(tmp_path)
    assert found == ["real.py"], f"{name} reached the walk, and would be uploaded"


@pytest.mark.parametrize("name", ["server.pem", "private.key", "bundle.p12", "store.jks"])
def test_private_key_suffixes_are_never_walked(tmp_path, name):
    (tmp_path / name).write_text("-----BEGIN PRIVATE KEY-----")
    (tmp_path / "real.py").write_text("x")
    found, _warn = _walk(tmp_path)
    assert found == ["real.py"], f"{name} reached the walk, and would be uploaded"


def test_a_credential_file_is_absent_from_the_census_too(tmp_path):
    """Not merely unsampled. It must not be counted, assigned, or manifested."""
    (tmp_path / ".env").write_text("WANDB_API_KEY=live")
    (tmp_path / "readme.md").write_text("hi")
    evidence = ev.gather(tmp_path)
    assert evidence.total_files == 1
    assert all(".env" not in f.path for f in evidence.files)
