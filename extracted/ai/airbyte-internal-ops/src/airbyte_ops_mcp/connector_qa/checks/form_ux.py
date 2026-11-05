# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
from __future__ import annotations

import html
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, ClassVar, Iterable, Sequence, cast
from urllib.parse import urlsplit

import yaml
from airbyte_cdk.sources.declarative.parsers.manifest_reference_resolver import (
    CircularReferenceException,
    ManifestReferenceResolver,
    UndefinedReferenceException,
)

from airbyte_ops_mcp.connector_ops.utils import Connector, ConnectorLanguage
from airbyte_ops_mcp.connector_qa.models import (
    Check,
    CheckCategory,
    CheckResult,
    Finding,
)

HANDBOOK_URL = "https://docs.airbyte.com/platform/connector-development/ux-handbook"

SENTENCE_CASE_WORDS = frozenset(
    {
        "Airbyte",
        "Amazon",
        "Apple",
        "Asana",
        "Atlassian",
        "Auth0",
        "Avro",
        "AWS",
        "Azure",
        "BigQuery",
        "Bing",
        "Box",
        "Canva",
        "Cassandra",
        "ClickHouse",
        "Confluence",
        "Databricks",
        "Debezium",
        "Discord",
        "Docker",
        "Dropbox",
        "Duo",
        "Elastic",
        "Elasticsearch",
        "English",
        "Excel",
        "Facebook",
        "Figma",
        "Fivetran",
        "Freshdesk",
        "GCP",
        "GCS",
        "GitHub",
        "GitLab",
        "Gmail",
        "Google",
        "HubSpot",
        "Iceberg",
        "Instagram",
        "Intercom",
        "Jira",
        "Java",
        "Jinja",
        "Kafka",
        "Kinesis",
        "Klaviyo",
        "Kotlin",
        "Kubernetes",
        "LinkedIn",
        "Linux",
        "Mailchimp",
        "MariaDB",
        "Meta",
        "Microsoft",
        "Miro",
        "Monday",
        "MongoDB",
        "MySQL",
        "Netflix",
        "Notion",
        "Okta",
        "OpenSearch",
        "Oracle",
        "Outlook",
        "Parquet",
        "PayPal",
        "Pinterest",
        "Postgres",
        "PostgreSQL",
        "Prefect",
        "Python",
        "Redshift",
        "Redis",
        "Salesforce",
        "ServiceNow",
        "Shopify",
        "Slack",
        "Snowflake",
        "Spotify",
        "Square",
        "Stripe",
        "Tableau",
        "Terraform",
        "TikTok",
        "Trello",
        "Twitter",
        "Unix",
        "Workday",
        "YouTube",
        "Zendesk",
        "dbt",
    }
)
ALLOWLISTED_TITLE_PHRASES = frozenset(
    {"Amazon Seller Partner", "Azure Blob Storage", "Google Ads", "Google Sheets"}
)
MONTH_AND_DAY_NAMES = frozenset(
    {
        "April",
        "August",
        "December",
        "February",
        "Friday",
        "January",
        "July",
        "June",
        "March",
        "May",
        "Monday",
        "November",
        "October",
        "Saturday",
        "September",
        "Sunday",
        "Thursday",
        "Tuesday",
        "Wednesday",
    }
)
DESCRIPTION_STOPWORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "be",
        "for",
        "in",
        "is",
        "of",
        "on",
        "or",
        "the",
        "this",
        "to",
        "use",
        "used",
        "you",
        "your",
    }
)

