"""
Build an OCDS profile.

.. code:: python

    from ocdsextensionregistry import ProfileBuilder

    builder = ProfileBuilder('1__1__4', {
        'lots': 'v1.1.4',
        'bids': 'v1.1.4',
    })

This initializes a profile of OCDS 1.1.4 with two extensions. Alternately, you can pass a list of extensions' metadata
URLs, base URLs, download URLs, and/or absolute paths to local directories, for example:

.. code:: python

    builder = ProfileBuilder('1__1__4', [
      'https://raw.githubusercontent.com/open-contracting-extensions/ocds_coveredBy_extension/master/extension.json',
      'https://raw.githubusercontent.com/open-contracting-extensions/ocds_options_extension/master/',
      'https://github.com/open-contracting-extensions/ocds_techniques_extension/archive/master.zip',
    ])

After initializing the profile, you can then:

-  :meth:`~ocdsextensionregistry.profile_builder.ProfileBuilder.release_schema_patch` to get the profile's patch of ``release-schema.json``
-  :meth:`~ocdsextensionregistry.profile_builder.ProfileBuilder.patched_release_schema` to get the patched version of ``release-schema.json``
-  :meth:`~ocdsextensionregistry.profile_builder.ProfileBuilder.extension_codelists` to get the profile's codelists
-  :meth:`~ocdsextensionregistry.profile_builder.ProfileBuilder.patched_codelists` to get the patched codelists
-  :meth:`~ocdsextensionregistry.profile_builder.ProfileBuilder.extensions` to iterate over the profile's versions of extensions
"""  # noqa: E501

import csv
import json
import logging
import os
import warnings
import zipfile
from collections.abc import Iterable
from io import StringIO
from urllib.parse import urljoin, urlsplit

import json_merge_patch
import requests

from ocdsextensionregistry.codelist import Codelist
from ocdsextensionregistry.exceptions import ExtensionWarning, UnsupportedSchemeError
from ocdsextensionregistry.extension_registry import ExtensionRegistry
from ocdsextensionregistry.extension_version import FIELD, ExtensionVersion
from ocdsextensionregistry.util import _resolve_zip, remove_nulls, replace_refs
from ocdsextensionregistry.versioned_release_schema import get_versioned_release_schema

logger = logging.getLogger("ocdsextensionregistry")


