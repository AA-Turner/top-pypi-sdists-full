"""Auto-update engine for model discovery and version tracking.

Maintains a sources.json of tracked GitHub repositories.
Periodically checks for new releases, compares against the local
registry (by version tag + SHA256), and downloads only new versions.
"""

import fnmatch
import json
import logging
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from .config import settings
from .github_client import (
    discover_model_assets,
    extract_version_number,
    parse_repo_url,
)
from .model_registry import ModelRegistry
from .schemas import DownloadModelReq

logger = logging.getLogger("ai-platform.updater")


@dataclass
class TrackedSource:
    model_id: str
    owner: str
    repo: str
    runtime: str = "llama_cpp"
    asset_pattern: str = "*.gguf"  # glob pattern to filter assets
    license: str | None = None
    last_checked: str | None = None
    auto_update: bool = True


@dataclass
class UpdateResult:
    model_id: str
    new_versions: list[str] = field(default_factory=list)
    skipped_duplicate: int = 0
    skipped_existing: int = 0
    errors: list[str] = field(default_factory=list)


class AutoUpdater:
    def __init__(self, registry: ModelRegistry) -> None:
        self.registry = registry
        self.sources_path = settings.config_dir / "sources.json"
        if not self.sources_path.exists():
            self.sources_path.write_text("[]", encoding="utf-8")

    # ── Source management ──────────────────────────────────────

    def list_sources(self) -> list[TrackedSource]:
        try:
            raw = json.loads(self.sources_path.read_text(encoding="utf-8"))
            return [TrackedSource(**s) for s in raw]
        except (json.JSONDecodeError, TypeError) as e:
            logger.error("Corrupt sources.json, resetting: %s", e)
            self.sources_path.write_text("[]", encoding="utf-8")
            return []

    def add_source(
        self,
        repo_url: str,
        model_id: str,
        runtime: str = "llama_cpp",
        asset_pattern: str = "*.gguf",
        license: str | None = None,
    ) -> TrackedSource:
        owner, repo = parse_repo_url(repo_url)

        sources = self.list_sources()
        for s in sources:
            if s.model_id == model_id:
                raise ValueError(f"Source already tracked: {model_id}")

        source = TrackedSource(
            model_id=model_id,
            owner=owner,
            repo=repo,
            runtime=runtime,
            asset_pattern=asset_pattern,
            license=license,
        )
        sources.append(source)
        self._save_sources(sources)
        logger.info("Added source: %s/%s -> %s", owner, repo, model_id)
        return source

    def remove_source(self, model_id: str) -> None:
        sources = self.list_sources()
        sources = [s for s in sources if s.model_id != model_id]
        self._save_sources(sources)
        logger.info("Removed source: %s", model_id)

    # ── Update checking ───────────────────────────────────────

    def check_updates(self, model_id: str | None = None) -> list[UpdateResult]:
        """Check one or all tracked sources for new releases."""
        sources = self.list_sources()
        if model_id:
            sources = [s for s in sources if s.model_id == model_id]
            if not sources:
                raise KeyError(f"No tracked source: {model_id}")

        results = []
        for source in sources:
            if not source.auto_update and model_id is None:
                continue
            result = self._check_source(source)
            results.append(result)

        # Update last_checked timestamps
        all_sources = self.list_sources()
        checked_ids = {r.model_id for r in results}
        for s in all_sources:
            if s.model_id in checked_ids:
                s.last_checked = datetime.now(timezone.utc).isoformat()
        self._save_sources(all_sources)

        return results

    def _check_source(self, source: TrackedSource) -> UpdateResult:
        result = UpdateResult(model_id=source.model_id)

        try:
            assets = discover_model_assets(source.owner, source.repo)
        except Exception as exc:
            result.errors.append(f"Failed to query GitHub: {exc}")
            return result

        # Filter by asset pattern
        matching = [
            a for a in assets
            if fnmatch.fnmatch(a["asset_name"].lower(), source.asset_pattern.lower())
        ]

        if not matching:
            logger.info("No matching assets for %s (pattern: %s)", source.model_id, source.asset_pattern)
            return result

        # Get existing version tags and hashes for deduplication
        existing_tags = set()
        existing_hashes = set()
        try:
            record = self.registry.get_model(source.model_id)
            for v in record.versions:
                if v.source_url:
                    existing_tags.add(self._tag_from_url_or_version(v))
                if v.sha256:
                    existing_hashes.add(v.sha256.lower())
        except KeyError:
            pass  # Model not yet registered

        for asset in matching:
            tag = asset["tag"]
            normalized_tag = extract_version_number(tag)

            # Dedup by version tag
            if tag in existing_tags or normalized_tag in existing_tags:
                result.skipped_existing += 1
                logger.debug("Skipping existing tag %s for %s", tag, source.model_id)
                continue

            # Download and register
            try:
                req = DownloadModelReq(
                    model_id=source.model_id,
                    source_url=asset["download_url"],
                    runtime=source.runtime,
                    filename=asset["asset_name"],
                    license=source.license,
                    format=asset.get("format"),
                )
                record = self.registry.download_and_register(req)

                # Check SHA256 dedup after download
                latest = record.active()
                if latest.sha256 and latest.sha256.lower() in existing_hashes:
                    result.skipped_duplicate += 1
                    logger.info(
                        "Downloaded %s tag %s but SHA256 matches existing version (kept as new version entry)",
                        source.model_id,
                        tag,
                    )
                else:
                    existing_hashes.add(latest.sha256.lower() if latest.sha256 else "")

                existing_tags.add(tag)
                existing_tags.add(normalized_tag)
                result.new_versions.append(tag)
                logger.info("Downloaded new version %s for %s", tag, source.model_id)
            except Exception as exc:
                result.errors.append(f"Failed to download {tag}: {exc}")
                logger.error("Download failed for %s %s: %s", source.model_id, tag, exc)

        return result

    # ── Helpers ────────────────────────────────────────────────

    def _tag_from_url_or_version(self, version) -> str:
        """Extract a tag-like identifier from a version."""
        if version.source_url and "/releases/download/" in version.source_url:
            parts = version.source_url.split("/releases/download/")
            if len(parts) > 1:
                return parts[1].split("/")[0]
        return f"v{version.version}"

    def _save_sources(self, sources: list[TrackedSource]) -> None:
        data = [asdict(s) for s in sources]
        self.sources_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