_TITLE_EDGE_PUNCTUATION = "()[]\"',.:;"
_TITLE_TOKEN = re.compile(r"[^\s/-]+")
_TITLE_CASE_WORD = re.compile(r"^[A-Z][a-z]+$")
_DATE_PATTERN = re.compile(r"(\[0-9\]|\\d)\{4\}-")
_DATE_TIME_GROUP = re.compile(r"(?:\\d|\[0-9\])\{2\}:")
_URL = re.compile(
    r"""https?://[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+(?:[/?#][^\s<>"']*)?""",
    re.IGNORECASE,
)
_DOC_HOST_PREFIXES = (
    "docs.",
    "doc.",
    "developer.",
    "developers.",
    "dev.",
    "support.",
    "help.",
    "learn.",
)
_DOC_PATH_SEGMENTS = frozenset(
    {
        "docs",
        "doc",
        "documentation",
        "api",
        "reference",
        "guide",
        "guides",
        "help",
        "kb",
        "articles",
        "integrations",
        "knowledge",
        "developer",
    }
)
_UX04_EXCLUDED_KEY = re.compile(r"(^|_)(id|ids|key|token|secret|password)$")
_UX06_SECRET_KEY = re.compile(
    r"password|passwd|secret|token|api_?key|access_?key|private_?key|"
    r"credentials_json|service_account_info|session_key|signing_key"
)
_UX06_EXCLUDED_SUFFIX = re.compile(
    r"_(id|url|uri|type|name|path|date|at|time|timestamp|expiry_date|expiry|"
    r"expires_at|endpoint|header)$"
)
_UX09_VALUE_KEY = re.compile(
    r"(^|_)(id|key|token|secret|password|account|workspace|tenant|subdomain|"
    r"domain|organization|org|project)($|_)"
)
_UX09_WHERE_TERMS = (
    "find",
    "found",
    "located",
    "from your",
    "from the",
    "in your",
    "settings",
    "dashboard",
    "console",
    "portal",
    "go to",
    "navigate",
    "generate",
    "create",
    "obtain",
    "see ",
)


@dataclass(frozen=True)
class FormField:
    path: str
    config_path: tuple[str, ...]
    key: str
    schema: dict[str, Any]
    required: bool
    is_selector: bool
    is_discriminator: bool
    top_level: bool


@dataclass(frozen=True)
class FormUxContext:
    connector_name_words: frozenset[str]
    oauth_config_paths: frozenset[tuple[str, ...]]


class FormUxSpecError(Exception):
    pass


@lru_cache(maxsize=256)
def _resolve_spec_cached(manifest_text: str, spec_json: str) -> dict[str, Any]:
    manifest = yaml.safe_load(manifest_text)
    manifest["spec"] = json.loads(spec_json)
    return ManifestReferenceResolver().preprocess_manifest(manifest)["spec"]


def load_resolved_spec(connector: Connector) -> dict[str, Any]:
    spec = connector.connector_spec_file_content
    if not spec:
        raise FormUxSpecError(f"No spec found in {Path(connector.manifest_path).name}")

    manifest_text = Path(connector.manifest_path).resolve().read_text()
    spec_json = json.dumps(spec, sort_keys=True, default=str)
    try:
        return _resolve_spec_cached(manifest_text, spec_json)
    except (CircularReferenceException, UndefinedReferenceException) as exc:
        raise FormUxSpecError(str(exc)) from exc


def _walk_object(
    schema: dict[str, Any],
    display_path: str,
    config_path: tuple[str, ...],
    *,
    top_level: bool,
    inside_one_of: bool,
) -> Iterable[FormField]:
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        return
    required_values = schema.get("required")
    required_names = (
        set(required_values) if isinstance(required_values, list) else set()
    )
    for key, property_schema in properties.items():
        if not isinstance(key, str) or not isinstance(property_schema, dict):
            continue
        field_path = f"{display_path}.{key}" if display_path else key
        field_config_path = (*config_path, key)
        enum = property_schema.get("enum")
        yield FormField(
            path=field_path,
            config_path=field_config_path,
            key=key,
            schema=property_schema,
            required=key in required_names,
            is_selector="oneOf" in property_schema,
            is_discriminator=inside_one_of
            and (
                "const" in property_schema
                or (isinstance(enum, list) and len(enum) == 1)
            ),
            top_level=top_level,
        )
        yield from _walk_schema(
            property_schema,
            field_path,
            field_config_path,
            inside_one_of=inside_one_of,
        )


