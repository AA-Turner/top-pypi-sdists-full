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
    pip install aigie[browser-use] # Browser-Use integration
    pip install aigie[crewai]      # CrewAI multi-agent
    pip install aigie[autogen]     # AutoGen/AG2 conversations
    pip install aigie[llamaindex]  # LlamaIndex RAG
    pip install aigie[openai-agents]  # OpenAI Agents SDK
    pip install aigie[dspy]        # DSPy modular LLM
    pip install aigie[claude-agent-sdk]  # Anthropic Claude Agent SDK
    pip install aigie[strands]  # Strands Agents SDK
    pip install aigie[google-adk]  # Google ADK
    pip install aigie[instructor]  # Instructor structured outputs
    pip install aigie[semantic-kernel]  # Microsoft Semantic Kernel

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

# Read long description from README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text() if readme_path.exists() else __doc__

setup(
    name="aigie",
    version="0.2.43",
    description="Enterprise-grade AI agent reliability monitoring and autonomous remediation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Aigie",
    author_email="support@aigie.io",
    url="https://github.com/Kytte-AI/kytte-python-sdk",
    package_dir={"": "sdk"},
    packages=find_packages(where="sdk", exclude=["tests", "tests.*", "examples", "examples.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
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
        # OTel infrastructure auto-instrumentation (DB, HTTP, cache visibility)
        # + OTLP exporter for internal telemetry (SDK → Aigie backend)
        "opentelemetry-api>=1.20.0",
        "opentelemetry-sdk>=1.20.0",
        "opentelemetry-exporter-otlp-proto-http>=1.20.0",
        "opentelemetry-instrumentation-psycopg2>=0.41b0",
        "opentelemetry-instrumentation-asyncpg>=0.41b0",
        "opentelemetry-instrumentation-redis>=0.41b0",
        "opentelemetry-instrumentation-httpx>=0.41b0",
        "opentelemetry-instrumentation-requests>=0.41b0",
        "opentelemetry-instrumentation-sqlalchemy>=0.41b0",
        "opentelemetry-instrumentation-aiohttp-client>=0.41b0",
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
        # when other extras (crewai pins openai<3) are co-installed and
        # triggers `resolution-too-deep`.
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
        # Browser-Use integration (web browser automation)
        "browser-use": [
            "browser-use>=0.1.0",
            "Pillow>=10.0.0",  # For screenshot compression
        ],
        # CrewAI integration (multi-agent orchestration)
        "crewai": [
            "crewai>=0.28.0",
        ],
        # AutoGen/AG2 integration (multi-agent conversations)
        "autogen": [
            "pyautogen>=0.2.0",
        ],
        # LlamaIndex integration (RAG workflows)
        "llamaindex": [
            "llama-index>=0.10.0",
        ],
        # Agno (formerly phidata) agent framework
        "agno": [
            "agno>=1.0.0",
        ],
        # OpenAI Agents SDK integration
        "openai-agents": [
            "openai-agents>=0.0.3",
        ],
        # DSPy integration (modular LLM programming)
        "dspy": [
            "dspy-ai>=2.4.0",
        ],
        # Claude Agent SDK integration (Anthropic's official agent SDK)
        "claude-agent-sdk": [
            "claude-agent-sdk>=0.0.10",
        ],
        # Strands Agents SDK integration (AWS/Anthropic's multi-agent framework)
        "strands": [
            "strands-agents>=0.1.0",
        ],
        # Google ADK integration (Google's Agent Development Kit)
        "google-adk": [
            "google-adk>=1.0.0",
        ],
        # LiveKit Agents integration (real-time voice AI)
        "livekit-agents": [
            "livekit-agents>=1.0.0",
        ],
        # Instructor integration (structured outputs)
        "instructor": [
            "instructor>=1.0.0",
        ],
        # Microsoft Semantic Kernel integration
        "semantic-kernel": [
            "semantic-kernel>=1.0.0",
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
            "browser-use>=0.1.0",
            "Pillow>=10.0.0",
            "crewai>=0.28.0",
            "pyautogen>=0.2.0",
            "llama-index>=0.10.0",
            "openai-agents>=0.0.3",
            "agno>=1.0.0",
            "dspy-ai>=2.4.0",
            "claude-agent-sdk>=0.0.10",
            "strands-agents>=0.1.0",
            "google-adk>=1.0.0",
            "instructor>=1.0.0",
            "semantic-kernel>=1.0.0",
            # Observability
            "opentelemetry-api>=1.20.0",
            "opentelemetry-sdk>=1.20.0",
            "opentelemetry-exporter-otlp-proto-http>=1.20.0",
        ],
        # All integrations (frameworks only, no vector DBs)
        "integrations": [
            "langchain-core>=0.1.0",
            "langgraph>=0.0.20",
            "browser-use>=0.1.0",
            "Pillow>=10.0.0",
            "crewai>=0.28.0",
            "pyautogen>=0.2.0",
            "llama-index>=0.10.0",
            "openai-agents>=0.0.3",
            "agno>=1.0.0",
            "dspy-ai>=2.4.0",
            "claude-agent-sdk>=0.0.10",
            "strands-agents>=0.1.0",
            "google-adk>=1.0.0",
            "instructor>=1.0.0",
            "semantic-kernel>=1.0.0",
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
        "Documentation": "https://docs.aigie.io",
        "Source": "https://github.com/Kytte-AI/kytte-python-sdk",
        "Tracker": "https://github.com/Kytte-AI/kytte-python-sdk/issues",
        "Changelog": "https://github.com/Kytte-AI/kytte-python-sdk/blob/main/CHANGELOG.md",
    },
)
