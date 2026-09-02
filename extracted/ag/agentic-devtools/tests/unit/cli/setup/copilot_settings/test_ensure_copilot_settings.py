import json

from agentic_devtools.cli.setup.copilot_settings import (
    _MARKETPLACE_NAME,
    _MARKETPLACE_SOURCE,
    _PLUGIN_KEY,
    _parse_top_level_members,
    ensure_copilot_settings,
)

_EXPECTED_PLUGINS = {_PLUGIN_KEY: True}
_EXPECTED_MARKETPLACES = {_MARKETPLACE_NAME: {"source": _MARKETPLACE_SOURCE}}


def test_creates_when_absent(tmp_path):
    assert ensure_copilot_settings(tmp_path)
    file_path = tmp_path / ".github" / "copilot" / "settings.json"
    assert file_path.exists()
    data = json.loads(file_path.read_text(encoding="utf-8"))
    assert data["enabledPlugins"] == _EXPECTED_PLUGINS
    assert data["extraKnownMarketplaces"] == _EXPECTED_MARKETPLACES


def test_merges_when_present_and_preserves_unrelated_key(tmp_path):
    copilot_dir = tmp_path / ".github" / "copilot"
    copilot_dir.mkdir(parents=True)
    settings_file = copilot_dir / "settings.json"
    settings_file.write_text('{\n    "unrelatedKey": "value",\n    "contextTier" : "default"\n}\n', encoding="utf-8")

    assert ensure_copilot_settings(tmp_path)

    updated = settings_file.read_text(encoding="utf-8")
    data = json.loads(updated)
    assert data["unrelatedKey"] == "value"
    assert data["contextTier"] == "default"
    assert data["enabledPlugins"] == _EXPECTED_PLUGINS
    assert data["extraKnownMarketplaces"] == _EXPECTED_MARKETPLACES
    assert '"contextTier" : "default"' in updated


def test_idempotent(tmp_path):
    assert ensure_copilot_settings(tmp_path)
    first_pass = (tmp_path / ".github" / "copilot" / "settings.json").read_text(encoding="utf-8")
    # second run produces no change
    assert not ensure_copilot_settings(tmp_path)
    assert (tmp_path / ".github" / "copilot" / "settings.json").read_text(encoding="utf-8") == first_pass


def test_handles_non_dict_json(tmp_path, capsys):
    copilot_dir = tmp_path / ".github" / "copilot"
    copilot_dir.mkdir(parents=True)
    settings_file = copilot_dir / "settings.json"
    settings_file.write_text("[]", encoding="utf-8")

    assert not ensure_copilot_settings(tmp_path)
    assert "is not a JSON object" in capsys.readouterr().err


def test_handles_invalid_json(tmp_path, capsys):
    copilot_dir = tmp_path / ".github" / "copilot"
    copilot_dir.mkdir(parents=True)
    settings_file = copilot_dir / "settings.json"
    settings_file.write_text("{", encoding="utf-8")

    assert not ensure_copilot_settings(tmp_path)
    assert "Failed to read" in capsys.readouterr().err


def test_handles_creation_error(tmp_path, capsys, monkeypatch):
    def raise_os_error(*_args, **_kwargs):
        raise OSError("boom")

    monkeypatch.setattr("agentic_devtools.cli.setup.copilot_settings.atomic_write", raise_os_error)

    assert not ensure_copilot_settings(tmp_path)
    assert "Failed to create" in capsys.readouterr().err


def test_handles_write_error(tmp_path, capsys, monkeypatch):
    copilot_dir = tmp_path / ".github" / "copilot"
    copilot_dir.mkdir(parents=True)
    settings_file = copilot_dir / "settings.json"
    settings_file.write_text("{}", encoding="utf-8")

    def raise_os_error(*_args, **_kwargs):
        raise OSError("boom")

    monkeypatch.setattr("agentic_devtools.cli.setup.copilot_settings.atomic_write", raise_os_error)

    assert not ensure_copilot_settings(tmp_path)
    assert "Failed to write" in capsys.readouterr().err


def test_handles_empty_file(tmp_path):
    copilot_dir = tmp_path / ".github" / "copilot"
    copilot_dir.mkdir(parents=True)
    settings_file = copilot_dir / "settings.json"
    settings_file.write_text("", encoding="utf-8")

    assert ensure_copilot_settings(tmp_path)
    data = json.loads(settings_file.read_text(encoding="utf-8"))
    assert data["enabledPlugins"] == _EXPECTED_PLUGINS


