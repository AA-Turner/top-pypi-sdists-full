from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dc-securex",
    version="3.3.1",
    author="SecureX Team",
    author_email="contact@securex.dev",
    description="Backend-only Discord anti-nuke protection SDK - Build your own UI!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/securex-antinuke-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Chat",
        "Framework :: Discord",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "discord.py>=2.0.0",
        "aiofiles>=23.0.0",
        "aiosqlite>=0.17.0",
    ],
    extras_require={
        "postgres": ["asyncpg>=0.27.0"],
    },
    keywords="discord bot antinuke security protection sdk backend api",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/securex-antinuke-sdk/issues",
        "Source": "https://github.com/yourusername/securex-antinuke-sdk",
        "Documentation": "https://github.com/yourusername/securex-antinuke-sdk/blob/main/README.md",
    },
)
