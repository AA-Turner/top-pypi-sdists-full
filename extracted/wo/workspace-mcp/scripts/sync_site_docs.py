# ruff: noqa

"""Keep the workspacemcp.com docs in step with a google_workspace_mcp release.

The work splits along a line drawn by how much of it a script can honestly do:

* **Mechanical.** Which release the docs were checked against, and when. Those
  are facts, so ``src/lib/version.ts`` is rewritten in place.
* **Semantic.** Tool inventories, parameter lists, environment variables — every
  one of these carries prose a script has no business inventing. So they are
  *checked*, not written: the release's own diff is mined for anything the site
  does not yet describe, and the result comes back as a review list.

The site lives in a separate repository, so nothing here stages or commits. It
edits the version pin, reports the drift, and leaves both to a human.
"""

import argparse
import ast
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

DEFAULT_SITE_REPO = Path.home() / "git" / "workspacesite"
SITE_REPO_ENV = "WORKSPACE_SITE_REPO"

# Site files this script knows how to read. VERSION_TS doubles as the marker
# that identifies a directory as the site repo.
VERSION_TS = Path("src/lib/version.ts")
TOOLS_TS = Path("src/lib/tools.ts")
SITE_SOURCE_DIR = Path("src")
SITE_TEXT_SUFFIXES = {".svelte", ".ts", ".js", ".md", ".html", ".json"}

# Injected by the tool decorators rather than supplied by the caller; the site
# documents neither, and shouldn't.
IMPLICIT_TOOL_PARAMS = {"service", "user_google_email"}

# Runtime plumbing rather than user-facing configuration — never documented, so
# flagging them as missing would be noise.
IGNORED_ENV_PREFIXES = ("OTEL_", "FASTMCP_", "INTEGRATION_TEST_")
IGNORED_ENV_VARS = {"HOME", "NO_COLOR", "PATH", "PORT", "TERM"}

# --- tools.ts parsing -------------------------------------------------------
# The literal in tools.ts is hand-maintained but rigidly formatted, which is
# what makes these patterns safe. A tool name either ends its line (multi-line
# form) or is followed by `tier:` (single-line form); a parameter name is always
# followed by `required:`. Nothing else in the file looks like either.
SITE_SLUG_RE = re.compile(r"^\s*'([a-z0-9-]+)': \{\s*$")
SOURCE_RE = re.compile(r"source: '([^']+)'")
TOOL_NAME_RE = re.compile(r"name: '([^']+)',(?:\s*$|\s*tier:)")
PARAM_RE = re.compile(r"\{ name: '([^']+)', required: (true|false)")

ENV_NAME_RE = re.compile(r"[A-Z][A-Z0-9_]{3,}")


def git(args, cwd, check=True):
    """Runs git in `cwd` and returns stdout, or "" when a checked-off call fails."""
    result = subprocess.run(
        ["git", *args], cwd=str(cwd), capture_output=True, text=True, encoding="utf-8"
    )
    if result.returncode != 0:
        if check:
            raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
        return ""
    return result.stdout


def resolve_site_repo(explicit=None):
    """Finds the site checkout from the flag, the environment, then the default."""
    for candidate in (explicit, os.environ.get(SITE_REPO_ENV), DEFAULT_SITE_REPO):
        if not candidate:
            continue
        path = Path(candidate).expanduser()
        if (path / VERSION_TS).exists():
            return path
    return None


def resolve_previous_tag(tag):
    """Returns the tag released before `tag`, or None if it is the first."""
    previous = git(
        ["describe", "--tags", "--abbrev=0", f"{tag}^"], cwd=REPO_ROOT, check=False
    ).strip()
    return previous or None


# --- Mechanical: the docs version pin ---------------------------------------


def update_version_pin(site_repo, tag, synced_at, write=True):
    """Points DOCS_RELEASE/DOCS_SYNCED_AT at this release. Returns a status dict."""
    path = site_repo / VERSION_TS
    original = path.read_text(encoding="utf-8")

    current_release = re.search(r"DOCS_RELEASE = '([^']*)'", original)
    current_synced = re.search(r"DOCS_SYNCED_AT = '([^']*)'", original)
    if not current_release or not current_synced:
        raise RuntimeError(
            f"{VERSION_TS} does not declare DOCS_RELEASE and DOCS_SYNCED_AT as expected"
        )

    updated = re.sub(
        r"(DOCS_RELEASE = ')[^']*(')", rf"\g<1>{tag}\g<2>", original, count=1
    )
    updated = re.sub(
        r"(DOCS_SYNCED_AT = ')[^']*(')", rf"\g<1>{synced_at}\g<2>", updated, count=1
    )

    status = {
        "file": str(VERSION_TS),
        "previous_release": current_release.group(1),
        "previous_synced_at": current_synced.group(1),
        "release": tag,
        "synced_at": synced_at,
        "changed": updated != original,
        "written": False,
    }
    if status["changed"] and write:
        path.write_text(updated, encoding="utf-8")
        status["written"] = True
    return status