def test_merges_existing_plugin_objects(tmp_path):
    """Entries added by other tools are preserved; our keys are added if absent."""
    copilot_dir = tmp_path / ".github" / "copilot"
    copilot_dir.mkdir(parents=True)
    settings_file = copilot_dir / "settings.json"
    settings_file.write_text(
        json.dumps(
            {
                "enabledPlugins": {"other/plugin@other-marketplace": True},
                "extraKnownMarketplaces": {
                    "other-marketplace": {"source": {"source": "github", "repo": "other/example-plugin"}}
                },
            }
        ),
        encoding="utf-8",
    )

    assert ensure_copilot_settings(tmp_path)

    data = json.loads(settings_file.read_text(encoding="utf-8"))
    # Pre-existing entries must be preserved
    assert data["enabledPlugins"]["other/plugin@other-marketplace"] is True
    assert data["extraKnownMarketplaces"]["other-marketplace"] == {
        "source": {"source": "github", "repo": "other/example-plugin"}
    }
    # Our entries must be added
    assert data["enabledPlugins"][_PLUGIN_KEY] is True
    assert data["extraKnownMarketplaces"][_MARKETPLACE_NAME] == {"source": _MARKETPLACE_SOURCE}


def test_does_not_overwrite_existing_plugin_key(tmp_path):
    """If our key is already present (idempotency), the file is not rewritten."""
    copilot_dir = tmp_path / ".github" / "copilot"
    copilot_dir.mkdir(parents=True)
    settings_file = copilot_dir / "settings.json"
    # Simulate the key already present (idempotency check at the entry level)
    settings_file.write_text(
        json.dumps(
            {
                "enabledPlugins": {_PLUGIN_KEY: True},
                "extraKnownMarketplaces": {_MARKETPLACE_NAME: {"source": _MARKETPLACE_SOURCE}},
            }
        ),
        encoding="utf-8",
    )

    assert not ensure_copilot_settings(tmp_path)


def test_replaces_non_object_values(tmp_path):
    """Legacy or invalid non-object values are replaced with the correct object form."""
    copilot_dir = tmp_path / ".github" / "copilot"
    copilot_dir.mkdir(parents=True)
    settings_file = copilot_dir / "settings.json"
    settings_file.write_text(
        json.dumps({"enabledPlugins": "invalid-string", "extraKnownMarketplaces": ["legacy-array"]}), encoding="utf-8"
    )

    assert ensure_copilot_settings(tmp_path)

    data = json.loads(settings_file.read_text(encoding="utf-8"))
    assert data["enabledPlugins"] == _EXPECTED_PLUGINS
    assert data["extraKnownMarketplaces"] == _EXPECTED_MARKETPLACES


def test_populates_empty_plugin_objects(tmp_path):
    copilot_dir = tmp_path / ".github" / "copilot"
    copilot_dir.mkdir(parents=True)
    settings_file = copilot_dir / "settings.json"
    settings_file.write_text('{"enabledPlugins": {}, "extraKnownMarketplaces": {}}', encoding="utf-8")

    assert ensure_copilot_settings(tmp_path)

    data = json.loads(settings_file.read_text(encoding="utf-8"))
    assert data["enabledPlugins"] == _EXPECTED_PLUGINS
    assert data["extraKnownMarketplaces"] == _EXPECTED_MARKETPLACES


def test_updates_stale_setup_owned_entries(tmp_path):
    copilot_dir = tmp_path / ".github" / "copilot"
    copilot_dir.mkdir(parents=True)
    settings_file = copilot_dir / "settings.json"
    settings_file.write_text(
        json.dumps(
            {
                "enabledPlugins": {
                    _PLUGIN_KEY: False,
                    "other/plugin@other-marketplace": True,
                },
                "extraKnownMarketplaces": {
                    _MARKETPLACE_NAME: {"source": {"source": "github", "repo": "old/repo"}},
                    "other-marketplace": {"source": {"source": "github", "repo": "other/example-plugin"}},
                },
            }
        ),
        encoding="utf-8",
    )

    assert ensure_copilot_settings(tmp_path)

    data = json.loads(settings_file.read_text(encoding="utf-8"))
    assert data["enabledPlugins"][_PLUGIN_KEY] is True
    assert data["enabledPlugins"]["other/plugin@other-marketplace"] is True
    assert data["extraKnownMarketplaces"][_MARKETPLACE_NAME] == {"source": _MARKETPLACE_SOURCE}
    assert data["extraKnownMarketplaces"]["other-marketplace"] == {
        "source": {"source": "github", "repo": "other/example-plugin"}
    }


