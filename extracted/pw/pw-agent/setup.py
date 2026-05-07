from setuptools import setup

setup(
    name="pw-agent",
    version="1.50.37",
    description="CLI coding assistant powered by your Ollama GPUs via PastaWater",
    long_description=open("README.md").read() if __import__("os").path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="PastaWater",
    author_email="support@pastawater.io",
    url="https://pastawater.io",
    project_urls={
        "Homepage": "https://pastawater.io",
        "GPU Setup": "https://pastawater.io/gpu-setup",
    },
    py_modules=["pw_agent", "agent", "llm_client", "tools", "config", "memory", "skills", "hooks", "subagent", "mcp_client", "codebase_index", "voice", "mcp_server", "lora_prep", "fleet"],
    install_requires=[
        "requests>=2.28.0",
        "rich>=13.0.0",
        "prompt_toolkit>=3.0.0",
        "numpy>=1.24.0",
    ],
    entry_points={
        "console_scripts": [
            "pw-agent=pw_agent:main",
        ],
    },
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
    ],
)