# --- Semantic: tool and parameter drift -------------------------------------


def _is_server_tool(decorator):
    """True for `@server.tool` and `@server.tool(...)`."""
    node = decorator.func if isinstance(decorator, ast.Call) else decorator
    return (
        isinstance(node, ast.Attribute)
        and node.attr == "tool"
        and isinstance(node.value, ast.Name)
        and node.value.id == "server"
    )


def _signature_params(node):
    """Maps each caller-supplied parameter to whether it is required."""
    args = node.args
    positional = [*args.posonlyargs, *args.args]
    first_defaulted = len(positional) - len(args.defaults)
    params = {}
    for index, arg in enumerate(positional):
        if arg.arg not in IMPLICIT_TOOL_PARAMS:
            params[arg.arg] = index < first_defaulted
    for arg, default in zip(args.kwonlyargs, args.kw_defaults):
        if arg.arg not in IMPLICIT_TOOL_PARAMS:
            params[arg.arg] = default is None
    return params


def _module_source(source, rev=None):
    """Reads a module from the working tree, or from a revision. "" if absent."""
    if rev is None:
        path = REPO_ROOT / source
        return path.read_text(encoding="utf-8") if path.exists() else ""
    return git(["show", f"{rev}:{source}"], cwd=REPO_ROOT, check=False)


def _factory_tools(tree):
    """Tool names produced by `create_comment_tools("document", ...)` and friends.

    These are registered by calling `server.tool(...)` on a renamed closure, so
    no decorator scan can see them — but the names are a pure function of the
    factory's first argument, and the site documents them with no parameters.
    """
    names = {}
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "create_comment_tools"
            and node.args
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
        ):
            app = node.args[0].value
            names[f"list_{app}_comments"] = {}
            names[f"manage_{app}_comment"] = {}
    return names


def python_tools(source, rev=None):
    """Extracts {tool_name: {param: required}} from a *_tools.py module."""
    text = _module_source(source, rev)
    if not text:
        return {}
    tree = ast.parse(text, filename=source)
    tools = {
        node.name: _signature_params(node)
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and any(_is_server_tool(d) for d in node.decorator_list)
    }
    tools.update(_factory_tools(tree))
    return tools


def known_tool_names():
    """Every tool name the server registers, wherever it is defined.

    Some tools a service page lists are not defined in that service's module —
    `start_google_auth` lives in `core/server.py`, for one — so a name missing
    from the module it is filed under is only stale if it is missing everywhere.
    """
    tracked = git(["ls-files", "*.py"], cwd=REPO_ROOT).split()
    names = set()
    for path in tracked:
        if path.startswith("tests/"):
            continue
        names.update(python_tools(path))
    return names


def site_tools(tools_ts):
    """Parses tools.ts into {slug: {source, tools: {name: {param: required}}}}."""
    services = {}
    service = None
    tool = None

    for line in tools_ts.read_text(encoding="utf-8").splitlines():
        slug = SITE_SLUG_RE.match(line)
        if slug:
            service = {"source": None, "tools": {}}
            services[slug.group(1)] = service
            tool = None
            continue
        if service is None:
            continue

        source = SOURCE_RE.search(line)
        if source:
            service["source"] = source.group(1)
            continue

        name = TOOL_NAME_RE.search(line)
        if name:
            tool = name.group(1)
            service["tools"][tool] = {}
        if tool is not None:
            for param, required in PARAM_RE.findall(line):
                service["tools"][tool][param] = required == "true"

    if not services:
        raise RuntimeError(
            f"parsed no services out of {tools_ts} — has its shape changed?"
        )
    return services


