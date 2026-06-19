"""
Aigie SDK - Enterprise-grade AI agent reliability monitoring.

Installation:
    # Basic installation
    pip install aigie

    # With compression (recommended for production)
    pip install aigie[compression]

    # With all features
    pip install aigie[all]

    # LLM Provider integrations
    pip install aigie[openai]      # OpenAI wrapper
    pip install aigie[anthropic]   # Anthropic Claude
    pip install aigie[gemini]      # Google Gemini

    # Agent Framework integrations
    pip install aigie[langchain]   # LangChain integration
    pip install aigie[langgraph]   # LangGraph integration
    pip install aigie[claude-agent-sdk]  # Anthropic Claude Agent SDK

    # Vector DB integrations
    pip install aigie[pinecone]    # Pinecone
    pip install aigie[qdrant]      # Qdrant
    pip install aigie[chromadb]    # ChromaDB
    pip install aigie[weaviate]    # Weaviate
    pip install aigie[vectordbs]   # All vector DBs

    # Observability
    pip install aigie[opentelemetry]  # OpenTelemetry inbound (OTel → Aigie)
    pip install aigie[otlp]           # OTLP export (Aigie → OTel collectors)
"""

from pathlib import Path

from setuptools import find_packages, setup

# Customer-facing PyPI description (kept separate from the dev README so internal
# dev/build/publish docs are not published to PyPI). Falls back to README.md.
description_path = Path(__file__).parent / "DESCRIPTION.md"
readme_path = Path(__file__).parent / "README.md"
if description_path.exists():
    long_description = description_path.read_text()
elif readme_path.exists():
    long_description = readme_path.read_text()
else:
    long_description = __doc__

setup(
    name="aigie",
    version="0.2.46",
    description="Enterprise-grade AI agent reliability monitoring and autonomous remediation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Aigie",
    author_email="support@kytte.ai",
    url="https://kytte.ai/",
    license="Proprietary",
    package_dir={"": "sdk"},
    packages=find_packages(where="sdk", exclude=["tests", "tests.*", "examples", "examples.*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.10",
    keywords="ai agent monitoring observability llm reliability remediation",
    # Core dependencies (minimal for basic usage)
    install_requires=[
        "httpx>=0.25.0",  # Async HTTP client
        "websockets>=11.0",  # Gateway WebSocket connection
        "redis>=5.0.0",  # Redis intervention transport (auto-discovered at init)
        # Autonomous v2 control plane (gRPC bidi stream) — ADR 0001
        "grpcio>=1.60",
        # Autonomous-v2 _pb stubs are compiled with the 6.31 series of
        # protoc; the runtime must match (or exceed) the gencode version.
        # Upper bound keeps us compatible with downstream ecosystems
        # (google-cloud-aiplatform etc.) that still cap at <7.
        "protobuf>=6.31,<7",
        "prometheus-client>=0.20.0",  # kytte_platform_unreachable_seconds etc.
        # OTel API/SDK + OTLP exporter for internal telemetry (SDK → Aigie
        # backend); httpx instrumentation traces that export path.
        "opentelemetry-api>=1.20.0",
        "opentelemetry-sdk>=1.20.0",
        "opentelemetry-exporter-otlp-proto-http>=1.20.0",
        "opentelemetry-instrumentation-httpx>=0.41b0",
    ],
    # Optional dependencies for enhanced features
    extras_require={
        # Compression (recommended for production - 50-90% bandwidth savings)
        "compression": [
            "zstandard>=0.22.0",
        ],
        # OpenAI integration
        # Upper bound: openai 3.x is unreleased and would be a breaking major;
        # leaving it open forces pip to backtrack across every minor release
        # when co-installed with other extras and triggers `resolution-too-deep`.
        "openai": [
            "openai>=1.0.0,<3",
        ],
        # Anthropic Claude integration
        "anthropic": [
            "anthropic>=0.18.0",
        ],
        # Google Gemini integration
        "gemini": [
            "google-generativeai>=0.3.0",
        ],
        # LangChain integration
        "langchain": [
            "langchain-core>=0.1.0",
        ],
        # LangGraph integration
        "langgraph": [
            "langgraph>=0.0.20",
            "langchain-core>=0.1.0",
        ],
        # Claude Agent SDK integration (Anthropic's official agent SDK)
        "claude-agent-sdk": [
            "claude-agent-sdk>=0.0.10",
        ],
        # Vector Database integrations
        "pinecone": [
            "pinecone-client>=3.0.0",
        ],
        "qdrant": [
            "qdrant-client>=1.7.0",
        ],
        "chromadb": [
            "chromadb>=0.4.0",
        ],
        "weaviate": [
            "weaviate-client>=4.0.0",
        ],
        # All vector DBs
        "vectordbs": [
            "pinecone-client>=3.0.0",
            "qdrant-client>=1.7.0",
            "chromadb>=0.4.0",
            "weaviate-client>=4.0.0",
        ],
        # OpenTelemetry support (inbound: OTel → Aigie)
        "opentelemetry": [
            "opentelemetry-api>=1.20.0",
            "opentelemetry-sdk>=1.20.0",
        ],
        # OTLP export (outbound: Aigie → external OTel collectors via HTTP)
        "otlp": [
            "opentelemetry-api>=1.20.0",
            "opentelemetry-sdk>=1.20.0",
            "opentelemetry-exporter-otlp-proto-http>=1.20.0",
        ],
        # Internal OTel telemetry (Aigie SDK → Aigie backend)
        "internal-telemetry": [
            "opentelemetry-sdk>=1.20.0",
            "opentelemetry-exporter-otlp-proto-http>=1.20.0",
            "opentelemetry-semantic-conventions>=0.41b0",
        ],
        # Pandas support for DataFrame export
        "pandas": [
            "pandas>=1.5.0",
        ],
        # Development dependencies
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "pytest-httpx>=0.30.0",
            "pytest-benchmark>=4.0.0",
            "pytest-mock>=3.12.0",
            "respx>=0.20.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.5.0",
            "ruff>=0.1.0",
            "pytest-timeout",
            "tenacity>=8.2.0",
            # Autonomous v2 build/lint tooling — ADR 0001
            "grpcio-tools>=1.60",
            "import-linter>=2.0",
        ],
        # Documentation
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
            "sphinx-autodoc-typehints>=1.24.0",
        ],
        # All features (production-ready)
        "all": [
            # Compression
            "zstandard>=0.22.0",
            # LLM providers
            "openai>=1.0.0,<3",
            "anthropic>=0.18.0",
            "google-generativeai>=0.3.0",
            # Frameworks
            "langchain-core>=0.1.0",
            "langgraph>=0.0.20",
            "claude-agent-sdk>=0.0.10",
            # Observability
            "opentelemetry-api>=1.20.0",
            "opentelemetry-sdk>=1.20.0",
            "opentelemetry-exporter-otlp-proto-http>=1.20.0",
        ],
        # All integrations (frameworks only, no vector DBs)
        "integrations": [
            "langchain-core>=0.1.0",
            "langgraph>=0.0.20",
            "claude-agent-sdk>=0.0.10",
        ],
    },
    # Entry points for CLI tools and pytest plugins
    entry_points={
        "console_scripts": [
            # "aigie=aigie.cli:main",  # Future CLI tool
        ],
        "pytest11": [
            "aigie = aigie.pytest_plugin",
        ],
    },
    # Package data
    package_data={
        "aigie": ["py.typed"],  # PEP 561 typed package
    },
    # Zip safe
    zip_safe=False,
    # Project URLs
    project_urls={
        "Homepage": "https://kytte.ai/",
    },
)
