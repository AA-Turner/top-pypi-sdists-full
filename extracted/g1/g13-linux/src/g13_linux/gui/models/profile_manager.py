"""
Profile Manager

Manages CRUD operations for G13 button mapping profiles.
"""

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from g13_linux._paths import get_profiles_dir


@dataclass
class ProfileData:
    """
    Profile data structure matching JSON format.

    Supports two mapping formats:
    - Simple: {'G1': 'KEY_1', ...}
    - Combo:  {'G1': {'keys': ['KEY_LEFTCTRL', 'KEY_B'], 'label': '...'}, ...}

    Button IDs:
    - G1-G22: Main G-keys
    - M1-M3: Mode buttons
    - MR: Macro record button
    - LEFT, DOWN: Thumb buttons adjacent to joystick
    - STICK: Joystick click (press down on stick)
    """

    name: str
    description: str = ""
    version: str = "0.1.0"
    mappings: dict = field(default_factory=dict)  # str | dict values
    lcd: dict = field(default_factory=lambda: {"enabled": True, "default_text": ""})
    backlight: dict = field(default_factory=lambda: {"color": "#FFFFFF", "brightness": 100})
    joystick: dict = field(
        default_factory=lambda: {
            "mode": "analog",  # "analog", "digital", or "disabled"
            "deadzone": 20,
            "sensitivity": 1.0,
            "key_up": "KEY_UP",
            "key_down": "KEY_DOWN",
            "key_left": "KEY_LEFT",
            "key_right": "KEY_RIGHT",
            "allow_diagonals": True,
        }
    )


class ProfileManager:
    """Manages profile CRUD operations"""

    def __init__(self, profiles_dir: str | None = None):
        if profiles_dir is None:
            profiles_dir = get_profiles_dir()

        self.profiles_dir = Path(profiles_dir)
        self.current_profile: ProfileData | None = None
        self.current_name: str | None = None  # Filename (without .json)

        # Ensure profiles directory exists
        self.profiles_dir.mkdir(parents=True, exist_ok=True)

    def list_profiles(self) -> list[str]:
        """Return list of available profile names"""
        return [p.stem for p in self.profiles_dir.glob("*.json")]

    def load_profile(self, name: str) -> ProfileData:
        """
        Load profile from JSON file

        Args:
            name: Profile name (without .json extension)

        Returns:
            Loaded ProfileData

        Raises:
            FileNotFoundError: If profile doesn't exist
            ValueError: If profile JSON is invalid
        """
        path = self.profiles_dir / f"{name}.json"

        if not path.exists():
            raise FileNotFoundError(f"Profile '{name}' not found at {path}")

        try:
            with open(path) as f:
                data = json.load(f)
            profile = ProfileData(**data)
            self.current_profile = profile
            self.current_name = name  # Track the filename
            return profile
        except (json.JSONDecodeError, TypeError) as e:
            raise ValueError(f"Invalid profile JSON in '{name}': {e}")

    def save_profile(self, profile: ProfileData, name: str | None = None):
        """
        Save profile to JSON file

        Args:
            profile: ProfileData to save
            name: Optional profile name (uses profile.name if not provided)
        """
        save_name = name or profile.name
        path = self.profiles_dir / f"{save_name}.json"

        with open(path, "w") as f:
            json.dump(asdict(profile), f, indent=2)

        self.current_profile = profile

    def create_profile(self, name: str) -> ProfileData:
        """
        Create new empty profile with default mappings

        Args:
            name: Profile name

        Returns:
            New ProfileData with default mappings
        """
        # Create default mappings for all buttons
        default_mappings = {}

        # G keys (G1-G22)
        for i in range(1, 23):
            default_mappings[f"G{i}"] = "KEY_RESERVED"

        # M keys (M1-M3)
        for i in range(1, 4):
            default_mappings[f"M{i}"] = "KEY_RESERVED"

        # Thumb buttons (adjacent to joystick)
        default_mappings["LEFT"] = "KEY_RESERVED"
        default_mappings["DOWN"] = "KEY_RESERVED"

        # Joystick click (press down on stick)
        default_mappings["STICK"] = "KEY_RESERVED"

        profile = ProfileData(
            name=name,
            description="",
            version="0.1.0",
            mappings=default_mappings,
            lcd={"enabled": True, "default_text": ""},
            backlight={"color": "#FFFFFF", "brightness": 100},
        )

        return profile

    def delete_profile(self, name: str):
        """
        Delete profile file

        Args:
            name: Profile name to delete

        Raises:
            FileNotFoundError: If profile doesn't exist
        """
        path = self.profiles_dir / f"{name}.json"

        if not path.exists():
            raise FileNotFoundError(f"Profile '{name}' not found")

        path.unlink()

        # Clear current profile if it was the deleted one
        if self.current_profile and self.current_profile.name == name:
            self.current_profile = None

    def profile_exists(self, name: str) -> bool:
        """Check if a profile exists"""
        path = self.profiles_dir / f"{name}.json"
        return path.exists()

    def export_profile(self, name: str, export_path: str) -> None:
        """
        Export a profile to an external location.

        Args:
            name: Profile name to export (without .json extension)
            export_path: Full path where to save the exported profile

        Raises:
            FileNotFoundError: If profile doesn't exist
        """
        source_path = self.profiles_dir / f"{name}.json"

        if not source_path.exists():
            raise FileNotFoundError(f"Profile '{name}' not found")

        # Ensure export path has .json extension
        export_path = Path(export_path)
        if export_path.suffix.lower() != ".json":
            export_path = export_path.with_suffix(".json")

        # Copy the profile file
        import shutil

        shutil.copy2(source_path, export_path)

    def import_profile(self, import_path: str, new_name: str | None = None) -> str:
        """
        Import a profile from an external location.

        Args:
            import_path: Path to the profile JSON file to import
            new_name: Optional new name for the profile (uses original name if None)

        Returns:
            The name of the imported profile

        Raises:
            FileNotFoundError: If import file doesn't exist
            ValueError: If the file is not a valid profile JSON
        """
        import_path = Path(import_path)

        if not import_path.exists():
            raise FileNotFoundError(f"Import file not found: {import_path}")

        # Load and validate the profile
        try:
            with open(import_path) as f:
                data = json.load(f)

            # Validate it can be parsed as ProfileData
            profile = ProfileData(**data)
        except (json.JSONDecodeError, TypeError) as e:
            raise ValueError(f"Invalid profile JSON: {e}")

        # Determine the profile name
        if new_name:
            profile_name = new_name
            profile.name = new_name
        else:
            # Use the profile's internal name or filename
            profile_name = profile.name or import_path.stem

        # Check for conflicts and generate unique name if needed
        original_name = profile_name
        counter = 1
        while self.profile_exists(profile_name):
            profile_name = f"{original_name}_{counter}"
            counter += 1

        # Save the profile
        self.save_profile(profile, profile_name)

        return profile_name
