"""Tests for G13 profile manager."""

import tempfile
from pathlib import Path

import pytest

from g13_linux.gui.models.profile_manager import ProfileData, ProfileManager


class TestProfileData:
    """Test ProfileData dataclass."""

    def test_create_minimal_profile(self):
        """Create profile with just a name."""
        profile = ProfileData(name="Test")

        assert profile.name == "Test"
        assert profile.description == ""
        assert profile.version == "0.1.0"
        assert profile.mappings == {}

    def test_create_full_profile(self):
        """Create profile with all fields."""
        profile = ProfileData(
            name="Full Test",
            description="A test profile",
            version="1.0.0",
            mappings={"G1": "KEY_A"},
            lcd={"enabled": True, "default_text": "Hello"},
            backlight={"color": "#FF0000", "brightness": 50},
            joystick={"mode": "mouse"},
        )

        assert profile.name == "Full Test"
        assert profile.mappings == {"G1": "KEY_A"}
        assert profile.joystick == {"mode": "mouse"}


class TestProfileManager:
    """Test ProfileManager CRUD operations."""

    @pytest.fixture
    def temp_profiles_dir(self):
        """Create temporary profiles directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def manager(self, temp_profiles_dir):
        """Create ProfileManager with temp directory."""
        return ProfileManager(temp_profiles_dir)

    def test_list_empty_profiles(self, manager):
        """List profiles when none exist."""
        profiles = manager.list_profiles()
        assert profiles == []

    def test_create_profile(self, manager):
        """Create new profile with defaults."""
        profile = manager.create_profile("New Profile")

        assert profile.name == "New Profile"
        assert "G1" in profile.mappings
        assert "G22" in profile.mappings
        assert "M1" in profile.mappings

    def test_save_and_load_profile(self, manager):
        """Save profile and load it back."""
        profile = ProfileData(
            name="Test Save",
            description="Testing save/load",
            mappings={"G1": "KEY_F1", "G2": {"keys": ["KEY_LEFTCTRL", "KEY_C"]}},
        )

        manager.save_profile(profile, "test_save")
        loaded = manager.load_profile("test_save")

        assert loaded.name == "Test Save"
        assert loaded.mappings["G1"] == "KEY_F1"
        assert loaded.mappings["G2"] == {"keys": ["KEY_LEFTCTRL", "KEY_C"]}

    def test_list_profiles_after_save(self, manager):
        """List includes saved profiles."""
        profile = ProfileData(name="Listed")
        manager.save_profile(profile, "listed_profile")

        profiles = manager.list_profiles()

        assert "listed_profile" in profiles

    def test_load_nonexistent_raises(self, manager):
        """Loading nonexistent profile raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            manager.load_profile("does_not_exist")

    def test_delete_profile(self, manager):
        """Delete removes profile file."""
        profile = ProfileData(name="To Delete")
        manager.save_profile(profile, "to_delete")

        assert "to_delete" in manager.list_profiles()

        manager.delete_profile("to_delete")

        assert "to_delete" not in manager.list_profiles()

    def test_delete_nonexistent_raises(self, manager):
        """Deleting nonexistent profile raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            manager.delete_profile("ghost")

    def test_profile_exists(self, manager):
        """Check profile existence."""
        assert not manager.profile_exists("nope")

        profile = ProfileData(name="Exists")
        manager.save_profile(profile, "exists_test")

        assert manager.profile_exists("exists_test")

    def test_current_profile_tracking(self, manager):
        """Current profile is tracked after load."""
        profile = ProfileData(name="Current")
        manager.save_profile(profile, "current")

        assert manager.current_profile is None or manager.current_profile.name == "Current"

        manager.load_profile("current")
        assert manager.current_profile.name == "Current"

    def test_delete_clears_current_if_same(self, manager):
        """Deleting current profile clears it."""
        profile = ProfileData(name="deletable")  # Name matches file name
        manager.save_profile(profile, "deletable")
        manager.load_profile("deletable")

        manager.delete_profile("deletable")

        assert manager.current_profile is None


class TestProfileValidation:
    """Test profile JSON validation."""

    @pytest.fixture
    def temp_profiles_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_load_invalid_json_raises(self, temp_profiles_dir):
        """Invalid JSON raises ValueError."""
        manager = ProfileManager(temp_profiles_dir)
        path = Path(temp_profiles_dir) / "bad.json"
        path.write_text("{ not valid json")

        with pytest.raises(ValueError):
            manager.load_profile("bad")

    def test_load_missing_fields_uses_defaults(self, temp_profiles_dir):
        """Profile with missing fields uses defaults."""
        manager = ProfileManager(temp_profiles_dir)
        path = Path(temp_profiles_dir) / "minimal.json"
        path.write_text('{"name": "Minimal"}')

        profile = manager.load_profile("minimal")

        assert profile.name == "Minimal"
        assert profile.description == ""
        assert profile.mappings == {}


class TestProfileManagerMissingCoverage:
    """Tests for edge cases to achieve 100% coverage."""

    def test_default_profiles_dir(self):
        """Test ProfileManager uses default directory when None passed (lines 40-41)."""
        # Create manager without specifying profiles_dir
        manager = ProfileManager(profiles_dir=None)

        # Should have set profiles_dir to project_root/configs/profiles
        assert manager.profiles_dir is not None
        assert manager.profiles_dir.name == "profiles"
        assert manager.profiles_dir.parent.name == "configs"
        # Directory should be created
        assert manager.profiles_dir.exists()


class TestProfileImportExport:
    """Test profile import/export functionality."""

    @pytest.fixture
    def temp_profiles_dir(self):
        """Create temporary profiles directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def manager(self, temp_profiles_dir):
        """Create ProfileManager with temp directory."""
        return ProfileManager(temp_profiles_dir)

    @pytest.fixture
    def export_dir(self):
        """Create temporary export directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_export_profile(self, manager, export_dir):
        """Export a profile to external location."""
        profile = ProfileData(
            name="Export Test",
            mappings={"G1": "KEY_A"},
        )
        manager.save_profile(profile, "export_test")

        export_path = Path(export_dir) / "exported.json"
        manager.export_profile("export_test", str(export_path))

        assert export_path.exists()
        # Verify content
        import json

        with open(export_path) as f:
            data = json.load(f)
        assert data["name"] == "Export Test"
        assert data["mappings"]["G1"] == "KEY_A"

    def test_export_adds_json_extension(self, manager, export_dir):
        """Export automatically adds .json extension."""
        profile = ProfileData(name="No Extension")
        manager.save_profile(profile, "no_ext")

        export_path = Path(export_dir) / "exported"  # No extension
        manager.export_profile("no_ext", str(export_path))

        # Should have added .json
        assert (Path(export_dir) / "exported.json").exists()

    def test_export_nonexistent_raises(self, manager, export_dir):
        """Exporting nonexistent profile raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            manager.export_profile("ghost", str(Path(export_dir) / "ghost.json"))

    def test_import_profile(self, manager, export_dir):
        """Import a profile from external location."""
        # Create a profile file to import
        import json

        import_path = Path(export_dir) / "to_import.json"
        profile_data = {
            "name": "Imported Profile",
            "description": "From external",
            "version": "1.0.0",
            "mappings": {"G1": "KEY_B"},
            "lcd": {"enabled": True, "default_text": ""},
            "backlight": {"color": "#00FF00", "brightness": 80},
        }
        with open(import_path, "w") as f:
            json.dump(profile_data, f)

        imported_name = manager.import_profile(str(import_path))

        assert imported_name == "Imported Profile"
        assert manager.profile_exists("Imported Profile")

        # Load and verify
        loaded = manager.load_profile("Imported Profile")
        assert loaded.mappings["G1"] == "KEY_B"
        assert loaded.backlight["color"] == "#00FF00"

    def test_import_with_new_name(self, manager, export_dir):
        """Import with custom name."""
        import json

        import_path = Path(export_dir) / "original.json"
        with open(import_path, "w") as f:
            json.dump({"name": "Original Name", "mappings": {}}, f)

        imported_name = manager.import_profile(str(import_path), new_name="Custom Name")

        assert imported_name == "Custom Name"
        assert manager.profile_exists("Custom Name")
        assert not manager.profile_exists("Original Name")

    def test_import_handles_name_conflict(self, manager, export_dir):
        """Import generates unique name on conflict."""
        # Create existing profile
        profile = ProfileData(name="Conflict")
        manager.save_profile(profile, "Conflict")

        # Create import file with same name
        import json

        import_path = Path(export_dir) / "conflict.json"
        with open(import_path, "w") as f:
            json.dump({"name": "Conflict", "mappings": {"G1": "KEY_NEW"}}, f)

        imported_name = manager.import_profile(str(import_path))

        # Should have generated unique name
        assert imported_name == "Conflict_1"
        assert manager.profile_exists("Conflict")
        assert manager.profile_exists("Conflict_1")

    def test_import_nonexistent_raises(self, manager):
        """Importing nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            manager.import_profile("/path/to/nonexistent.json")

    def test_import_invalid_json_raises(self, manager, export_dir):
        """Importing invalid JSON raises ValueError."""
        import_path = Path(export_dir) / "invalid.json"
        import_path.write_text("{ not valid json")

        with pytest.raises(ValueError):
            manager.import_profile(str(import_path))

    def test_import_missing_name_uses_filename(self, manager, export_dir):
        """Import uses filename if profile has no name."""
        import json

        import_path = Path(export_dir) / "nameless_profile.json"
        # Profile with empty name
        with open(import_path, "w") as f:
            json.dump({"name": "", "mappings": {}}, f)

        imported_name = manager.import_profile(str(import_path))

        # Should use filename stem since name is empty
        assert imported_name == "nameless_profile"
