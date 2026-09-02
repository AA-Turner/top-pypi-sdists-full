"""Workspace onboarding resolver (auth P4, PF-350, §5.2/§5.5).

The **server half** of onboarding: given an org alias (+ optional project alias)
it resolves the InnoDay org/project and discovers the repos to clone, using the
DB + a GitHub token. The client half — the actual `git clone`/`pull` and writing
`.innoday/project.yml` — lives in `src/cli/commands/workspace.py` (the CLI has
no DB access), and is invoked by `innoday init`/`join`/`refresh` and the MCP
`setup_project_workspace` tool. Both go through the `/api/v1/onboarding/resolve`
endpoint (`src/routers/onboarding.py`), which is this service's only caller.

This service does NOT pick or switch orgs interactively — the aliases name
exactly what to set up (design principle: cwd/alias only).
"""

import os
from typing import Any, List, Optional, Sequence, Union

from sqlalchemy import func
from sqlmodel import Session, select

from src.api.github_api import GitHubAPI, GitHubAPIError
from src.domain.organization import Organization
from src.domain.project import Project, ProjectRepository
from src.domain.project_timeline import ProjectTimeline
from src.domain.repository import Repository
from src.services.org_credential_service import get_github_credentials

#: How many timeline entries a refresh snapshots into the workspace. Enough to
#: read "what has been happening here" at a glance without turning
#: `.innoday/timeline.md` into a file nobody scrolls to the end of.
TIMELINE_SNAPSHOT_LIMIT = 20
#: Hard ceiling for a caller-supplied limit, so this stays a snapshot.
TIMELINE_SNAPSHOT_MAX = 100


class WorkspaceOnboardError(Exception):
    pass


class WorkspaceCredentialMissingError(WorkspaceOnboardError):
    """No GitHub credential is stored for this org — a 400, not a 502.

    Distinct from its parent so the router can tell "this tenant is not
    configured" (the caller must connect GitHub) from "GitHub rejected the
    credential we do have" (an upstream failure). Both used to surface as 502,
    which sent the reader looking for a GitHub outage.
    """


