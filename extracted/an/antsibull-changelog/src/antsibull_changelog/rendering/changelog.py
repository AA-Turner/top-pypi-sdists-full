# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2024, Ansible Project

"""
Rendering a changelog.
"""

from __future__ import annotations

import collections
import os
from collections.abc import Mapping
from typing import Any

from ..changelog_generator import (
    ChangelogEntry,
    ChangelogGeneratorBase,
    get_plugin_name,
)
from ..changes import ChangesData
from ..config import (
    ChangelogConfig,
    ChangelogOutput,
    ChangelogRenderConfig,
    PathsConfig,
    TextFormat,
)
from ..logger import LOGGER
from .document import AbstractRenderer, DocumentRenderer, SectionRenderer
from .md_document import MDDocumentRenderer
from .rst_document import RSTDocumentRenderer


def add_section_content(
    entry: ChangelogEntry, renderer: AbstractRenderer, section_name: str
) -> None:
    """
    Add a section's content of fragments to the changelog.
    """
    if section_name not in entry.changes:
        return

    content = entry.changes[section_name]

    if isinstance(content, list):
        for text in sorted(content):
            renderer.add_fragment(text, text_format=entry.text_format)
    else:
        renderer.add_text(content, text_format=entry.text_format)


class ChangelogGenerator(ChangelogGeneratorBase):
    """
    Render changelog.

    This class can be both used to create a full changelog, or to append a
    changelog to an existing renderer. This is for example useful to create
    a combined ACD changelog.
    """

    def __init__(  # pylint: disable=useless-parent-delegation
        self,
        config: ChangelogConfig,
        changes: ChangesData,
        *,
        flatmap: bool = True,
        render_config: ChangelogRenderConfig | None = None,
    ):
        """
        Create a changelog generator.
        """
        super().__init__(
            config,
            changes,
            flatmap=flatmap,
            render_config=render_config,
        )

    def append_changelog_entry(
        self,
        renderer: AbstractRenderer,
        changelog_entry: ChangelogEntry,
        add_version: bool = False,
    ) -> None:
        """
        Append changelog entry to a renderer.
        """
        section_renderer: SectionRenderer | None = None
        if add_version:
            section_renderer = renderer.add_section("v%s" % changelog_entry.version)
            renderer = section_renderer

        if self.render_config.per_release_toc:
            renderer.add_toc(max_depth=self.render_config.per_release_toc_depth)

        for section_name in self.config.sections:
            self._add_section(
                renderer,
                changelog_entry,
                section_name,
            )

        fqcn_prefix = self.get_fqcn_prefix()
        self._add_plugins(
            renderer,
            changelog_entry.plugins,
            fqcn_prefix=fqcn_prefix,
        )
        self._add_modules(
            renderer,
            changelog_entry.modules,
            flatmap=self.flatmap,
            fqcn_prefix=fqcn_prefix,
        )
        self._add_objects(
            renderer,
            changelog_entry.objects,
            fqcn_prefix=fqcn_prefix,
        )

        if section_renderer:
            section_renderer.close()

    def generate_to(  # pylint: disable=too-many-arguments
        self,
        renderer: AbstractRenderer,
        squash: bool = False,
        after_version: str | None = None,
        until_version: str | None = None,
        only_latest: bool = False,
    ) -> None:
        """
        Append changelog to a renderer.

        :arg squash: Squash all releases into one entry
        :arg after_version: If given, only consider versions after this one
        :arg until_version: If given, do not consider versions following this one
        :arg only_latest: If set to ``True``, only generate the latest entry
        """
        release_entries = self.collect(
            squash=squash, after_version=after_version, until_version=until_version
        )

        for release in release_entries:
            self.append_changelog_entry(
                renderer,
                release,
                add_version=not squash and not only_latest,
            )
            if only_latest:
                break

    def generate(self, renderer: DocumentRenderer, only_latest: bool = False) -> None:
        """
        Generate the changelog.
        """
        if not only_latest:
            renderer.set_title(self.get_title())
            if self.render_config.global_toc:
                renderer.add_toc(
                    "Topics", max_depth=self.render_config.global_toc_depth
                )

            if self.changes.ancestor and self.config.mention_ancestor:
                renderer.add_text(
                    "This changelog describes changes after version {0}.".format(
                        self.changes.ancestor
                    ),
                    text_format=TextFormat.RESTRUCTURED_TEXT,
                )

        self.generate_to(renderer, only_latest=only_latest)

    def _add_section(
        self,
        renderer: AbstractRenderer,
        changelog_entry: ChangelogEntry,
        section_name: str,
    ) -> None:
        """
        Add a section of fragments to the changelog.
        """
        if section_name not in changelog_entry.changes:
            return

        section_title = self.config.sections[section_name]
        section = renderer.add_section(section_title)

        add_section_content(changelog_entry, renderer, section_name)

        section.close()

    @staticmethod
    def _add_plugins(
        renderer: AbstractRenderer,
        plugins_database: dict[str, list[dict[str, Any]]],
        fqcn_prefix: str | None,
    ) -> None:
        """
        Add new plugins to the changelog.
        """
        if not plugins_database:
            return

        plugins_section: SectionRenderer | None = None

        for plugin_type in sorted(plugins_database):
            plugins = plugins_database.get(plugin_type)
            if not plugins:
                continue

            if not plugins_section:
                plugins_section = renderer.add_section("New Plugins")

            plugin_section = plugins_section.add_section(plugin_type.title())

            ChangelogGenerator.add_plugins(plugin_section, plugins, fqcn_prefix)

            plugin_section.close()

        if plugins_section:
            plugins_section.close()

    @staticmethod
    def add_plugins(
        renderer: AbstractRenderer,
        plugins: list[dict[str, Any]],
        fqcn_prefix: str | None,
    ) -> None:
        """
        Add new plugins of one type to the changelog.
        """
        for plugin in sorted(plugins, key=lambda plugin: plugin["name"]):
            plugin_name = get_plugin_name(plugin["name"], fqcn_prefix=fqcn_prefix)
            renderer.add_fragment(
                "%s - %s" % (plugin_name, plugin["description"]),
                text_format=TextFormat.RESTRUCTURED_TEXT,
            )

    @staticmethod
    def _add_modules(
        renderer: AbstractRenderer,
        modules: list[dict[str, Any]],
        flatmap: bool,
        fqcn_prefix: str | None,
    ) -> None:
        """
        Add new modules to the changelog.
        """
        if not modules:
            return

        section = renderer.add_section("New Modules")
        ChangelogGenerator.add_modules(section, modules, flatmap, fqcn_prefix)
        section.close()

    @staticmethod
    def add_modules(
        renderer: AbstractRenderer,
        modules: list[dict[str, Any]],
        flatmap: bool,
        fqcn_prefix: str | None,
    ) -> None:
        """
        Add new modules to the changelog.
        """
        modules_by_namespace = collections.defaultdict(list)
        for module in sorted(modules, key=lambda module: module["name"]):
            modules_by_namespace[module["namespace"]].append(module)

        previous_section = None
        section_renderer: SectionRenderer | None = None
        for namespace in sorted(modules_by_namespace):
            parts = namespace.split(".")

            section = parts.pop(0).replace("_", " ").title()

            if section != previous_section and section_renderer:
                section_renderer.close()
                section_renderer = None

            if section and section_renderer is None:
                section_renderer = renderer.add_section(section)

            previous_section = section

            subsection = ".".join(parts)

            subsection_renderer: SectionRenderer | None = None
            if subsection:
                subsection_renderer = (section_renderer or renderer).add_section(
                    subsection
                )

            entry_renderer = subsection_renderer or section_renderer or renderer
            ChangelogGenerator._add_namespaced_modules(
                entry_renderer, modules_by_namespace, namespace, flatmap, fqcn_prefix
            )

            if subsection_renderer:
                subsection_renderer.close()

        if section_renderer:
            section_renderer.close()

    @staticmethod
    def _add_namespaced_modules(
        renderer: AbstractRenderer,
        modules_by_namespace: Mapping[str, list[dict[str, Any]]],
        namespace: str,
        flatmap: bool,
        fqcn_prefix: str | None,
    ) -> None:
        for module in modules_by_namespace[namespace]:
            module_name = get_plugin_name(
                module["name"],
                fqcn_prefix=fqcn_prefix,
                namespace=namespace,
                flatmap=flatmap,
            )
            renderer.add_fragment(
                "%s - %s" % (module_name, module["description"]),
                text_format=TextFormat.RESTRUCTURED_TEXT,
            )

    @staticmethod
    def _add_objects(
        renderer: AbstractRenderer,
        objects_database: dict[str, list[dict[str, Any]]],
        fqcn_prefix: str | None,
    ) -> None:
        """
        Add new objects to the changelog.
        """
        if not objects_database:
            return

        for object_type in sorted(objects_database):
            objects = objects_database.get(object_type)
            if not objects:
                continue

            section_renderer = renderer.add_section("New " + object_type.title() + "s")

            ChangelogGenerator.add_objects(section_renderer, objects, fqcn_prefix)

            section_renderer.close()

    @staticmethod
    def add_objects(
        renderer: AbstractRenderer,
        objects: list[dict[str, Any]],
        fqcn_prefix: str | None,
    ) -> None:
        """
        Add new objects of one type to the changelog.
        """
        for ansible_object in sorted(
            objects, key=lambda ansible_object: ansible_object["name"]
        ):
            object_name = get_plugin_name(
                ansible_object["name"], fqcn_prefix=fqcn_prefix
            )
            renderer.add_fragment(
                "%s - %s" % (object_name, ansible_object["description"]),
                text_format=TextFormat.RESTRUCTURED_TEXT,
            )


