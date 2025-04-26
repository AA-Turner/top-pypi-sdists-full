import os
import aiohttp
import asyncio
import json
import sys
import re
from json_repair import repair_json
import platform

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class DependencyFileFinderAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_dependency_file_planning(self, tree):
        """
        Identify critical dependency and configuration files in the project structure.

        Args:
            tree (str): The project structure.

        Returns:
            dict: Dictionary with the dependency file paths.
        """
        logger.debug("\n #### `SnowX` is initiating dependency file planning")
        
        # Comprehensive dependency file patterns covering various tech stacks
        dependency_patterns = [
            # JavaScript/Node.js
            "package.json", "yarn.lock", "pnpm-lock.yaml", "npm-shrinkwrap.json", "bower.json",
            # Python
            "requirements.txt", "Pipfile", "pyproject.toml", "setup.py", "poetry.lock", "conda.yaml", "environment.yml",
            # Ruby
            "Gemfile", "gems.rb",
            # Java/Kotlin/Scala
            "pom.xml", "build.gradle", "build.gradle.kts", "settings.gradle", "ivy.xml", "build.sbt",
            # .NET/C#
            "*.csproj", "*.fsproj", "packages.config", "paket.dependencies", "*.sln",
            # PHP
            "composer.json", "composer.lock",
            # Go
            "go.mod", "go.sum", "Gopkg.toml", "glide.yaml",
            # Rust
            "Cargo.toml", "Cargo.lock",
            # Swift/iOS/macOS
            "Podfile", "Package.swift", "Cartfile",
            # Docker/Containers
            "Dockerfile", "docker-compose.yml", "docker-compose.yaml",
            # Web
            "webpack.config.js", "rollup.config.js", "vite.config.js", "tsconfig.json",
            # Other
            "pubspec.yaml", "mix.exs", "rebar.config", "deps.edn", "project.clj",
            "build.xml", "meson.build", "CMakeLists.txt", "Makefile", "configure.ac",
            "snowx.md"
        ]
        
        # Files to exclude
        exclude_patterns = [
            "node_modules/",
            "build/",
            "dist/",
            ".git/",
            "vendor/",
            "target/",
            "bin/",
            "obj/"
        ]
        
        # Use regex to find filenames
        file_paths = []
        repo_path = self.repo.get_repo_path()
        
        # Walk through the repo directory to find dependency files
        for root, dirs, files in os.walk(repo_path):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if not any(exclude == d + '/' for exclude in exclude_patterns)]
            
            for file in files:
                # Check if file matches any dependency pattern
                file_path = os.path.join(root, file)
                
                # Skip files in excluded paths
                if any(exclude in file_path for exclude in exclude_patterns):
                    continue
                
                # Match against dependency patterns
                for pattern in dependency_patterns:
                    if '*' in pattern:
                        extension = pattern.replace('*', '')
                        if file.endswith(extension):
                            file_paths.append(file_path)
                            break
                    elif pattern == file:
                        file_paths.append(file_path)
                        break

        
        logger.debug(f"\n #### `SnowX` identified {len(file_paths)} dependency files")
        
        return {
            "dependency_files": file_paths
        }


    async def get_dependency_file_plannings(self):
        logger.debug("\n #### `SnowX` is starting to gather dependency file plannings")
        all_dependency_file_contents = self.repo.print_tree()

        logger.debug("\n #### `SnowX` is processing the project structure")
        plan = await self.get_dependency_file_planning(all_dependency_file_contents)
        return plan
