"""Mantine base class."""

from typing import Literal

from reflex.assets import asset
from reflex.vars.base import Var

from reflex_enterprise.components.component import Component, ComponentEnterprise

PACKAGE_NAME = "@mantine/core"
PACKAGE_VERSION = "8.3.9"

MantineSize = Literal["xs", "sm", "md", "lg", "xl"]

provider_path = asset(path="mantine_provider.js", shared=True)
try:
    public_provider_path = provider_path.importable_path
except AttributeError:
    # Fallback for < 0.9.0
    public_provider_path = "$/public" + provider_path


class MemoizedMantineProvider(Component):
    """Next-themes integration for radix themes components."""

    library = public_provider_path
    tag = "MemoizedMantineProvider"
    is_default = True


# Base interface for Mantine components
class MantineCoreBase(ComponentEnterprise):
    """Base class for Mantine components."""

    library = f"{PACKAGE_NAME}@{PACKAGE_VERSION}"

    def add_imports(self):
        """Add import for Mantine components."""
        return {
            "": ["@mantine/core/styles.css"],
        }

    @staticmethod
    def _get_app_wrap_components() -> dict[tuple[int, str], Component]:
        return {
            (44, "MantineProvider"): MemoizedMantineProvider.create(),
        }


class MantineLeftSection(ComponentEnterprise):
    """MantineLeftSection component for Mantine."""

    # Content section rendered on the left side of the input
    left_section: Var[Component | str]

    # Props for the left section
    left_section_props: Var[dict]

    # Width of the left section
    left_section_width: Var[float | str]

    # Controls pointer events on the left section
    left_section_pointer_events: Var[str]


class MantineRightSection(ComponentEnterprise):
    """MantineRightSection component for Mantine."""

    # Content section rendered on the right side of the input
    right_section: Var[Component | str]

    # Props for the right section
    right_section_props: Var[dict]

    # Width of the right section
    right_section_width: Var[float | str]

    # Controls pointer events on the right section
    right_section_pointer_events: Var[str]


class BaseMantineInput(MantineCoreBase, MantineLeftSection, MantineRightSection):
    """BaseInput component for Mantine."""

    # Determines whether the clear button should be displayed in the right section when the component has value, false by default
    clearable: Var[bool]

    # Placeholder text displayed when the input is empty
    placeholder: Var[str]

    # Allow multiline input
    multiline: Var[bool]

    # Set the input as read-only
    read_only: Var[bool]


class MantineDescriptionProps(MantineCoreBase):
    """BaseDescription component for Mantine."""

    # Description text displayed below the input
    description: Var[Component | str]

    # Props passed down to the description component
    description_props: Var[dict]


class MantineErrorProps(MantineCoreBase):
    """BaseError component for Mantine."""

    # Error message displayed below the input
    error: Var[Component | str | bool]

    # Props passed down to the error component
    error_props: Var[dict]


class MantineLabelProps(MantineCoreBase):
    """BaseLabel component for Mantine."""

    # Label text displayed above the input
    label: Var[Component | str]

    # Props passed down to the label component
    label_props: Var[dict]