def tool_drift(services, tag, previous_tag):
    """Compares each documented service against the module it claims to mirror.

    The site documents a curated subset of each tool's parameters on purpose, so
    "this parameter isn't on the page" is an editorial choice, not drift — the
    only exception being a parameter *this release added*, which nobody has had
    the chance to write up yet. Everything else reported here is a genuine
    contradiction: a page describing something the code no longer does.

    Contradictions are judged against the working tree, since that is what the
    site has to agree with. The "added by this release" delta is judged between
    the two tags, which is the same thing immediately after a release and stays
    truthful when the tool is pointed at an older one.
    """
    new_work, stale = [], []
    registered = known_tool_names()

    for slug, service in sorted(services.items()):
        source = service["source"]
        if not source:
            stale.append(f"`{slug}` declares no `source:` module")
            continue
        if not (REPO_ROOT / source).exists():
            stale.append(f"`{slug}` points at `{source}`, which no longer exists")
            continue

        in_code = python_tools(source)
        released = python_tools(source, tag)
        before = python_tools(source, previous_tag) if previous_tag else released
        on_site = service["tools"]

        for name in sorted(set(released) - set(before) - set(on_site)):
            new_work.append(f"`{slug}`: new tool `{name}` is not on the site yet")
        for name in sorted(set(on_site) - set(in_code) - registered):
            stale.append(f"`{slug}`: site documents `{name}`, which no longer exists")

        for name in sorted(set(released) & set(on_site)):
            added = set(released[name]) - set(before.get(name, {}))
            for param in sorted(added - set(on_site[name])):
                new_work.append(
                    f"`{slug}.{name}`: new parameter `{param}` is not documented"
                )

        for name in sorted(set(in_code) & set(on_site)):
            params, documented = in_code[name], on_site[name]
            for param in sorted(set(documented) - set(params)):
                stale.append(
                    f"`{slug}.{name}`: documented parameter `{param}` no longer exists"
                )
            for param in sorted(set(params) & set(documented)):
                if params[param] != documented[param]:
                    stale.append(
                        f"`{slug}.{name}`: `{param}` is "
                        f"{'required' if params[param] else 'optional'} in code, "
                        f"documented as {'required' if documented[param] else 'optional'}"
                    )

    return new_work, stale


# --- Semantic: what this release actually touched ---------------------------


def changed_tool_modules(services, previous_tag, tag):
    """Documented modules with commits between the two tags, as (slug, source)."""
    if not previous_tag:
        return []
    changed = set(
        git(["diff", "--name-only", f"{previous_tag}..{tag}"], cwd=REPO_ROOT).split()
    )
    return [
        (slug, service["source"])
        for slug, service in sorted(services.items())
        if service["source"] in changed
    ]


def _env_vars_in(text, filename):
    """Environment variables read by one module.

    Resolves module-level constants as well as literals, because the settings
    worth documenting tend to be the ones named once and reused —
    `os.getenv(_ALLOW_NULL_ORIGIN_CONSENT_ENV)` is invisible to a text search.
    """
    if not text:
        return set()
    try:
        tree = ast.parse(text, filename=filename)
    except SyntaxError:
        return set()

    constants = {
        target.id: node.value.value
        for node in tree.body
        if isinstance(node, ast.Assign)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
        for target in node.targets
        if isinstance(target, ast.Name)
    }

    found = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not node.args:
            continue
        func = node.func
        if not isinstance(func, ast.Attribute):
            continue
        reads_env = func.attr == "getenv" or (
            func.attr == "get"
            and isinstance(func.value, ast.Attribute)
            and func.value.attr == "environ"
        )
        if not reads_env:
            continue
        arg = node.args[0]
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            found.add(arg.value)
        elif isinstance(arg, ast.Name) and arg.id in constants:
            found.add(constants[arg.id])

    return {name for name in found if ENV_NAME_RE.fullmatch(name)}