class ProfileBuilder:
    def __init__(
        self, standard_tag, extension_versions, registry_base_url=None, standard_base_url=None, schema_base_url=None
    ):
        """
        Accept an OCDS version and either a dictionary of extension identifiers and versions, or a list of extensions'
        metadata URLs, base URLs and/or download URLs, and initialize a reader of the extension registry.

        .. attention::

           This method is vulnerable to server-side request forgery (SSRF). A user can create a release package or
           record package whose extension URLs point to internal resources, which would receive a GET request.

        :param str standard_tag: the OCDS version tag, e.g. ``'1__1__4'``
        :param extension_versions: the extension versions
        :param str registry_base_url: the registry's base URL, defaults to
            ``'https://raw.githubusercontent.com/open-contracting/extension_registry/main/'``
        :param standard_base_url: the standard's base URL, defaults to
            ``f'https://codeload.github.com/open-contracting/standard/zip/{standard_tag}'``
            (can be a ``file://`` URL to a directory or a ZIP file, or the bytes of a ZIP file)
        :param str schema_base_url: the schema's base URL, e.g.
            ``'https://standard.open-contracting.org/profiles/ppp/schema/1__0__0__beta/'``
        :type standard_base_url: str or bytes
        :type extension_versions: dict or list
        """
        # Allows setting the registry URL to e.g. a pull request, when working on a profile.
        if not registry_base_url:
            registry_base_url = "https://raw.githubusercontent.com/open-contracting/extension_registry/main/"
        if not standard_base_url and standard_tag:
            standard_base_url = f"https://codeload.github.com/open-contracting/standard/zip/{standard_tag}"

        self.standard_tag = standard_tag
        self.extension_versions = extension_versions
        self.registry_base_url = registry_base_url
        self.standard_base_url = standard_base_url
        self.schema_base_url = schema_base_url
        self._registry = None
        self._file_cache = {}

    @property
    def registry(self):
        if self._registry is None:
            self._registry = ExtensionRegistry(f"{self.registry_base_url}extension_versions.csv")

        return self._registry

    @staticmethod
    def _extension_from_url(url, parsed):
        data = dict.fromkeys(["Id", "Date", "Version", "Base URL", "Download URL"])
        kwargs = {"input_url": url}
        if url.endswith("/extension.json"):
            data["Base URL"] = url[:-14]
        elif url.endswith("/"):
            data["Base URL"] = url
        # If the files are served via API, with the filename as a query string parameter.
        elif "extension.json" in url:
            kwargs["url_pattern"] = url.replace("extension.json", FIELD)
        elif "release-schema.json" in url:
            kwargs["url_pattern"] = url.replace("release-schema.json", FIELD)
        elif parsed.path.endswith(".json"):
            kwargs["file_urls"] = {"release-schema.json": url}
        else:
            data["Download URL"] = url
        return ExtensionVersion(data, **kwargs)

    def extensions(self):
        """Return the matching extension versions from the registry."""
        if isinstance(self.extension_versions, dict):
            for identifier, version in self.extension_versions.items():
                parsed = urlsplit(version)
                if parsed.scheme:
                    yield self._extension_from_url(version, parsed)
                else:
                    yield self.registry.get(id=identifier, version=version)
        elif isinstance(self.extension_versions, Iterable):
            for url in self.extension_versions:
                if not url or not isinstance(url, str):
                    continue
                yield self._extension_from_url(url, urlsplit(url))

    def release_schema_patch(self, *, extension_field=None, extension_value="name", language="en"):
        """
        Return the consolidated release schema patch.

        Use ``extension_field`` and ``extension_value`` to annotate each definition and field with the extension
        that defined or patched it.

        :param str extension_field: the name of the property to add to each definition and field in the extension
        :param str extension_value: the value of the property to add to each definition and field in the extension,
            either the 'name' or 'url'
        :param str language: the language to use for the name of the extension
        :warns ExtensionWarning: if the release schema patch's URL is not a supported scheme, if the request fails, if
            the bulk file is not a ZIP file, or if the release schema patch is not UTF-8 or not JSON
        :raises NotImplementedError: if the ``extension_value`` is not recognized
        """
        output = {}

        # Remove `null`, because removing fields or properties is prohibited.
        for extension in self.extensions():
            try:
                patch = json.loads(extension.remote("release-schema.json", default="{}"))
                remove_nulls(patch)
            except (
                UnicodeDecodeError,
                UnsupportedSchemeError,
                json.JSONDecodeError,
                requests.RequestException,
                zipfile.BadZipFile,
            ) as e:
                warnings.warn(ExtensionWarning(extension, e), stacklevel=2)
                continue
            if extension_field:
                if extension_value == "name":
                    value = extension.metadata["name"][language]
                elif extension_value == "url":
                    value = extension.get_url("release-schema.json")
                else:
                    raise NotImplementedError
                _add_extension_field(patch, value, extension_field)
            json_merge_patch.merge(output, patch)

        return output

    def patched_release_schema(self, *, schema=None, language="en", **kwargs):
        """
        Return the patched release schema.

        Use ``extension_field`` and ``extension_value`` to annotate each definition and field with the extension
        that defined or patched it.

        :param dict schema: the release schema
        :param str language: see :meth:`~ocdsextensionregistry.profile_builder.ProfileBuilder.release_schema_patch`
            and :meth:`~ocdsextensionregistry.profile_builder.ProfileBuilder.get_standard_file_contents`
        :param kwargs: see :meth:`~ocdsextensionregistry.profile_builder.ProfileBuilder.release_schema_patch`
        """
        if not schema:
            schema = json.loads(self.get_standard_file_contents("release-schema.json", language=language))

        json_merge_patch.merge(schema, self.release_schema_patch(language=language, **kwargs))

        if base := self.schema_base_url:
            schema["id"] = urljoin(base, "release-schema.json")

        return schema

    def release_package_schema(
        self, *, schema=None, patched=None, embed=False, proxies=False, language="en", **kwargs
    ):
        """
        Return a release package schema.

        If the profile builder was initialized with ``schema_base_url``, update schema URLs.

        :param dict schema: the base release package schema
        :param dict patched: the patched release schema
        :param bool embed: whether to embed or ``$ref``'erence the patched release schema
        :param bool proxies: whether to replace references with proxy objects
        :param str language: see :meth:`~ocdsextensionregistry.profile_builder.ProfileBuilder.release_schema_patch`
            and :meth:`~ocdsextensionregistry.profile_builder.ProfileBuilder.get_standard_file_contents`
        :param kwargs: see :meth:`~ocdsextensionregistry.profile_builder.ProfileBuilder.release_schema_patch`
        """
        if not schema:
            schema = json.loads(self.get_standard_file_contents("release-package-schema.json", language=language))

        if base := self.schema_base_url:
            schema["id"] = urljoin(base, "release-package-schema.json")
            if not embed:
                schema["properties"]["releases"]["items"]["$ref"] = urljoin(base, "release-schema.json")

        if embed or patched:
            if patched is None:
                patched = self.patched_release_schema(language=language, **kwargs)
            schema["properties"]["releases"]["items"] = replace_refs(patched, proxies=proxies)

        return schema

    def record_package_schema(self, *, schema=None, patched=None, embed=False, proxies=False, language="en", **kwargs):
        """
        Return a record package schema.

        If the profile builder was initialized with ``schema_base_url``, update schema URLs.

        :param dict schema: the base record package schema
        :param dict patched: the patched release schema
        :param bool proxies: whether to replace references with proxy objects
        :param bool embed: whether to embed or ``$ref``'erence the patched release schema
        :param str language: see :meth:`~ocdsextensionregistry.profile_builder.ProfileBuilder.release_schema_patch`
            and :meth:`~ocdsextensionregistry.profile_builder.ProfileBuilder.get_standard_file_contents`
        :param kwargs: see :meth:`~ocdsextensionregistry.profile_builder.ProfileBuilder.release_schema_patch`
        """
        if not schema:
            schema = json.loads(self.get_standard_file_contents("record-package-schema.json", language=language))

        properties = schema["definitions"]["record"]["properties"]

        if base := self.schema_base_url:
            schema["id"] = urljoin(base, "record-package-schema.json")
            if not embed:
                url = urljoin(base, "release-schema.json")
                properties["compiledRelease"]["$ref"] = url
                properties["releases"]["oneOf"][1]["items"]["$ref"] = url
                properties["versionedRelease"]["$ref"] = urljoin(base, "versioned-release-validation-schema.json")

        if embed or patched:
            if patched is None:
                patched = self.patched_release_schema(language=language, **kwargs)
            deref = replace_refs(patched, proxies=proxies)
            properties["compiledRelease"] = deref
            properties["releases"]["oneOf"][1]["items"] = deref
            properties["versionedRelease"] = replace_refs(
                get_versioned_release_schema(patched, self.standard_tag), proxies=proxies
            )

        return schema

    def standard_codelists(self):
        """Return the standard's codelists as :class:`~ocdsextensionregistry.codelist.Codelist` objects."""
        codelists = {}

        # Populate the file cache.
        self.get_standard_file_contents("release-schema.json")

        # This method shouldn't need to know about `_file_cache`.
        for path, content in self._file_cache["en"].items():
            name = os.path.basename(path)
            if "codelists" in path.split("/") and name:
                codelists[name] = Codelist(name)
                codelists[name].extend(csv.DictReader(StringIO(content)), "OCDS Core")

        return list(codelists.values())

    def extension_codelists(self):
        """
        Return the extensions' codelists as :class:`~ocdsextensionregistry.codelist.Codelist` objects.

        The extensions' codelists may be new, or may add codes to (+name.csv), remove codes from (-name.csv) or replace
        (name.csv) the codelists of the standard or other extensions.

        Codelist additions and removals are merged across extensions. If new codelists or codelist replacements differ
        across extensions, an error is raised.
        """
        codelists = {}

        # Keep the original content of codelists, to compare across extensions.
        originals = {}

        for extension in self.extensions():
            # We use the "codelists" field in extension.json (which standard-maintenance-scripts validates). An
            # extension is not guaranteed to offer a download URL, which is the only other way to get codelists.
            for name in extension.metadata.get("codelists", []):
                content = extension.remote(f"codelists/{name}")

                if name not in codelists:
                    codelists[name] = Codelist(name)
                    originals[name] = content
                elif not codelists[name].patch:
                    if originals[name] != content:
                        raise AssertionError(f"codelist {name} differs across extensions")
                    continue

                codelists[name].extend(csv.DictReader(StringIO(content)), extension.metadata["name"]["en"])

        # If a codelist replacement (name.csv) is consistent with additions (+name.csv) and removals (-name.csv), the
        # latter should be removed. In other words, the expectations are that:
        #
        # * A codelist replacement shouldn't omit added codes.
        # * A codelist replacement shouldn't include removed codes.
        # * If codes are added after a codelist is replaced, this should result in duplicate codes.
        # * If codes are removed after a codelist is replaced, this should result in no change.
        #
        # If these expectations are not met, an error is raised. As such, profile authors only have to handle cases
        # where codelist modifications are inconsistent across extensions.
        for codelist in list(codelists.values()):
            basename = codelist.basename
            if codelist.patch and basename in codelists:
                name = codelist.name
                codes = codelists[basename].codes
                if codelist.addend:
                    for row in codelist:
                        code = row["Code"]
                        if code not in codes:
                            warnings.warn(f"{code} added by {name}, but not in {basename}", stacklevel=2)
                    logger.info("%s has the codes added by %s - ignoring %s", basename, name, name)
                else:
                    for row in codelist:
                        code = row["Code"]
                        if code in codes:
                            warnings.warn(f"{code} removed by {name}, but in {basename}", stacklevel=2)
                    logger.info("%s has no codes removed by %s - ignoring %s", basename, name, name)
                del codelists[name]

        return list(codelists.values())

    def patched_codelists(self):
        """Return patched and new codelists as :class:`~ocdsextensionregistry.codelist.Codelist` objects."""
        codelists = {}

        for codelist in self.standard_codelists():
            codelists[codelist.name] = codelist

        for codelist in self.extension_codelists():
            if codelist.patch:
                basename = codelist.basename
                if codelist.addend:
                    # Add the rows.
                    codelists[basename].rows.extend(codelist.rows)
                    # Note that the rows may not all have the same columns, but DictWriter can handle this.
                else:
                    # Remove the codes. Multiple extensions can remove the same codes.
                    removed = codelist.codes
                    codelists[basename].rows = [row for row in codelists[basename] if row["Code"] not in removed]
            else:
                # Set or replace the rows.
                codelists[codelist.name] = codelist

        return list(codelists.values())

    def get_standard_file_contents(self, basename, language="en"):
        """
        Return the contents of the file within the standard.

        Download the given version of the standard, and cache the contents of files in the ``schema/`` directory.

        Replace the ``{{lang}}`` and ``{{version}}`` placeholders in files.

        :param str language: the string with which to replace ``{{lang}}`` placeholders
        """
        if language not in self._file_cache:
            zipfile = _resolve_zip(self.standard_base_url, "schema")
            names = zipfile.namelist()

            path = names[0]
            if self.standard_tag < "1__1__5":
                path += "standard/schema/"
            else:
                path += "schema/"
            start = len(path)

            cache = {}
            for name in names[1:]:
                if path in name:
                    # The ocds_babel.translate.translate() function makes these substitutions for published files.
                    cache[name[start:]] = (
                        zipfile.read(name)
                        .decode("utf-8")
                        .replace("{{lang}}", language)
                        .replace("{{version}}", ".".join(self.standard_tag.split("__")[:2]))
                    )

            # Set _file_cache at once, e.g. if threaded.
            self._file_cache[language] = cache

        return self._file_cache[language][basename]


def _add_extension_field(schema, extension_name, field_name, pointer=None):
    if pointer is None:
        pointer = ()
    if isinstance(schema, list):
        for item in schema:
            _add_extension_field(item, extension_name, field_name=field_name, pointer=pointer)
    elif isinstance(schema, dict):
        if len(pointer) > 1 and pointer[-2] in {"definitions", "properties"} and "title" in schema:
            schema[field_name] = extension_name
        for key, value in schema.items():
            _add_extension_field(value, extension_name, field_name=field_name, pointer=(*pointer, key))