def test_updates_setup_owned_entry_without_reformatting_other_nested_entries(tmp_path):
    copilot_dir = tmp_path / ".github" / "copilot"
    copilot_dir.mkdir(parents=True)
    settings_file = copilot_dir / "settings.json"
    settings_file.write_text(
        "{\n"
        '    "enabledPlugins": {\n'
        '        "other/plugin@other-marketplace" : true,\n'
        f'        "{_PLUGIN_KEY}" : false\n'
        "    },\n"
        f'    "extraKnownMarketplaces": {json.dumps(_EXPECTED_MARKETPLACES)}\n'
        "}\n",
        encoding="utf-8",
    )

    assert ensure_copilot_settings(tmp_path)

    updated = settings_file.read_text(encoding="utf-8")
    assert '"other/plugin@other-marketplace" : true' in updated
    assert f'"{_PLUGIN_KEY}" : true' in updated


def test_repairs_bool_equivalent_non_boolean_plugin_entry(tmp_path):
    copilot_dir = tmp_path / ".github" / "copilot"
    copilot_dir.mkdir(parents=True)
    settings_file = copilot_dir / "settings.json"
    settings_file.write_text(
        json.dumps(
            {
                "enabledPlugins": {_PLUGIN_KEY: 1},
                "extraKnownMarketplaces": {_MARKETPLACE_NAME: {"source": _MARKETPLACE_SOURCE}},
            }
        ),
        encoding="utf-8",
    )

    assert ensure_copilot_settings(tmp_path)

    data = json.loads(settings_file.read_text(encoding="utf-8"))
    assert data["enabledPlugins"][_PLUGIN_KEY] is True


def test_skips_non_finite_json_constants(tmp_path, capsys):
    copilot_dir = tmp_path / ".github" / "copilot"
    copilot_dir.mkdir(parents=True)
    settings_file = copilot_dir / "settings.json"
    original = '{\n    "enabledPlugins": {"other/plugin@other-marketplace": NaN}\n}\n'
    settings_file.write_text(original, encoding="utf-8")

    assert not ensure_copilot_settings(tmp_path)

    assert settings_file.read_text(encoding="utf-8") == original
    assert "non-finite JSON constant is not supported: NaN" in capsys.readouterr().err


def test_handles_parse_error_before_merge(tmp_path, capsys, monkeypatch):
    copilot_dir = tmp_path / ".github" / "copilot"
    copilot_dir.mkdir(parents=True)
    settings_file = copilot_dir / "settings.json"
    settings_file.write_text("{}", encoding="utf-8")

    def raise_value_error(*_args, **_kwargs):
        raise ValueError("boom")

    monkeypatch.setattr("agentic_devtools.cli.setup.copilot_settings._parse_top_level_members", raise_value_error)

    assert not ensure_copilot_settings(tmp_path)
    assert "Failed to parse" in capsys.readouterr().err


def test_handles_parse_error_after_merge(tmp_path, capsys, monkeypatch):
    copilot_dir = tmp_path / ".github" / "copilot"
    copilot_dir.mkdir(parents=True)
    settings_file = copilot_dir / "settings.json"
    settings_file.write_text("{}", encoding="utf-8")
    call_count = {"value": 0}
    original = _parse_top_level_members

    def parse_then_fail(content):
        call_count["value"] += 1
        if call_count["value"] == 1:
            return original(content)
        raise ValueError("boom")

    monkeypatch.setattr("agentic_devtools.cli.setup.copilot_settings._parse_top_level_members", parse_then_fail)

    assert not ensure_copilot_settings(tmp_path)
    assert "after merge" in capsys.readouterr().err


def test_preserves_crlf_line_endings(tmp_path):
    """CRLF line endings in an existing settings file are preserved byte-for-byte."""
    copilot_dir = tmp_path / ".github" / "copilot"
    copilot_dir.mkdir(parents=True)
    settings_file = copilot_dir / "settings.json"
    # Write a CRLF file with an unrelated key (so a merge is needed).
    crlf_content = '{\r\n    "unrelatedKey": "value"\r\n}\r\n'
    settings_file.write_bytes(crlf_content.encode("utf-8"))

    assert ensure_copilot_settings(tmp_path)

    raw = settings_file.read_bytes().decode("utf-8")
    assert "\r\n" in raw, "CRLF line endings must be preserved"
    data = json.loads(raw)
    assert data["unrelatedKey"] == "value"
    assert data["enabledPlugins"] == _EXPECTED_PLUGINS
