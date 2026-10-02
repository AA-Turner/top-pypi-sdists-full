# Copyright 2024 Agnostiq Inc.

from enum import Enum
from typing import Any, Dict, List, Optional, Union

import requests
from pydantic import BaseModel, ConfigDict


class BaseImageConfig(BaseModel):
    """
    Represents the base Docker image configuration for an environment.

    Attributes:
        base_image: The base Docker image for the environment, formatted as `<registry>/<image>:<tag>`,
                    where `:tag` is optional. This should point to a publicly accessible or private image.

        username_credentials_reference_id: Optional(str); The ID of the username secret uploaded to the Covalent Cloud via
                                            the `store_secret` function, if the Docker image is stored in a private.

        password_credentials_reference_id: Optional(str); The ID of the password uploaded to the Covalent Cloud via the
                                        `store_secret` function, if the Docker image is stored in a private registry.
    """

    base_image: str
    # Temporary: handle Nvidia images as a special case until we
    # refactor the general base_image pipeline
    nvidia: bool = False
    username_credentials_reference_id: Optional[str] = None
    password_credentials_reference_id: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class PackageProvider(Enum):
    """
    Enum representing the package provider for runtime packages to be installed in the environment.

    Values:
        SYSTEM: the OS default package manager (e.g., APT for Ubuntu, yum for CentOS, etc.).
        WGET: wget to download packages from a given URL.
        GIT: git to clone repositories as packages.
    """

    SYSTEM = "SYSTEM"
    WGET = "WGET"
    GIT = "GIT"


class RuntimePackage(BaseModel):
    """
    Defines a runtime package to be installed in the environment.

    Attributes:
        name: The name of the package. For SYSTEM providers, this is the package name. For WGET and GIT,
              this should be the URL of the artifact or repository to fetch.
        provider Optional(PackageProvider): The provider for this package. Defaults to SYSTEM if not specified.
    """

    name: str
    provider: Optional[PackageProvider] = PackageProvider.SYSTEM
    model_config = ConfigDict(from_attributes=True)


class EnvironmentRuntimeConfig(BaseModel):
    """
    Configuration for the runtime environment, including the base image and any additional packages.

    Attributes:
        image: Optional(BaseImageConfig); Configuration for the base Docker image of the environment.
    """

    image: Optional[BaseImageConfig] = None
    model_config = ConfigDict(from_attributes=True)


class Environment(BaseModel):
    """
    Basic representation of a user created environment in Covalent Cloud.

    Attributes:
        id: The unique identifier of the environment.
        name: The name of the environment.
        created_at: The timestamp when the environment was created.
        status: The current status of the environment.
        definition: A dictionary containing the environment definition.
    """

    id: str
    name: str
    created_at: str
    status: str
    definition_url: str

    # Will be populated when the environment definition is loaded
    conda: Optional[List[str]] = None  # List of conda packages
    pip: Optional[List[str]] = None  # List of pip packages

    def __str__(self) -> str:
        return f"Environment({self.name})"

    def __repr__(self) -> str:
        return f"Environment({self.name})"

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

    def _parse_definition(self, text: str) -> Dict[str, Union[str, List[str]]]:
        """
        Parse the environment definition from the raw string to a dictionary.
        """

        conda = []
        pip = []

        lines = text.split("\n")
        # Only get the lines that start with "-" or "  -" i.e. the dependencies
        lines = [line for line in lines if line.startswith("-") or line.startswith("  -")]
        i = 0

        # Parse up to the first "pip:" line to get all the conda packages
        while not lines[i].endswith("pip:"):
            if lines[i].startswith("-"):
                package = lines[i].strip("-").strip()
                conda.append(package)
            i += 1

        # Parse the pip packages after the "pip:" line
        i += 1
        while i < len(lines) and not lines[i].startswith("-"):
            if lines[i].startswith("  -"):
                package = lines[i].strip("  -").strip()
                pip.append(package)
            i += 1

        return conda, pip

    def load_definition(self) -> None:
        """
        Load the environment definition from presigned S3 URL.
        """

        # In case the definition is already loaded in any of the attributes
        if self.conda is not None or self.pip is not None:
            return

        response = requests.get(self.definition_url)
        response.raise_for_status()
        self.conda, self.pip = self._parse_definition(response.text)
