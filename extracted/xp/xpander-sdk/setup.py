from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="xpander-sdk",
    version="2.0.503",
    author="xpanderAI",
    author_email="dev@xpander.ai",
    description="xpander.ai Backend-as-a-service for AI Agents - SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.xpander.ai",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "python-dotenv>=1.2.1",
        "packaging>=25.0",
        "pydantic>=2.12.5",
        "loguru>=0.7.3",
        "httpx>=0.28.1",
        "httpx_sse>=0.4.3",
        "fastapi>=0.115.0",
        "uvicorn>=0.30.0",
        "nest-asyncio>=1.6.0",
        "strands-agents>=1.20.0",
        "openai-agents>=0.6.4",
        "headroom-ai>=0.26.0",
        "firecrawl-anydoc>=0.1.7,<0.1.8",
        "python-docx>=1.1.2",
        "openpyxl>=3.1.5",
        "python-pptx>=1.0.2",
        "pillow",
        "pypdf",
    ],
    extras_require={
        "agno": [
            "agno==2.5.14",
            "sqlalchemy",
            "psycopg[binary,pool]",
            "greenlet",
            "aioboto3==15.5.0",
        ],
        "test": [
            "pytest",
            "pytest-asyncio",
            "pytest-cov",
            "agno==2.5.14",
            "sqlalchemy",
            "psycopg[binary,pool]",
            "greenlet",
            # Bedrock prompt-cache path (CachingAwsBedrock) imports anthropic + aioboto3
            # transitively; needed so test collection can import the module.
            # anthropic 1.x rejects the httpx.Client agno 2.5.14 passes as http_client
            "anthropic<1",
            "aioboto3==15.5.0",
            # gemini llm_api_base routing tests construct the real client
            "google-genai>=1.52.0",
        ],
        "dev": [
            "black",
            "pre-commit",
            "pytest",
            "pytest-asyncio",
            "pytest-cov",
            "anthropic<1",
            "mcp",
            "openai",
            "fireworks-ai",
            "aioboto3==15.5.0",
            "google-genai>=1.52.0",
            "azure-ai-inference",
            "aiohttp",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
