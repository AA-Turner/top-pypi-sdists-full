import warnings

warnings.warn(
    "\n\n"
    "┌─────────────────────────────────────────────────────────────────┐\n"
    "│                      PACKAGE DEPRECATED                        │\n"
    "│                                                                 │\n"
    "│  'arcade-ai' has been renamed to 'arcade-mcp'.                 │\n"
    "│                                                                 │\n"
    "│  Migrate using whichever tool you used to install:             │\n"
    "│                                                                 │\n"
    "│  pip:                                                           │\n"
    "│    pip uninstall arcade-ai && pip install arcade-mcp           │\n"
    "│                                                                 │\n"
    "│  uv (global tool):                                              │\n"
    "│    uv tool uninstall arcade-ai && uv tool install arcade-mcp   │\n"
    "│                                                                 │\n"
    "│  uv (project dependency):                                       │\n"
    "│    uv remove arcade-ai && uv add arcade-mcp                    │\n"
    "│                                                                 │\n"
    "│  Docs: https://docs.arcade.dev                                  │\n"
    "└─────────────────────────────────────────────────────────────────┘\n",
    DeprecationWarning,
    stacklevel=2,
)