def _walk_schema(
    schema: dict[str, Any],
    display_path: str,
    config_path: tuple[str, ...],
    *,
    inside_one_of: bool,
) -> Iterable[FormField]:
    if schema.get("airbyte_hidden") is True:
        return
    yield from _walk_object(
        schema,
        display_path,
        config_path,
        top_level=False,
        inside_one_of=inside_one_of,
    )
    options = schema.get("oneOf")
    if isinstance(options, list):
        for index, option in enumerate(options):
            if isinstance(option, dict):
                yield from _walk_schema(
                    option,  # ty: ignore[invalid-argument-type] JSON Schema keys
                    f"{display_path}.oneOf[{index}]",
                    config_path,
                    inside_one_of=True,
                )
    items = schema.get("items")
    if isinstance(items, dict):
        yield from _walk_schema(
            items,
            f"{display_path}[]",
            config_path,
            inside_one_of=inside_one_of,
        )


def walk_form_fields(spec: dict[str, Any]) -> Iterable[FormField]:
    connection_specification = spec.get("connection_specification")
    if isinstance(connection_specification, dict):
        yield from _walk_object(
            connection_specification, "", (), top_level=True, inside_one_of=False
        )


def _visible_fields(spec: dict[str, Any]) -> Iterable[FormField]:
    for form_field in walk_form_fields(spec):
        if (
            form_field.schema.get("airbyte_hidden") is True
            or form_field.is_discriminator
        ):
            continue
        yield form_field


def _words(text: str) -> set[str]:
    return set(re.findall(r"[^\W_]+", text.lower(), flags=re.UNICODE))


