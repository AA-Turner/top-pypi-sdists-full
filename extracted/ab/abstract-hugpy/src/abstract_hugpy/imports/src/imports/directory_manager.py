import os
from pathlib import Path
from abstract_utilities import get_env_value
import itertools

# ────────────────────────────────────────────────────────────────────────────────
# DEFAULT ROOTS
# ────────────────────────────────────────────────────────────────────────────────

DEFAULT_DATA_ROOTS = [
    "/mnt/24T/media",
    "/var/www/media"
]

FALLBACK_DATA_DIRECTORY = f"{DEFAULT_DATA_ROOTS[0]}/DATA"

# ────────────────────────────────────────────────────────────────────────────────
# ENV → DIRECTORIES MAPPING
# ────────────────────────────────────────────────────────────────────────────────

DIR_ENV_KEYS = {
    "media":     "MEDIA_ROOT_DIRECTORY",
    "data":      "DATA_ROOT_DIRECTORY",
    "videos":    "VIDEOS_ROOT_DIRECTORY",
    "documents": "DOCUMENTS_ROOT_DIRECTORY",
    "downloads": "DOWNLOADS_ROOT_DIRECTORY",
    "uploads":   "UPLOADS_ROOT_DIRECTORY",
    "images":    "IMAGES_ROOT_DIRECTORY",
}

# ────────────────────────────────────────────────────────────────────────────────
# LOADER
# ────────────────────────────────────────────────────────────────────────────────

def resolve_directory(env_key: str, fallback: str | None = None) -> str:
    """
    Load directory path from environment; fallback if missing.
    """
    value = get_env_value(env_key) or fallback
    if not value:
        raise RuntimeError(f"Environment variable {env_key} is missing and no fallback provided.")
    return str(Path(value).resolve())


# ────────────────────────────────────────────────────────────────────────────────
# LOAD REAL DIRECTORIES
# ────────────────────────────────────────────────────────────────────────────────

MEDIA_DIRECTORY = resolve_directory(
    "MEDIA_ROOT_DIRECTORY",
    fallback="/var/www/media"
)

DATA_DIRECTORY = resolve_directory(
    "DATA_ROOT_DIRECTORY",
    fallback=FALLBACK_DATA_DIRECTORY
)

VIDEOS_DIRECTORY     = resolve_directory("VIDEOS_ROOT_DIRECTORY",     f"{DATA_DIRECTORY}/videos")
DOCUMENTS_DIRECTORY  = resolve_directory("DOCUMENTS_ROOT_DIRECTORY",  f"{DATA_DIRECTORY}/documents")
DOWNLOADS_DIRECTORY  = resolve_directory("DOWNLOADS_ROOT_DIRECTORY",  f"{DATA_DIRECTORY}/downloads")
UPLOADS_DIRECTORY    = resolve_directory("UPLOADS_ROOT_DIRECTORY",    f"{DATA_DIRECTORY}/uploads")
IMAGES_DIRECTORY     = resolve_directory("IMAGES_ROOT_DIRECTORY",     f"{DATA_DIRECTORY}/images")

DIRECTORIES = {
    "media": MEDIA_DIRECTORY,
    "data": DATA_DIRECTORY,
    "videos": VIDEOS_DIRECTORY,
    "documents": DOCUMENTS_DIRECTORY,
    "downloads": DOWNLOADS_DIRECTORY,
    "uploads": UPLOADS_DIRECTORY,
    "images": IMAGES_DIRECTORY,
}

# ────────────────────────────────────────────────────────────────────────────────
# ALIAS GENERATOR
# ────────────────────────────────────────────────────────────────────────────────

def generate_directory_aliases(base: str):
    """
    Produce all naming variants for a given directory base name.
    Returns canonical name + alias mapping.
    """
    base = base.lower().strip("/ ")

    plural = base if base.endswith("s") else base + "s"
    singular = base[:-1] if base.endswith("s") else base

    bases = {singular, plural}
    bases_upper = {b.upper() for b in bases}

    core_tokens = ["", "_ROOT", "_DIRECTORY", "_ROOT_DIR", "_ROOT_DIRECTORY"]
    default_tokens = ["", "_DEFAULT", "_DEFAULT_ROOT", "_ROOT_DEFAULT"]

    canonical = f"{plural.upper()}_DIR"
    aliases = {}

    for b in bases_upper:
        for core, default in itertools.product(core_tokens, default_tokens):
            name = f"{b}{core}{default}".strip("_")
            if name:
                aliases[name] = canonical

    aliases[plural.upper()] = canonical
    aliases[singular.upper()] = canonical

    return canonical, aliases


# ────────────────────────────────────────────────────────────────────────────────
# BUILD UNIVERSAL ALIAS REGISTRY
# ────────────────────────────────────────────────────────────────────────────────

ALIASES = {}


for name, real_path in DIRECTORIES.items():
    canonical, alias_map = generate_directory_aliases(name)

    # define the canonical variable
    globals()[canonical] = real_path

    # define *all alias variables* to point to the same value
    for alias, canon in alias_map.items():
        globals()[alias] = real_path   # ← THIS FIXES YOUR ERROR

    # store alias → canonical mapping for resolver
    ALIASES.update(alias_map)
# ────────────────────────────────────────────────────────────────────────────────
# UNIVERSAL RESOLVER
# ────────────────────────────────────────────────────────────────────────────────

def resolve_any_directory(key: str) -> str:
    """
    Given ANY directory alias (IMAGE_DIR, IMAGES_ROOT_DIRECTORY_DEFAULT, etc.),
    return the correct canonical path.
    """
    key = key.upper()

    if key not in ALIASES:
        raise KeyError(f"Unknown directory alias: {key}")

    canonical = ALIASES[key]
    return globals()[canonical]


# ────────────────────────────────────────────────────────────────────────────────
# DEBUG PRINT
# ────────────────────────────────────────────────────────────────────────────────

def print_directories():
    print("\n=== Loaded Directory Configuration ===")
    for key, val in DIRECTORIES.items():

        print(f"{key.upper():12} → {val}")
    print("======================================\n")

