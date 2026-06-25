import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# ---------------------------------------------------------------------------
# Optional, feature-specific dependencies.
#
# As of the lazy-import refactor, all of the heavy / non-core third-party
# packages are imported lazily by abstract_utilities. The core package installs
# and imports with **no** third-party requirements; install the extra(s) below
# only for the features you actually use, e.g.:
#
#     pip install abstract_utilities[pdf]
#     pip install abstract_utilities[data,web]
#     pip install abstract_utilities[all]
# ---------------------------------------------------------------------------
extras_require = {
    # PDF reading / writing + OCR fallback
    "pdf": ["PyPDF2", "pdfplumber", "pdf2image", "pytesseract"],
    # tabular / geospatial data + spreadsheet readers
    "data": ["pandas", "geopandas", "openpyxl", "ezodf"],
    # flask helpers + werkzeug uploads + HTTP
    "web": ["flask", "werkzeug", "requests"],
    # tiktoken-based token counting (parse_utils)
    "tokens": ["tiktoken"],
    # interactive / remote command execution (ssh_utils)
    "ssh": ["pexpect>=4.8.0"],
    # .env loading (env_utils)
    "env": ["python-dotenv"],
    # yt-dlp helpers (imports/utils, not loaded by the core import chain)
    "ytdlp": ["yt_dlp>=2023.10.13"],
}
extras_require["all"] = sorted({pkg for group in extras_require.values() for pkg in group})

setuptools.setup(
    name="abstract_utilities",
    version='0.2.2.784',
    author="putkoff",
    author_email="partners@abstractendeavors.com",
    description="Utility modules for data comparison, JSON handling, string manipulation, math operations, and general automation tasks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AbstractEndeavors/abstract_utilities",

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],

    python_requires=">=3.10",

    # Core install pulls in no third-party packages: every heavy dependency is
    # imported lazily and is declared as an optional extra above.
    install_requires=[],
    extras_require=extras_require,

    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)