class WorkspaceOnboardService:
    """Resolve an org/project by alias and discover its GitHub repos."""

    def __init__(self, session: Session, github_token: Optional[str] = None):
        """``github_token`` is an explicit, caller-supplied override.

        It stays **optional and defaulted to None**: `github_connect_service`
        constructs this service single-arg (twice) purely to reach `github_org()`
        / `github_topics()`, which need no token at all. Making it required would
        break #550's project-aware org resolution, whose failure mode is mass
        deactivation of a client's repos.

        There is deliberately **no `os.getenv("GITHUB_TOKEN")` fallback** (#554):
        that is the operator's credential, shared by every tenant in the process,
        so falling back to it means an unconfigured org silently discovers repos
        against a GitHub account it was never granted. `discover_repos` resolves
        the org's own Vault credential instead.
        """
        self.session = session
        self.github_token = github_token

    def resolve_org(self, org_alias: str) -> Organization:
        # Aliases are case-insensitive identifiers: users type `hs/pf` while a
        # stored alias may be `HS`/`PF`. An exact match made a correct alias
        # resolve as "not found" purely on casing.
        org = self.session.exec(
            select(Organization).where(
                func.lower(Organization.alias) == org_alias.lower()
            )
        ).first()
        if not org:
            raise WorkspaceOnboardError(
                f"Organization '{org_alias}' not found in InnoDay"
            )
        return org

    def resolve_project(
        self, org_id: str, project_alias: Optional[str]
    ) -> Optional[Project]:
        query = select(Project).where(Project.organization_id == org_id)
        if project_alias:
            # Case-insensitive for the same reason as resolve_org above.
            query = query.where(func.lower(Project.alias) == project_alias.lower())
        projects = self.session.exec(query).all()
        if project_alias:
            if not projects:
                raise WorkspaceOnboardError(
                    f"Project '{project_alias}' not found in org"
                )
            return projects[0]
        # No alias given: the org's default/only project, if exactly one.
        return projects[0] if len(projects) == 1 else None

    @staticmethod
    def _project_setting(mapping: Optional[dict], project: Optional[Project]) -> Any:
        """A per-project entry from a settings map, tolerating key casing.

        Both `settings['github_topics']` and `settings['github_orgs']` are keyed
        by project alias. Aliases are stored UPPERCASE because they double as the
        ticket prefix (`PF-412`), but these maps are hand-edited, so a lowercase
        key is a likely typo rather than a different project.
        """
        if project is None or not mapping:
            return None
        alias = project.alias or ""
        if alias in mapping:
            return mapping[alias]
        return next(
            (
                v
                for k, v in mapping.items()
                if isinstance(k, str) and k.lower() == alias.lower()
            ),
            None,
        )

    def github_org(self, org: Organization, project: Optional[Project]) -> str:
        """The GitHub org login to search for this project's repos.

        Resolution: a per-project `settings['github_orgs']` entry, then the
        org-wide `settings['github_org']`, then the last-resort fallbacks.

        The per-project override exists because **the InnoDay org that owns a
        project and the GitHub org that hosts its repos are independent**. `bp`
        owns BPCL, whose repos are under `BrightPowerSoftware`, and BPAI, whose
        repos stayed under `havilandsoftware` when the project moved orgs. A
        single org-wide value cannot describe both, and setting it to either one
        silently sends the other project's discovery to the wrong GitHub account
        — where it finds nothing rather than failing.

        Unlike `github_topics`, an override **replaces** rather than extends: a
        repo lives in exactly one GitHub org, so there is nothing to union.

        The remaining fallbacks are deliberately last-resort: a process-wide
        `GITHUB_ORG` env var is shared by every tenant (so it silently points one
        org's discovery at another's GitHub account), and the org alias is only
        ever right by coincidence — `atomic`'s repos live under `atomicpe`,
        `mb`'s under `MovementBase`. Set `settings.github_org` per org; the
        fallbacks exist so an unconfigured org degrades to "finds nothing"
        rather than crashing.
        """
        settings = org.settings or {}
        override = self._project_setting(settings.get("github_orgs"), project)
        if isinstance(override, str) and override.strip():
            return override.strip()
        return settings.get("github_org") or os.getenv("GITHUB_ORG") or org.alias

    def github_topic(
        self, org: Organization, project: Optional[Project]
    ) -> Optional[str]:
        """The project's topics as one comma-separated string, or None.

        Kept for the API response shape and any single-topic caller;
        `github_topics()` is the real accessor. See it for why the value is
        lowercased (GitHub topics are lowercase; aliases are stored UPPERCASE
        because they double as the ticket prefix, e.g. `PF-412`) and why a
        project may carry more than one topic.
        """
        topics = self.github_topics(org, project)
        return ",".join(topics) if topics else None

    def github_topics(self, org: Organization, project: Optional[Project]) -> List[str]:
        """Every GitHub topic whose repos belong to this project, lowercased.

        The project's own alias (lowercased — GitHub topics always are, while
        aliases are stored uppercase as the ticket prefix) is ALWAYS included,
        with any configured `settings['github_topics']` entries added to it. The
        override extends the set rather than replacing it, so a repo tagged with
        just the alias is still found once an override is added for the project.

        A project may legitimately span several topics (bp's BPAI repos carry
        both `bp-ai` and `brightpower`), so the override value is a
        comma-separated list and a repo matching ANY entry belongs. Returns []
        when there is no project.
        """
        if project is None:
            return []
        settings = org.settings or {}
        alias = project.alias or ""
        override = self._project_setting(settings.get("github_topics"), project)
        # Alias first, then the configured extras. Order is preserved and
        # blanks/dupes from a hand-edited settings string are dropped.
        seen: set = set()
        topics: List[str] = []
        for part in [alias, *str(override or "").split(",")]:
            t = part.strip().lower()
            if t and t not in seen:
                seen.add(t)
                topics.append(t)
        return topics

    async def discover_repos(
        self, org: Organization, github_org: str, topic: Union[str, Sequence[str]]
    ) -> List[dict]:
        """Every non-archived repo in ``github_org`` tagged with ANY of ``topic``.

        Accepts a single topic, a comma-separated string, or a sequence — a
        project can span several topics (bp's BPAI repos carry `bp-ai` AND
        `brightpower`), and a repo matching any one of them belongs to it.

        ``org`` is the InnoDay org whose credential authorises the lookup, and is
        required positionally so a caller cannot reach GitHub without naming the
        tenant it is acting for. Note it is a *separate* argument from
        ``github_org``: the two are independent (`bp` owns projects hosted under
        both `BrightPowerSoftware` and `havilandsoftware`).
        """
        token = self.github_token
        if not token:
            creds = get_github_credentials(self.session, org.id)
            token = (creds or {}).get("token")
        if not token:
            raise WorkspaceCredentialMissingError(
                f"No GitHub credential stored for organization "
                f"'{org.alias or org.id}'. Connect GitHub for this organization "
                f"(the token is stored in Vault) before discovering repositories."
            )
        api = GitHubAPI(token=token)
        all_repos: List[dict] = []
        page = 1
        while True:
            try:
                batch = await api.get_organization_repositories(
                    github_org, page=page, per_page=100
                )
            except GitHubAPIError as exc:
                # Translate into the error type the routers already handle, so a
                # rejected credential returns an actionable 502 instead of an
                # opaque 500 that reads like an InnoDay bug.
                if exc.is_auth_error:
                    # Names the org's stored GitHub credential, not GITHUB_TOKEN:
                    # since #554 that env var is not what authenticates here, so
                    # "rotate it and redeploy" sent the reader to the wrong place.
                    raise WorkspaceOnboardError(
                        f"GitHub rejected this organization's stored GitHub "
                        f"credential (HTTP {exc.status_code}) for GitHub org "
                        f"'{github_org}'. The token is expired, revoked, or missing "
                        f"the `repo`/`read:org` scope — reconnect GitHub for this "
                        f"organization to store a fresh one."
                    ) from exc
                raise WorkspaceOnboardError(str(exc)) from exc
            if not batch:
                break
            all_repos.extend(batch)
            if len(batch) < 100:
                break
            page += 1

        # Case-insensitive on both sides: GitHub normalises topics to lowercase,
        # but don't let an unexpected casing on either side silently drop a repo.
        parts = [topic] if isinstance(topic, str) else list(topic or [])
        wanted = {
            t.strip().lower()
            for part in parts
            for t in str(part).split(",")
            if t.strip()
        }
        return [
            r
            for r in all_repos
            if not r.get("archived")
            and not r.get("disabled")
            and wanted & {str(t).lower() for t in (r.get("topics") or [])}
        ]

    # -- refresh-time state the CLI cannot compute for itself -----------------
    #
    # `innoday refresh` is meant to be safe to run repeatedly and unattended,
    # which means it must never infer a destructive fact from the absence of
    # data. The three helpers below all exist so the client is *told* things
    # rather than deducing them from a diff.

    def removed_repos(self, project: Optional[Project]) -> List[dict]:
        """Repos this project has explicitly LOST, newest removal first.

        This is the only sanctioned basis for archiving a repo directory. The
        CLI used to archive anything present in its local `project.yml` but
        absent from a resolve response, which conflates "the label was removed"
        with "this particular lookup came back short" -- and the second is a
        transient GitHub failure, not a decision anyone made.

        `ProjectRepository.is_active` is maintained by
        `GitHubConnectService.sync_project_repositories`, which sets it False
        only when a sync positively observes a repo no longer carrying the
        project's topic label. That is a recorded event with a timestamp, so a
        client acting on it is acting on something that actually happened.
        """
        if not project:
            return []
        rows = self.session.exec(
            select(ProjectRepository, Repository)
            .join(Repository, Repository.id == ProjectRepository.repository_id)
            .where(
                ProjectRepository.project_id == project.id,
                ProjectRepository.is_active == False,  # noqa: E712
            )
        ).all()
        out = [
            {
                "name": repo.name,
                "removed_at": (
                    link.removed_at.isoformat() if link.removed_at else None
                ),
            }
            for link, repo in rows
            if repo and repo.name
        ]
        # Newest removal first, with unknown times last -- those predate the
        # column and carry no ordering information. Partitioned rather than
        # sorted with a single key, because `reverse=True` on a composite key
        # would also flip the None group to the front, which is the opposite of
        # what is wanted.
        dated = sorted(
            (r for r in out if r["removed_at"]),
            key=lambda r: r["removed_at"],
            reverse=True,
        )
        undated = [r for r in out if not r["removed_at"]]
        return dated + undated

    def recent_timeline(
        self, project: Optional[Project], limit: int = TIMELINE_SNAPSHOT_LIMIT
    ) -> List[dict]:
        """The project's most recent timeline entries, newest first.

        Returned inline with the resolve response so a refresh is one round
        trip rather than two, and so a workspace carries a readable history
        offline. Deliberately capped: this is a snapshot for context, not a
        replacement for `innoday timeline`, which paginates the full feed.
        """
        if not project:
            return []
        rows = self.session.exec(
            select(ProjectTimeline)
            .where(ProjectTimeline.project_id == project.id)
            .order_by(ProjectTimeline.occurred_at.desc(), ProjectTimeline.id.desc())
            .limit(max(1, min(limit, TIMELINE_SNAPSHOT_MAX)))
        ).all()
        return [
            {
                "event_type": (
                    e.event_type.value
                    if hasattr(e.event_type, "value")
                    else str(e.event_type)
                ),
                "title": e.title,
                "summary": e.summary,
                "occurred_at": e.occurred_at.isoformat() if e.occurred_at else None,
                "created_by": e.created_by,
            }
            for e in rows
        ]

    def store_context(
        self,
        project: Project,
        *,
        project_context: Optional[str],
        template_version: Optional[int],
        additional_context: Optional[str],
    ) -> dict:
        """Persist a refresh's context back onto the project.

        Two fields, two different rules:

        * ``project_context`` is generated output, so the only question is
          which generation is newer. A client running an older template must
          not overwrite a newer one -- otherwise whichever machine refreshed
          most recently would win, and the UI would flip between generations
          depending on who ran `refresh` last. Equal versions do overwrite:
          same template, so the content is a re-render, and accepting it keeps
          a project whose repos changed from showing a stale repo list.
        * ``additional_context`` is hand-written, so it is stored as given.
          The union with whatever the server already held is computed on the
          CLIENT (it is the side that also holds the local file, and doing it
          in one place keeps one definition of the merge). Passing None means
          "I have nothing to say about this field" and leaves it untouched --
          distinct from passing "", which is a deliberate clear.
        """
        stored_version = project.project_context_version
        context_written = False
        if project_context is not None and template_version is not None:
            if stored_version is None or template_version >= stored_version:
                project.project_context = project_context
                project.project_context_version = template_version
                context_written = True

        if additional_context is not None:
            project.additional_context = additional_context

        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        return {
            "project_context_written": context_written,
            "project_context_version": project.project_context_version,
            "additional_context_stored": additional_context is not None,
        }