def create_document_renderer(
    document_format: TextFormat, start_level: int = 0
) -> DocumentRenderer:
    """
    Create a document renderer for a given format.
    """
    if document_format == TextFormat.RESTRUCTURED_TEXT:
        return RSTDocumentRenderer(start_level=start_level)
    if document_format == TextFormat.MARKDOWN:
        return MDDocumentRenderer(start_level=start_level)
    raise ValueError(f"Unsupported format {document_format}")


def _create_changelog_path(
    paths: PathsConfig,
    changes: ChangesData,
    output: ChangelogOutput,
) -> str:
    major_minor_version = ".".join(
        changes.latest_version.split(".")[: output.filename_version_depth]
    )
    changelog_filename = output.file
    if "%s" in changelog_filename:
        changelog_filename = changelog_filename % (major_minor_version,)
    return os.path.join(paths.base_dir, changelog_filename)


def generate_changelog(  # pylint: disable=too-many-arguments
    paths: PathsConfig,
    config: ChangelogConfig,
    changes: ChangesData,
    output: ChangelogOutput,
    *,
    flatmap: bool = True,
    only_latest: bool = False,
):
    """
    Generate the changelog as reStructuredText.

    :kwarg flatmap: Whether the collection uses flatmapping or not
    :kwarg only_latest: Only write the last changelog entry without any preamble
    """
    changelog_path = _create_changelog_path(paths, changes, output)

    generator = ChangelogGenerator(
        config,
        changes,
        flatmap=flatmap,
        render_config=output,
    )
    renderer = create_document_renderer(
        output.format, start_level=1 if only_latest else 0
    )
    generator.generate(renderer, only_latest=only_latest)

    text = renderer.render()
    for warning in renderer.get_warnings():
        LOGGER.warning(warning)

    with open(changelog_path, "w", encoding="utf-8") as changelog_fd:
        changelog_fd.write(text)


__all__ = (
    "add_section_content",
    "ChangelogGenerator",
    "create_document_renderer",
    "generate_changelog",
)
