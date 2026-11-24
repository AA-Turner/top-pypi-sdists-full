"""SystemPathRegistry — the single source of truth for where writers file their output.

Anything a writer files without the person picking a folder — AI generations,
scraper output, derived variants, thumbnails, ephemeral previews — MUST request
its folder path through this registry. Hand-crafted paths are forbidden: they
pollute user libraries, bypass retention policies, and make audit / cleanup
impossible.

AUDIENCE — every registered folder declares whose output it holds
(``SystemFolder.audience``, 2026-10-30):

    "system" (default) — machine output: derived, fetched or produced on the
                      platform's own initiative. MUST live under one of the
                      two system roots below, so the person never sees it in
                      the tree, the sync feed or Recents.
    "person"          — output the PERSON asked for: an image they generated
                      in a chat, speech they requested, a video, a document.
                      MUST live OUTSIDE the system roots (``Images/Generated``,
                      ``Audio/Generated``, …) so it appears in their Files tree
                      AND Recents (Arman 2026-10-30: "That's not an automated
                      thing the system is doing. That's the user generating an
                      image."). Guard: tests/test_person_output_is_the_persons.py.

Two system roots:

    generations/    — content the system *produced* on its own initiative
                      (automated pipelines). The person's own generations
                      no longer live here — they are "person" folders.

    system-files/   — content the system *derived* or *fetched* (variants
                      from a master, thumbnails, ephemeral previews,
                      scraper output, redaction renders, etc.). Provenance:
                      derived from or about other content.

Anything in cld_files NOT under these prefixes is user-owned. Quota /
retention / audit jobs use this split to apply the right policy.

Register a feature once at import time:

    from matrx_files import register_system_folder

    THUMBNAILS = register_system_folder(
        "thumbnails",
        root="system-files/thumbnails",
        description="Master-row thumbnail renders for the file browser preview.",
    )                                   # audience="system" by default

Use it everywhere afterward:

    path = AI_IMAGES.path(filename)     # a person folder
    # → "Images/Generated/sunset-over-mountains-1747266537.jpg"

Or by name (when the registration site is upstream):

    AI_IMAGES = get_system_folder("ai_images")
    path = AI_IMAGES.path(*segments)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Literal

_ALLOWED_ROOTS: Final[tuple[str, ...]] = ("generations", "system-files")

#: Whose output a registered folder holds — see the module docstring.
FolderAudience = Literal["system", "person"]
_AUDIENCES: Final[tuple[str, ...]] = ("system", "person")


@dataclass(frozen=True)
class SystemFolder:
    """A registered system-managed folder.

    Construct only through ``register_system_folder``. ``root`` is the
    folder prefix under which every path this folder produces lives.
    ``audience`` says whose output it holds: ``"system"`` folders are
    enforced to start with one of the canonical system roots (hidden from
    the person); ``"person"`` folders are enforced to start OUTSIDE them
    (visible in the person's tree and Recents).
    """

    name: str
    root: str
    description: str
    audience: FolderAudience = "system"

    def path(self, *segments: str) -> str:
        """Join the segments under this folder's root.

        Empty / None / `/`-only segments are skipped. The result is a
        forward-slash logical path with no leading slash — exactly the
        shape ``FileService.write`` / ``managed_write_async`` expect
        for the ``file_path`` argument.
        """
        parts: list[str] = [self.root]
        for seg in segments:
            if not seg:
                continue
            cleaned = seg.strip("/").strip()
            if not cleaned:
                continue
            parts.append(cleaned)
        return "/".join(parts)


class SystemPathRegistry:
    """Process-wide registry of named system folders.

    Use the module-level :func:`register_system_folder` /
    :func:`get_system_folder` / :func:`list_system_folders` wrappers
    rather than the class methods directly — the wrappers carry the
    type annotations FE / tooling pick up.
    """

    _features: dict[str, SystemFolder] = {}

    @classmethod
    def register(
        cls,
        name: str,
        *,
        root: str,
        description: str,
        audience: FolderAudience = "system",
    ) -> SystemFolder:
        if audience not in _AUDIENCES:
            raise ValueError(f"audience must be one of {_AUDIENCES!r}; got {audience!r}.")
        clean_root = root.strip("/").strip()
        head = clean_root.split("/", 1)[0]
        if audience == "system" and head not in _ALLOWED_ROOTS:
            raise ValueError(
                f"System folder root must start with one of "
                f"{_ALLOWED_ROOTS!r}; got {root!r}. Anything outside "
                f"those roots is the person's namespace — register it with "
                f"audience=\"person\" only if the person asked for this output."
            )
        if audience == "person" and head in _ALLOWED_ROOTS:
            raise ValueError(
                f"Person folder {name!r} cannot live under a system root "
                f"({root!r}): files there are hidden from the person's tree "
                f"and Recents, which is exactly what a person folder must not be."
            )
        existing = cls._features.get(name)
        if existing is not None and (existing.root, existing.audience) != (clean_root, audience):
            raise ValueError(
                f"System folder {name!r} already registered at "
                f"{existing.root!r} ({existing.audience}); cannot re-register at "
                f"{clean_root!r} ({audience}). Pick a unique name."
            )
        folder = SystemFolder(
            name=name, root=clean_root, description=description, audience=audience
        )
        cls._features[name] = folder
        return folder

    @classmethod
    def get(cls, name: str) -> SystemFolder:
        if name not in cls._features:
            known = ", ".join(sorted(cls._features)) or "(none registered)"
            raise KeyError(
                f"Unknown system folder {name!r}. Register it via "
                f"register_system_folder(...) at module import time, "
                f"or pick one of: {known}."
            )
        return cls._features[name]

    @classmethod
    def list_all(cls) -> list[SystemFolder]:
        return sorted(cls._features.values(), key=lambda f: f.root)

    @classmethod
    def is_system_path(cls, file_path: str) -> bool:
        """True iff ``file_path`` starts with one of the canonical roots."""
        if not file_path:
            return False
        head = file_path.lstrip("/").split("/", 1)[0]
        return head in _ALLOWED_ROOTS

    @classmethod
    def roots(cls) -> tuple[str, ...]:
        """The canonical system roots — for callers that filter system
        content out of user-facing listings at the query layer."""
        return _ALLOWED_ROOTS


def register_system_folder(
    name: str,
    *,
    root: str,
    description: str,
    audience: FolderAudience = "system",
) -> SystemFolder:
    """Module-level wrapper. Prefer this over the class method."""
    return SystemPathRegistry.register(
        name, root=root, description=description, audience=audience
    )


def get_system_folder(name: str) -> SystemFolder:
    """Look up a previously-registered folder by name."""
    return SystemPathRegistry.get(name)


def list_system_folders() -> list[SystemFolder]:
    return SystemPathRegistry.list_all()


def is_system_path(file_path: str) -> bool:
    """Whether ``file_path`` is under the system-managed roots.

    Used by retention / quota jobs to apply different policy to system
    files vs user uploads.
    """
    return SystemPathRegistry.is_system_path(file_path)


# ---------------------------------------------------------------------------
# Built-in registrations. Anything a writer files without the person picking a
# folder SHOULD live under one of these names. Hosts add their own product-specific
# registrations at import time.
# ---------------------------------------------------------------------------

# The person's own AI output — they asked for it, so it is THEIR file: in the
# Files tree, in Recents, never under a system root (Arman 2026-10-30).

AI_IMAGES = register_system_folder(
    "ai_images",
    root="Images/Generated",
    description="Images the person generated (DALL-E, gpt-image, Imagen, Grok, …) in a chat, "
    "an agent run or a tool they called.",
    audience="person",
)

AI_AUDIO = register_system_folder(
    "ai_audio",
    root="Audio/Generated",
    description="Speech, music and sound effects the person asked an AI to make (TTS, …).",
    audience="person",
)

AI_VIDEO = register_system_folder(
    "ai_video",
    root="Video/Generated",
    description="Videos the person generated (Veo, Sora, Replicate, …).",
    audience="person",
)

AI_DOCUMENTS = register_system_folder(
    "ai_documents",
    root="Documents/Generated",
    description="Documents the person asked an AI to produce (docx / pptx / xlsx / PDF).",
    audience="person",
)

REQUEST_SNAPSHOTS = register_system_folder(
    "request_snapshots",
    root="system-files/request-snapshots",
    description="Byte blobs captured from a paid request's snapshot (aidream "
    "services/request_snapshot_blobs.py) — audit evidence, never the person's document.",
)

VOICE_SAMPLES = register_system_folder(
    "voice_samples",
    root="system-files/voice-samples",
    description="Public voice-catalog preview clips synced from TTS providers "
    "(aidream scripts/sync_voices.py) — catalog presentation, never a person's audio.",
)

VARIANTS = register_system_folder(
    "variants",
    root="system-files/variants",
    description="Derived variants (resized thumbnails, format conversions, social-share crops).",
)

THUMBNAILS = register_system_folder(
    "thumbnails",
    root="system-files/thumbnails",
    description="Master-row thumbnail renders for the file browser preview.",
)

PREVIEWS = register_system_folder(
    "previews",
    root="system-files/previews",
    description="Ephemeral no-persist preview renders for the Image Studio.",
)

SCRAPER = register_system_folder(
    "scraper",
    root="system-files/scraper",
    description="Web-scraper output: HTML snapshots, screenshots, asset captures.",
)

BROWSER_CAPTURE = register_system_folder(
    "browser_capture",
    root="system-files/browser-captures",
    description=(
        "Cloud Browser page-state captures — the before/after screenshots that "
        "bracket an agent-directed login. Never public: a login page can hold a "
        "typed value, so these are owner-scoped and referenced only by file_id."
    ),
)

REDACTION = register_system_folder(
    "redaction",
    root="system-files/redaction",
    description="PII-redacted derivatives of master documents.",
)

ANALYSIS_RESULTS = register_system_folder(
    "analysis_results",
    root="system-files/analysis",
    description="Per-detector JSON payloads from the file-analysis pipeline.",
)

PAGE_RENDERS = register_system_folder(
    "page_renders",
    root="system-files/page-renders",
    description="Rasterized PDF page images at specific DPIs (for OCR / inline viewer).",
)

PDF_DERIVATIVES = register_system_folder(
    "pdf_derivatives",
    root="system-files/pdf-derivatives",
    description="System-derived PDFs: split, merged, compressed, redacted, etc.",
)

PDF_EXTRACTIONS = register_system_folder(
    "pdf_extractions",
    root="system-files/pdf-extractions",
    description="OCR + text-extraction outputs from PDFs.",
)

PDF_PAGE_PDFS = register_system_folder(
    "pdf_page_pdfs",
    root="system-files/pdf-page-pdfs",
    description="Single-page / page-range PDFs sliced from a source document, "
    "cached as cld_files derivatives and attached to agent calls (e.g. "
    "page-extraction's pdf_page source variation).",
)

OFFICE_PDFS = register_system_folder(
    "office_pdfs",
    root="system-files/office-pdfs",
    description="PDF conversions of Office masters (docx/pptx/xlsx), cached as "
    "files.files derivatives (derivation_kind='pdf_conversion') so decks and "
    "documents render visually through the canonical PDF machinery.",
)

AUDIO_EXTRACTS = register_system_folder(
    "audio_extracts",
    root="system-files/audio-extracts",
    description="Audio tracks demuxed/normalized from a parent video file, "
    "cached as files.files derivatives (derivation_kind='audio_extracted').",
)

TRANSCRIPT_RECORDINGS = register_system_folder(
    "transcript_recordings",
    root="system-files/transcripts",
    description="Audio / screen recordings captured by the Transcripts feature "
    "on the user's behalf. Owned by the user but managed through the "
    "Transcripts UI (looked up by cld_files id), never the file browser — so "
    "they live under the system namespace and stay out of the workspace tree "
    "and recents.",
)


__all__ = [
    "SystemFolder",
    "SystemPathRegistry",
    "register_system_folder",
    "get_system_folder",
    "list_system_folders",
    "is_system_path",
    "AI_IMAGES",
    "AI_AUDIO",
    "AI_VIDEO",
    "AI_DOCUMENTS",
    "REQUEST_SNAPSHOTS",
    "VOICE_SAMPLES",
    "FolderAudience",
    "VARIANTS",
    "THUMBNAILS",
    "PREVIEWS",
    "SCRAPER",
    "REDACTION",
    "BROWSER_CAPTURE",
    "ANALYSIS_RESULTS",
    "PAGE_RENDERS",
    "PDF_DERIVATIVES",
    "PDF_EXTRACTIONS",
    "PDF_PAGE_PDFS",
    "OFFICE_PDFS",
    "AUDIO_EXTRACTS",
    "TRANSCRIPT_RECORDINGS",
]