def _plain_text(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]*>", " ", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"[*_~#>]+", " ", text)
    return html.unescape(text)


def _normalized_words(text: str) -> set[str]:
    return set(re.findall(r"[^\W_]+", _plain_text(text).lower(), flags=re.UNICODE))


def _schema_types(schema: dict[str, Any]) -> set[str]:
    type_value = schema.get("type")
    if isinstance(type_value, str):
        return {type_value}
    if isinstance(type_value, list):
        return {value for value in type_value if isinstance(value, str)}
    return set()


def _is_multi_value_enum(schema: dict[str, Any]) -> bool:
    enum = schema.get("enum")
    return isinstance(enum, list) and len(enum) > 1


def _oauth_config_paths(spec: dict[str, Any]) -> frozenset[tuple[str, ...]]:
    advanced_auth = spec.get("advanced_auth")
    oauth_config = (
        advanced_auth.get("oauth_config_specification")
        if isinstance(advanced_auth, dict)
        else None
    )
    output_specification = (
        oauth_config.get("complete_oauth_output_specification")
        if isinstance(oauth_config, dict)
        else None
    )
    properties = (
        output_specification.get("properties")
        if isinstance(output_specification, dict)
        else None
    )
    if not isinstance(properties, dict):
        return frozenset()

    paths: set[tuple[str, ...]] = set()
    for output_field in properties.values():
        if not isinstance(output_field, dict):
            continue
        config_path = output_field.get("path_in_connector_config")
        if isinstance(config_path, (list, tuple)):
            path = tuple(str(part) for part in config_path if str(part))
        elif isinstance(config_path, str):
            path = tuple(part for part in re.split(r"[./\[\]]+", config_path) if part)
        else:
            continue
        if path:
            paths.add(path)
    return frozenset(paths)


def _context_for(connector: Connector, spec: dict[str, Any]) -> FormUxContext:
    return FormUxContext(
        connector_name_words=frozenset(_words(connector.name_from_metadata or "")),
        oauth_config_paths=_oauth_config_paths(spec),
    )


def _title_case_offenses(
    title: str, connector_name_words: frozenset[str]
) -> list[tuple[re.Match[str], str]]:
    phrase_spans = []
    for phrase in sorted(ALLOWLISTED_TITLE_PHRASES, key=len, reverse=True):
        pattern = re.compile(rf"(?<![\w]){re.escape(phrase)}(?![\w])")
        phrase_spans.extend(
            (match.start(), match.end()) for match in pattern.finditer(title)
        )

    offenses: list[tuple[re.Match[str], str]] = []
    first_word_seen = False
    for match in _TITLE_TOKEN.finditer(title):
        raw_word = match.group()
        word = raw_word.strip(_TITLE_EDGE_PUNCTUATION)
        if not word:
            continue
        leading = len(raw_word) - len(raw_word.lstrip(_TITLE_EDGE_PUNCTUATION))
        word_start = match.start() + leading
        word_end = word_start + len(word)
        if any(start <= word_start and word_end <= end for start, end in phrase_spans):
            first_word_seen = True
            continue
        internally_capitalized = any(char.isupper() for char in word[1:])
        if not first_word_seen:
            if (
                word[0].islower()
                and not internally_capitalized
                and word not in SENTENCE_CASE_WORDS
            ):
                offenses.append((match, "capitalize"))
            first_word_seen = True
        elif (
            _TITLE_CASE_WORD.fullmatch(word)
            and word not in SENTENCE_CASE_WORDS
            and word.lower() not in connector_name_words
            and word not in MONTH_AND_DAY_NAMES
            and not internally_capitalized
        ):
            offenses.append((match, "lower"))
    return offenses


def _suggest_title(title: str, offenses: list[tuple[re.Match[str], str]]) -> str:
    suggestion = title
    for match, case_action in reversed(offenses):
        raw_word = suggestion[match.start() : match.end()]
        leading = len(raw_word) - len(raw_word.lstrip(_TITLE_EDGE_PUNCTUATION))
        trailing = len(raw_word) - len(raw_word.rstrip(_TITLE_EDGE_PUNCTUATION))
        end = len(raw_word) - trailing if trailing else len(raw_word)
        word = raw_word[leading:end]
        if not word:
            continue
        replacement = (
            word[0].upper() + word[1:] if case_action == "capitalize" else word.lower()
        )
        suggestion = (
            suggestion[: match.start()]
            + raw_word[:leading]
            + replacement
            + (raw_word[end:] if end < len(raw_word) else "")
            + suggestion[match.end() :]
        )
    return suggestion


def _extract_urls(text: str) -> list[str]:
    urls = []
    for match in _URL.finditer(text):
        url = match.group().rstrip(".,;:!?)]}\\\"'")
        if url:
            urls.append(url)
    return urls


def _is_documentation_url(url: str) -> bool:
    parsed_url = urlsplit(url)
    host = parsed_url.hostname or ""
    if any(host.startswith(prefix) for prefix in _DOC_HOST_PREFIXES):
        return True
    path_segments = {
        segment.lower() for segment in parsed_url.path.split("/") if segment
    }
    return bool(path_segments & _DOC_PATH_SEGMENTS)


class FormUxCheck(Check):
    blocking: ClassVar[bool] = False
    category = CheckCategory.FORM_UX
    applies_to_connector_languages: ClassVar[list[ConnectorLanguage]] = [
        ConnectorLanguage.MANIFEST_ONLY
    ]
    rule_id: ClassVar[str]
    anchor: ClassVar[str]
    name: ClassVar[str]
    description: ClassVar[str]

    def find(self, spec: dict[str, Any], ctx: FormUxContext) -> list[Finding]:
        raise NotImplementedError

    def _finding(self, field: FormField, message: str) -> Finding:
        return Finding(self.rule_id, field.path, message, self.anchor)

    def _run(self, connector: Connector) -> CheckResult:
        try:
            spec = load_resolved_spec(connector)
        except FormUxSpecError as exc:
            return self.fail(connector, str(exc))

        findings = self.find(spec, _context_for(connector, spec))
        if not findings:
            return self.pass_(connector, "No Form UX findings")
        finding_lines = "\n".join(
            f"- {finding.field_path}: {finding.message}" for finding in findings
        )
        return self.fail(
            connector,
            f"{len(findings)} finding(s). See {self.anchor}\n{finding_lines}",
            findings=findings,
        )


class CheckFormUx01(FormUxCheck):
    rule_id = "UX-01"
    anchor = f"{HANDBOOK_URL}#ux-01"
    name = "UX-01: Every field has a title and description"
    description = (
        "Give every user-facing field a clear `title` and `description`. The description "
        "should help the user understand what to enter.\n\n"
        "Exception: A `oneOf` selector and its discriminator `const` fields do not need "
        "their own title and description.\n\n"
        f"See [UX-01 in the Connector UX Handbook]({anchor})."
    )

    def find(self, spec: dict[str, Any], ctx: FormUxContext) -> list[Finding]:
        findings = []
        for field in _visible_fields(spec):
            if field.is_selector:
                continue
            missing = [
                label
                for label in ("title", "description")
                if not isinstance(field.schema.get(label), str)
                or not field.schema[label].strip()
            ]
            if missing:
                findings.append(
                    self._finding(field, f"Missing {' and '.join(missing)}")
                )
        return findings


class CheckFormUx02(FormUxCheck):
    rule_id = "UX-02"
    anchor = f"{HANDBOOK_URL}#ux-02"
    name = "UX-02: Titles use sentence case"
    description = (
        "Write titles in sentence case: capitalize the first word and proper nouns, not "
        "every word. Keep product names and acronyms correctly capitalized.\n\n"
        "Exception: Preserve capitalization in product names and acronyms, such as "
        "“API key” and “Azure Blob Storage.”\n\n"
        f"See [UX-02 in the Connector UX Handbook]({anchor})."
    )

    def find(self, spec: dict[str, Any], ctx: FormUxContext) -> list[Finding]:
        findings = []
        for field in _visible_fields(spec):
            title = field.schema.get("title")
            if not isinstance(title, str) or not title.strip():
                continue
            offenses = _title_case_offenses(title, ctx.connector_name_words)
            if offenses:
                suggestion = _suggest_title(title, offenses)
                findings.append(
                    self._finding(
                        field,
                        f'Title "{title}" is not sentence case; try "{suggestion}"',
                    )
                )
        return findings


class CheckFormUx03(FormUxCheck):
    rule_id = "UX-03"
    anchor = f"{HANDBOOK_URL}#ux-03"
    name = "UX-03: Description says more than the title"
    description = (
        "Explain the field's purpose in its description instead of repeating its title. "
        "Add context that helps the user choose a value.\n\n"
        f"See [UX-03 in the Connector UX Handbook]({anchor})."
    )

    def find(self, spec: dict[str, Any], ctx: FormUxContext) -> list[Finding]:
        findings = []
        for field in _visible_fields(spec):
            description = field.schema.get("description")
            if not isinstance(description, str) or not description.strip():
                continue
            title = field.schema.get("title")
            title_words = _normalized_words(title if isinstance(title, str) else "")
            description_words = _normalized_words(description)
            ignored = DESCRIPTION_STOPWORDS | ctx.connector_name_words
            title_words -= ignored
            description_words -= ignored
            if description_words <= title_words:
                findings.append(
                    self._finding(
                        field,
                        "Description repeats the title; add context that helps users choose a value",
                    )
                )
        return findings


class CheckFormUx04(FormUxCheck):
    rule_id = "UX-04"
    anchor = f"{HANDBOOK_URL}#ux-04"
    name = "UX-04: Required fields have a default when a safe value exists"
    description = (
        "Give required fields a default when a safe value exists. A common region or "
        "`is_sandbox: false` can be a safe default; never default credentials or IDs.\n\n"
        f"See [UX-04 in the Connector UX Handbook]({anchor})."
    )

    def find(self, spec: dict[str, Any], ctx: FormUxContext) -> list[Finding]:
        findings = []
        for field in _visible_fields(spec):
            schema = field.schema
            if not field.required or field.is_selector or "default" in schema:
                continue
            if schema.get("airbyte_secret") is True or _UX04_EXCLUDED_KEY.search(
                field.key.lower()
            ):
                continue
            if _schema_types(schema) & {
                "boolean",
                "integer",
                "number",
            } or _is_multi_value_enum(schema):
                findings.append(
                    self._finding(
                        field,
                        "Required field has no default; add one if a safe value exists",
                    )
                )
        return findings


class CheckFormUx05(FormUxCheck):
    rule_id = "UX-05"
    anchor = f"{HANDBOOK_URL}#ux-05"
    name = "UX-05: `pattern` has a readable `pattern_descriptor`"
    description = (
        "When you validate a value with `pattern`, provide a readable "
        "`pattern_descriptor`. Describe the expected format rather than relying on users "
        "to interpret a regular expression.\n\n"
        f"See [UX-05 in the Connector UX Handbook]({anchor})."
    )

    def find(self, spec: dict[str, Any], ctx: FormUxContext) -> list[Finding]:
        findings = []
        for field in _visible_fields(spec):
            schema = field.schema
            if "pattern" not in schema:
                continue
            descriptor = schema.get("pattern_descriptor")
            if not isinstance(descriptor, str) or not descriptor.strip():
                message = "Add a readable pattern_descriptor"
            elif any(
                token in descriptor for token in ("\\", "[", "]", "^", "(?", ".*")
            ) or descriptor.endswith("$"):
                message = (
                    "pattern_descriptor should describe the format in plain language, "
                    "not look like a regular expression"
                )
            else:
                continue
            findings.append(self._finding(field, message))
        return findings


class CheckFormUx06(FormUxCheck):
    rule_id = "UX-06"
    anchor = f"{HANDBOOK_URL}#ux-06"
    name = "UX-06: Secrets marked `airbyte_secret`"
    description = (
        "Mark every secret field with `airbyte_secret: true`. Do not mark public values, "
        "IDs, or other non-secret fields as secrets.\n\n"
        f"See [UX-06 in the Connector UX Handbook]({anchor})."
    )

    def find(self, spec: dict[str, Any], ctx: FormUxContext) -> list[Finding]:
        findings = []
        for field in _visible_fields(spec):
            schema = field.schema
            key = field.key.lower()
            if (
                "string" not in _schema_types(schema)
                or schema.get("airbyte_secret") is True
                or schema.get("format") in {"date", "date-time"}
                or "const" in schema
                or "enum" in schema
                or not _UX06_SECRET_KEY.search(key)
                or _UX06_EXCLUDED_SUFFIX.search(key)
            ):
                continue
            findings.append(
                self._finding(field, "Secret field is missing airbyte_secret: true")
            )
        return findings


class CheckFormUx08(FormUxCheck):
    rule_id = "UX-08"
    anchor = f"{HANDBOOK_URL}#ux-08"
    name = "UX-08: Explain meaning and impact"
    description = (
        "Explain what a field controls and how changing it affects the data, sync, or "
        "output. Give users enough context to choose a value.\n\n"
        f"See [UX-08 in the Connector UX Handbook]({anchor})."
    )

    def find(self, spec: dict[str, Any], ctx: FormUxContext) -> list[Finding]:
        findings = []
        for field in _visible_fields(spec):
            schema = field.schema
            description = schema.get("description")
            if not isinstance(description, str) or not description.strip():
                continue
            types = _schema_types(schema)
            behavior_field = (
                bool(types & {"integer", "number", "boolean"})
                or _is_multi_value_enum(schema)
                or "array" in types
                or ("string" in types and schema.get("format") in {"date", "date-time"})
            )
            if (
                behavior_field
                and schema.get("airbyte_secret") is not True
                and len(_plain_text(description).strip()) < 80
            ):
                findings.append(
                    self._finding(
                        field,
                        "Description is short; explain what the field controls and how it affects the sync",
                    )
                )
        return findings


class CheckFormUx09(FormUxCheck):
    rule_id = "UX-09"
    anchor = f"{HANDBOOK_URL}#ux-09"
    name = "UX-09: Say where to get each value"
    description = (
        "Tell users where to find each value they must provide. Link to setup instructions "
        "when they can explain the steps.\n\n"
        "Exception: Do not apply this rule to fields OAuth fills in through "
        "`advanced_auth.complete_oauth_output_specification`.\n\n"
        f"See [UX-09 in the Connector UX Handbook]({anchor})."
    )

    def find(self, spec: dict[str, Any], ctx: FormUxContext) -> list[Finding]:
        findings = []
        for field in _visible_fields(spec):
            schema = field.schema
            description = schema.get("description")
            if not isinstance(description, str) or not description.strip():
                continue
            description_text = description
            key = field.key.lower()
            must_obtain = schema.get("airbyte_secret") is True or (
                "string" in _schema_types(schema) and _UX09_VALUE_KEY.search(key)
            )
            if (
                not must_obtain
                or field.config_path in ctx.oauth_config_paths
                or re.search(r"https?://|<a\s|\]\(", description_text, re.IGNORECASE)
                or any(term in description_text.lower() for term in _UX09_WHERE_TERMS)
            ):
                continue
            findings.append(
                self._finding(
                    field,
                    "Description does not say where to find or obtain this value",
                )
            )
        return findings


class CheckFormUx10(FormUxCheck):
    rule_id = "UX-10"
    anchor = f"{HANDBOOK_URL}#ux-10"
    name = "UX-10: Doc links point to anchors"
    description = (
        "For documentation links, link to the relevant heading or setup section when a "
        "page has one. Use a stable, current URL rather than sending users to a page's "
        "top-level overview.\n\n"
        f"See [UX-10 in the Connector UX Handbook]({anchor})."
    )

    def find(self, spec: dict[str, Any], ctx: FormUxContext) -> list[Finding]:
        findings = []
        for field in _visible_fields(spec):
            description = field.schema.get("description")
            if not isinstance(description, str):
                continue
            for url in _extract_urls(description):
                if _is_documentation_url(url) and not urlsplit(url).fragment:
                    findings.append(
                        self._finding(
                            field,
                            f"Link to the relevant section (#anchor) when the page has one: {url}",
                        )
                    )
        return findings


class CheckFormUx11(FormUxCheck):
    rule_id = "UX-11"
    anchor = f"{HANDBOOK_URL}#ux-11"
    name = "UX-11: Auth is not entirely optional"
    description = (
        "Put the method selector (`credentials`) in the top-level `required` list and "
        "define one `oneOf` option per authentication method. If anonymous access is "
        "supported, represent **No auth** as an explicit option rather than making the "
        "selector optional; GitHub, HubSpot, and Jira manifests demonstrate required "
        "selectors with method options.\n\n"
        "Exception: Deliberately optional credentials, such as a public API key or a "
        "database password that can be omitted, are still reported. You can ignore the "
        "finding when the connector intentionally supports that configuration.\n\n"
        f"See [UX-11 in the Connector UX Handbook]({anchor})."
    )
    _OPTIONAL_CREDENTIALS_SUFFIX = "If credentials are deliberately optional (for example, a public API), you can ignore this."

    def find(self, spec: dict[str, Any], ctx: FormUxContext) -> list[Finding]:
        connection_specification = spec.get("connection_specification")
        if not isinstance(connection_specification, dict):
            return []
        top_level_fields = [field for field in _visible_fields(spec) if field.top_level]
        selector_names = {
            "credentials",
            "authorization",
            "authentication",
            "auth",
            "auth_method",
        }
        selectors = [
            field
            for field in top_level_fields
            if field.key in selector_names
            and ("oneOf" in field.schema or "object" in _schema_types(field.schema))
        ]
        if selectors:
            return [
                self._finding(
                    field,
                    "Authentication selector should be required. "
                    + self._OPTIONAL_CREDENTIALS_SUFFIX,
                )
                for field in selectors
                if not field.required
            ]

        secrets = [
            field
            for field in top_level_fields
            if field.schema.get("airbyte_secret") is True
        ]
        if secrets and not any(field.required for field in secrets):
            return [
                Finding(
                    self.rule_id,
                    "connection_specification",
                    "Top-level secret fields are all optional. "
                    + self._OPTIONAL_CREDENTIALS_SUFFIX,
                    self.anchor,
                )
            ]
        return []


class CheckFormUx12(FormUxCheck):
    rule_id = "UX-12"
    anchor = f"{HANDBOOK_URL}#ux-12"
    name = "UX-12: Date pattern also sets `format: date`/`date-time`"
    description = (
        "For a date or date-time field, set `type: string`, the matching `format`, and a "
        "`pattern` with a readable `pattern_descriptor`. Use `date` for a date and "
        "`date-time` when the value includes a time.\n\n"
        f"See [UX-12 in the Connector UX Handbook]({anchor})."
    )

    def find(self, spec: dict[str, Any], ctx: FormUxContext) -> list[Finding]:
        findings = []
        for field in _visible_fields(spec):
            pattern = field.schema.get("pattern")
            date_match = (
                _DATE_PATTERN.search(pattern) if isinstance(pattern, str) else None
            )
            if date_match is None:
                continue
            trailing_pattern = cast(str, pattern)[date_match.end() :]
            matches_time = (
                any(marker in trailing_pattern for marker in ("T", ":", r"\s"))
                or _DATE_TIME_GROUP.search(trailing_pattern) is not None
            )
            allowed_formats = {"date-time"} if matches_time else {"date", "date-time"}
            if (
                "string" not in _schema_types(field.schema)
                or field.schema.get("format") not in allowed_formats
            ):
                findings.append(
                    self._finding(
                        field,
                        "Date-like pattern requires type: string and format: date or date-time",
                    )
                )
        return findings


ENABLED_CHECKS: list[FormUxCheck] = [
    CheckFormUx01(),
    CheckFormUx02(),
    CheckFormUx03(),
    CheckFormUx04(),
    CheckFormUx05(),
    CheckFormUx06(),
    CheckFormUx08(),
    CheckFormUx09(),
    CheckFormUx10(),
    CheckFormUx11(),
    CheckFormUx12(),
]


def render_form_ux_summary(results: Sequence[CheckResult]) -> str:
    findings_by_connector: dict[str, dict[str, list[Finding]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for result in results:
        if result.check.category != CheckCategory.FORM_UX or not result.findings:
            continue
        connector_name = getattr(result.connector, "technical_name", None)
        if not isinstance(connector_name, str) or not connector_name:
            connector_name = getattr(result.connector, "name_from_metadata", None)
        if not isinstance(connector_name, str) or not connector_name:
            connector_name = str(result.connector)
        for finding in result.findings:
            findings_by_connector[connector_name][finding.rule_id].append(finding)

    sections = []
    for connector_name in sorted(findings_by_connector):
        rules = findings_by_connector[connector_name]
        lines = [
            f"### Form UX: {connector_name}",
            "",
            "| Rule ID | Findings | Handbook link |",
            "| --- | ---: | --- |",
        ]
        rule_ids = sorted(rules, key=lambda rule_id: int(rule_id.split("-")[1]))
        for rule_id in rule_ids:
            rule_findings = rules[rule_id]
            lines.append(
                f"| {rule_id} | {len(rule_findings)} | [Handbook]({rule_findings[0].anchor}) |"
            )
        for rule_id in rule_ids:
            rule_findings = rules[rule_id]
            lines.extend(
                [
                    "",
                    f"<details><summary>{rule_id} ({len(rule_findings)})</summary>",
                    "",
                ]
            )
            lines.extend(
                f"- {finding.field_path}: {finding.message}"
                for finding in rule_findings
            )
            lines.extend(["", "</details>"])
        sections.append("\n".join(lines))
    return "\n\n".join(sections)
