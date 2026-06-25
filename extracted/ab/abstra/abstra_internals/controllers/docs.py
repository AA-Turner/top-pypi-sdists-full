from __future__ import annotations

from pathlib import Path
from typing import Literal

import requests

from abstra_internals.environment import DOCS_URL
from abstra_internals.repositories.factory import Repositories
from abstra_internals.utils.sdk import SDKContractParser

_AI_GUIDES_DIR = Path(__file__).parent.parent / "ai_guides"

_GUIDE_SOURCES = {
    ("page", "guide"): ("docs", "/docs/md/workflow/pages/pages.md"),
    ("page", "examples"): ("ai_guides", "pages_examples.md"),
    ("form", "guide"): ("docs", "/docs/md/workflow/forms/step-types.md"),
    ("form", "examples"): ("ai_guides", "forms_examples.md"),
    ("agent", "guide"): ("ai_guides", "agents_guide.md"),
    ("agent", "examples"): ("ai_guides", "agents_examples.md"),
}


def _available_names(module_data: dict, object_type: str) -> list:
    """Names in a module of the given object_type ('class'/'function'), falling
    back to all names when none are tagged."""
    return [
        name
        for name, info in module_data.items()
        if isinstance(info, dict) and info.get("object_type") == object_type
    ] or list(module_data)


class DocsController:
    repos: Repositories
    sdk: dict

    def __init__(self, repos: Repositories):
        self.repos = repos
        self.sdk = SDKContractParser("abstra", silent=True).run()

    def read_abstra_docs(self, path: str = "/llms.txt"):
        """
        Fetches the documentation menu from the abstra documentation URL.

        It should always be the first step before generating any code.

        This should be used to understand how Abstra works and what functionalities are available.

        Args:
            path (str): The path to the documentation file. Defaults to "/llms.txt" which is the main menu. Example: "/docs/md/workflow/forms/examples/external-data.md
        Copywritings:
            Read the abstra documentation
            Reading the abstra documentation...

        """

        if not path:
            path = "/llms.txt"
        if not path.startswith("/"):
            path = "/" + path
        if path.startswith("/docs/"):
            path = path.replace("/docs/", "/")

        url = DOCS_URL + (path or "/llms.txt")
        menu_content = requests.get(url).text
        return menu_content

    def list_all_modules_in_abstra_lib(self):
        """
        Reads the documentation of the abstra package.

        It should be followed by listing objects in a specific module.

        Copywritings:
            List all modules in the abstra package
            Listing all modules in the abstra package...
        """
        return list(self.sdk.keys())

    def list_objects_in_abstra_module(self, module_name: str):
        """
        Get the documentation for a specific module.

        It helps to understand what functions, classes, and variables are available in the module.

        Args:
            module_name (str): The name of the module.

        Copywritings:
            List all objects in a specific module
            Listing all objects in a specific module...
        """

        return [
            {
                "type": value["object_type"],
                "name": key,
                "description": value.get("description", ""),
            }
            for key, value in self.sdk[module_name].items()
        ]

    def get_stage_guide(
        self,
        topic: Literal["page", "form", "agent"],
        kind: Literal["guide", "examples"] = "guide",
    ) -> str:
        """
        Get the guide or examples for writing good Abstra code for Pages,
        Forms, or Agents. Always call this before writing any code for the respective topic.

        Args:
            topic: Which topic to get docs for. One of 'page', 'form', or 'agent'.
            kind: Either 'guide' (best-practices guide) or 'examples' (annotated
                real-world code examples). Defaults to 'guide'.

        Copywritings:
            Get the stage guide
            Reading stage guide...
        """
        source = _GUIDE_SOURCES.get((topic, kind))
        if source is None:
            raise ValueError(f"Unknown topic/kind combination: {topic!r}/{kind!r}")

        source_kind, location = source
        if source_kind == "docs":
            return self.read_abstra_docs(location)

        path = _AI_GUIDES_DIR / location
        if not path.exists():
            return "No examples available yet."
        return path.read_text()

    def describe_class(
        self,
        module_name: str,
        class_name: str,
        include: (
            list[Literal["params", "properties", "parents", "examples"]] | None
        ) = None,
    ) -> dict:
        """
        Describe a class from the abstra SDK.

        Returns the requested projections of the class, or all of them if
        `include` is omitted.

        Args:
            module_name: Name of the SDK module containing the class.
            class_name: Name of the class to describe.
            include: Which projections to return. Any subset of
                'params', 'properties', 'parents', 'examples'. Defaults to all.

        Copywritings:
            Describe a class from the abstra SDK
            Describing a class from the abstra SDK...
        """
        if module_name not in self.sdk:
            raise ValueError(
                f"Unknown module {module_name!r}. Valid modules: {list(self.sdk)}"
            )
        module_data = self.sdk[module_name]
        if class_name not in module_data:
            available = _available_names(module_data, "class")
            raise ValueError(
                f"Unknown class {class_name!r} in module {module_name!r}. "
                f"Available classes: {available}"
            )
        class_data = module_data[class_name]
        projections = {
            "params": (class_data.get("init") or {}).get("params"),
            "properties": class_data.get("properties"),
            "parents": class_data.get("parent_classes"),
            "examples": class_data.get("examples"),
        }
        selections = include if include is not None else list(projections)
        return {key: projections[key] for key in selections if key in projections}

    def describe_function(
        self,
        module_name: str,
        function_name: str,
        include: (list[Literal["params", "examples", "return_type"]] | None) = None,
    ) -> dict:
        """
        Describe a function from the abstra SDK.

        Returns the requested projections of the function, or all of them if
        `include` is omitted.

        Args:
            module_name: Name of the SDK module containing the function.
            function_name: Name of the function to describe.
            include: Which projections to return. Any subset of
                'params', 'examples', 'return_type'. Defaults to all.

        Copywritings:
            Describe a function from the abstra SDK
            Describing a function from the abstra SDK...
        """
        if module_name not in self.sdk:
            raise ValueError(
                f"Unknown module {module_name!r}. Valid modules: {list(self.sdk)}"
            )
        module_data = self.sdk[module_name]
        if function_name not in module_data:
            available = _available_names(module_data, "function")
            raise ValueError(
                f"Unknown function {function_name!r} in module {module_name!r}. "
                f"Available functions: {available}"
            )
        function_data = module_data[function_name]
        projections = {
            "params": function_data.get("params"),
            "examples": function_data.get("examples"),
            "return_type": function_data.get("return_type"),
        }
        selections = include if include is not None else list(projections)
        return {key: projections[key] for key in selections if key in projections}