def _known_at(name, rev):
    """True if `name` appears anywhere in the tree at `rev`."""
    result = subprocess.run(
        ["git", "grep", "-q", "--fixed-strings", name, rev],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def new_env_vars(previous_tag, tag):
    """Environment variables this release introduced.

    Only the files this release touched can have introduced one, so those are
    the only ones parsed. Candidates are then confirmed against the previous
    tag as a whole, so a setting merely *moved* into a changed file is not
    mistaken for a new one.
    """
    if not previous_tag:
        return set()

    changed = [
        path
        for path in git(
            ["diff", "--name-only", f"{previous_tag}..{tag}"], cwd=REPO_ROOT
        ).split()
        if path.endswith(".py") and not path.startswith("tests/")
    ]

    candidates = set()
    for path in changed:
        candidates |= _env_vars_in(_module_source(path, tag), path)
    candidates -= {
        name
        for name in candidates
        if name in IGNORED_ENV_VARS or name.startswith(IGNORED_ENV_PREFIXES)
    }
    return {name for name in candidates if not _known_at(name, previous_tag)}


def undocumented_on_site(site_repo, names):
    """Of `names`, the ones that appear nowhere in the site's source."""
    if not names:
        return []
    haystack = []
    for path in sorted((site_repo / SITE_SOURCE_DIR).rglob("*")):
        if path.is_file() and path.suffix in SITE_TEXT_SUFFIXES:
            haystack.append(path.read_text(encoding="utf-8", errors="ignore"))
    corpus = "\n".join(haystack)
    return sorted(name for name in names if name not in corpus)


# --- Reporting --------------------------------------------------------------


def _section(title, lines, empty):
    body = "\n".join(f"- {line}" for line in lines) if lines else f"- {empty}"
    return f"## {title}\n\n{body}\n"


def render_report(result):
    """Renders the sync result as the markdown left behind in dist/."""
    pin = result["version_pin"]
    if not pin["changed"]:
        pin_line = f"already pinned to {pin['release']} ({pin['synced_at']})"
    elif pin["written"]:
        pin_line = (
            f"updated {pin['previous_release']} → {pin['release']}, "
            f"synced {pin['previous_synced_at']} → {pin['synced_at']}"
        )
    else:
        pin_line = (
            f"would update {pin['previous_release']} → {pin['release']} "
            f"(check mode, nothing written)"
        )

    parts = [
        f"# Site docs sync — {result['tag']}\n",
        f"Site repo: `{result['site_repo']}`  ",
        f"Compared: `{result['previous_tag'] or 'n/a'}` → `{result['tag']}`\n",
        _section("Version pin", [f"`{pin['file']}`: {pin_line}"], ""),
        _section(
            "Documented modules this release touched",
            [
                f"`{source}` → review `/{slug}`"
                for slug, source in result["changed_modules"]
            ],
            "none — no documented tool module changed",
        ),
        _section(
            "New in this release, not yet on the site",
            result["new_to_document"],
            "none — everything this release added is already documented",
        ),
        _section(
            "Pages that contradict the code",
            result["stale_docs"],
            "none — no documented tool or parameter disagrees with the code",
        ),
        _section(
            "Environment variables new in this release",
            [
                f"`{name}` is not mentioned anywhere on the site"
                for name in result["undocumented_env_vars"]
            ]
            or [
                f"`{name}` (already documented)"
                for name in sorted(result["new_env_vars"])
            ],
            "none — this release added no environment variables",
        ),
        "\n_Nothing above is staged or committed; the site repo is left dirty for review._\n",
    ]
    return "\n".join(parts)


def sync(tag, previous_tag=None, site_repo=None, synced_at=None, write=True):
    """Runs the whole sync and returns a result dict."""
    repo = resolve_site_repo(site_repo)
    if repo is None:
        raise RuntimeError(
            "could not find the site repo — pass --site-repo or set "
            f"{SITE_REPO_ENV} (looked for {VERSION_TS} under {DEFAULT_SITE_REPO})"
        )

    # Check the revisions before touching anything, so a typo cannot leave the
    # version pin rewritten by a run that then falls over.
    for rev in (tag, previous_tag):
        if rev and not git(
            ["rev-parse", "--verify", f"{rev}^{{commit}}"], cwd=REPO_ROOT, check=False
        ):
            raise RuntimeError(f"`{rev}` is not a revision in {REPO_ROOT}")

    previous_tag = previous_tag or resolve_previous_tag(tag)
    # Local date, not UTC: this is the "we checked the docs on" label a human
    # reads next to the release, and a release cut in the evening should not be
    # stamped with tomorrow.
    synced_at = synced_at or datetime.now().strftime("%Y-%m-%d")
    services = site_tools(repo / TOOLS_TS)
    introduced = new_env_vars(previous_tag, tag)
    new_to_document, stale_docs = tool_drift(services, tag, previous_tag)

    return {
        "tag": tag,
        "previous_tag": previous_tag,
        "site_repo": str(repo),
        "version_pin": update_version_pin(repo, tag, synced_at, write=write),
        "changed_modules": changed_tool_modules(services, previous_tag, tag),
        "new_to_document": new_to_document,
        "stale_docs": stale_docs,
        "new_env_vars": sorted(introduced),
        "undocumented_env_vars": undocumented_on_site(repo, introduced),
    }


def needs_review(result):
    """True when a human has to touch the site before the docs are honest again."""
    return bool(
        result["new_to_document"]
        or result["stale_docs"]
        or result["undocumented_env_vars"]
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Sync the workspacemcp.com docs with a google_workspace_mcp release"
    )
    parser.add_argument(
        "--tag", required=True, help="Release tag being documented, e.g. v1.24.0"
    )
    parser.add_argument(
        "--previous-tag", help="Tag to diff against (default: the prior tag)"
    )
    parser.add_argument(
        "--site-repo",
        help=f"Path to the site checkout (default: ${SITE_REPO_ENV} or {DEFAULT_SITE_REPO})",
    )
    parser.add_argument("--synced-at", help="ISO date to record (default: today)")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report drift without editing the version pin",
    )
    parser.add_argument(
        "--json", dest="as_json", action="store_true", help="Emit the result as JSON"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        result = sync(
            args.tag,
            previous_tag=args.previous_tag,
            site_repo=args.site_repo,
            synced_at=args.synced_at,
            write=not args.check,
        )
    except RuntimeError as error:
        print(f"❌ {error}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2) if args.as_json else render_report(result))
    return 1 if args.check and needs_review(result) else 0


if __name__ == "__main__":
    sys.exit(main())
