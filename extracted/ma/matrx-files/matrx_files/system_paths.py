"""SystemPathRegistry — the single source of truth for system-managed paths.

Anything the system writes automatically — AI generations, scraper output,
derived variants, thumbnails, ephemeral previews — MUST request its
folder path through this registry. Hand-crafted paths under user-namespace
folders are forbidden: they pollute user libraries, bypass retention
policies, and make audit / cleanup impossible.

Two top-level roots:

    generations/    — content the system *produced* (LLM output, image
                      generation, TTS audio, video generation, etc.).
                      Provenance: model + prompt is in metadata; the
                      bytes did not exist before the system created them.

    system-files/   — content the system *derived* or *fetched* (variants
                      from a master, thumbnails, ephemeral previews,
                      scraper output, redaction renders, etc.). Provenance:
                      derived from or about other content.

Anything in cld_files NOT under these prefixes is user-owned. Quota /
retention / audit jobs use this split to apply the right policy.

Register a feature once at import time:

    from matrx_files import register_system_folder

    AI_IMAGES = register_system_folder(
        "ai_images",
        root="generations/images",
        description="LLM / diffusion image-generation outputs.",
    )

Use it everywhere afterward:

    path = AI_IMAGES.path(filename)
    # → "generations/images/sunset-over-mountains-1747266537.jpg"

Or by name (when the registration site is upstream):

    AI_IMAGES = get_system_folder("ai_images")
    path = AI_IMAGES.path(*segments)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

_ALLOWED_ROOTS: Final[tuple[str, ...]] = ("generations", "system-files")


@dataclass(frozen=True)
class SystemFolder:
    """A registered system-managed folder.

    Construct only through ``register_system_folder``. ``root`` is the
    folder prefix under which every path this folder produces lives —
    enforced to start with one of the canonical roots.
    """

    name: str
    root: str
    description: str

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
    ) -> SystemFolder:
        clean_root = root.strip("/").strip()
        head = clean_root.split("/", 1)[0]
        if head not in _ALLOWED_ROOTS:
            raise ValueError(
                f"System folder root must start with one of "
                f"{_ALLOWED_ROOTS!r}; got {root!r}. Anything outside "
                f"those roots is treated as a user-namespace path and "
                f"cannot register as system-managed."
            )
        if name in cls._features and cls._features[name].root != clean_root:
            raise ValueError(
                f"System folder {name!r} already registered at "
                f"{cls._features[name].root!r}; cannot re-register at "
                f"{clean_root!r}. Pick a unique name."
            )
        folder = SystemFolder(name=name, root=clean_root, description=description)
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
) -> SystemFolder:
    """Module-level wrapper. Prefer this over the class method."""
    return SystemPathRegistry.register(name, root=root, description=description)


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
# Built-in registrations. Anything the platform itself auto-saves SHOULD
# live under one of these names. Hosts add their own product-specific
# registrations at import time.
# ---------------------------------------------------------------------------

AI_IMAGES = register_system_folder(
    "ai_images",
    root="generations/images",
    description="LLM / diffusion image-generation outputs (DALL-E, gpt-image, Stable Diffusion, …).",
)

AI_AUDIO = register_system_folder(
    "ai_audio",
    root="generations/audio",
    description="TTS / speech-synthesis outputs.",
)

AI_VIDEO = register_system_folder(
    "ai_video",
    root="generations/video",
    description="Video-generation outputs (Replicate, Veo, Sora, …).",
)

AI_DOCUMENTS = register_system_folder(
    "ai_documents",
    root="generations/documents",
    description="AI-generated PDFs / Word docs / spreadsheets.",
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
