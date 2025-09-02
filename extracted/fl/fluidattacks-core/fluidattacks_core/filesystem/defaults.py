from enum import Enum


class Language(Enum):
    Swift = "swift"
    CSharp = "csharp"
    Go = "golang"
    FuzzyTestLang = "fuzzy_test_lang"
    Java = "Java"
    Python = "Python"
    PHP = "PHP"
    Ruby = "Ruby"
    C = "C"
    Kotlin = "Kotlin"
    Ghidra = "Ghidra"
    JavaScript = "JavaScript"
    TypeScript = "TypeScript"
    LLVM = "LLVM"
    NewC = "newc"
    Scala = "Scala"
    Unknown = "unknown"


CONFIG_MARKERS: dict[Language, dict[str, set[str] | list[str]]] = {
    Language.Java: {
        "names": {
            "pom.xml",
            "settings.gradle",
            "settings.gradle.kts",
            "build.gradle",
            "build.gradle.kts",
            "gradle.properties",
            "gradlew",
            "gradlew.bat",
            "mvnw",
            "mvnw.cmd",
            "application.properties",
            "application.yml",
            "log4j.properties",
            "web.xml",
            "hibernate.cfg.xml",
            "persistence.xml",
            "sonar-project.properties",
            "checkstyle.xml",
        },
        "globs": [],
    },
    Language.Python: {
        "names": {
            "pyproject.toml",
            "requirements.txt",
            "requirements.in",
            "constraints.txt",
            "setup.py",
            "setup.cfg",
            "Pipfile",
            "Pipfile.lock",
            "poetry.lock",
            "poetry.toml",
            "hatch.toml",
            "tox.ini",
            "pytest.ini",
            "mypy.ini",
            ".pylintrc",
            "pylintrc",
            ".flake8",
            ".isort.cfg",
            "ruff.toml",
            ".ruff.toml",
            ".coveragerc",
            "noxfile.py",
            "config.yaml",
        },
        "globs": [],
    },
    Language.JavaScript: {
        "names": {
            "package.json",
            "package-lock.json",
            "yarn.lock",
            "pnpm-lock.yaml",
            "bun.lockb",
            "bunfig.toml",
            "nx.json",
            "lerna.json",
            "turbo.json",
            "angular.json",
            "workspace.json",
            "gulpfile.js",
            "gulpfile.ts",
            "gruntfile.js",
        },
        "globs": [
            "vite.config.*",
            "next.config.*",
            "nuxt.config.*",
            "svelte.config.*",
            "astro.config.*",
            "rollup.config.*",
            "webpack.config.*",
            "babel.config.*",
            ".babelrc*",
            "eslint.config.*",
            ".eslintrc*",
            ".prettierrc*",
            "prettier.config.*",
            "jest.config.*",
        ],
    },
    Language.TypeScript: {
        "names": {
            "tsconfig.json",
            "tsconfig.base.json",
            "tsconfig.app.json",
            "tsconfig.build.json",
            "tsconfig.node.json",
            "deno.json",
            "deno.jsonc",
        },
        "globs": [
            "tsconfig.*.json",
        ],
    },
    Language.PHP: {
        "names": {
            "composer.json",
            "composer.lock",
            "php.ini",
            "phpunit.xml",
            "phpunit.xml.dist",
            "phpcs.xml",
            "phpcs.xml.dist",
            "phpmd.xml",
            "phpstan.neon",
            "phpstan.neon.dist",
            "psalm.xml",
            "psalm.xml.dist",
            ".php-cs-fixer.php",
            ".php_cs",
            ".php_cs.dist",
            "codeception.yml",
            "symfony.lock",
            "artisan",
            "wp-config.php",
            ".env",
        },
        "globs": [
            "phpspec.yml*",
        ],
    },
    Language.CSharp: {
        "names": {
            "app.config",
            "web.config",
            "packages.config",
            "nuget.config",
            "NuGet.Config",
            "Directory.Build.props",
            "Directory.Build.targets",
            "Directory.Packages.props",
            "global.json",
            "appsettings.json",
        },
        "globs": [
            "*.sln",
            "*.csproj",
            "*.fsproj",
            "*.vbproj",
            "appsettings.*.json",
        ],
    },
    Language.Go: {
        "names": {
            "go.mod",
            "go.sum",
            "go.work",
            "go.work.sum",
            ".golangci.yml",
            ".golangci.yaml",
            "Gopkg.toml",
            "Gopkg.lock",
            "glide.yaml",
            "glide.lock",
        },
        "globs": [],
    },
    Language.Ruby: {
        "names": {
            "Gemfile",
            "Gemfile.lock",
            ".ruby-version",
            ".rubocop.yml",
            ".reek",
            ".rspec",
            ".overcommit.yml",
            "Rakefile",
            "Capfile",
            "Guardfile",
            "config.ru",
            "database.yml",
            "boot.rb",
        },
        "globs": [],
    },
    Language.Kotlin: {
        "names": {
            "build.gradle.kts",
            "settings.gradle.kts",
            "build.gradle",
            "settings.gradle",
            "gradle.properties",
            "pom.xml",
            "gradlew",
            "gradlew.bat",
        },
        "globs": [],
    },
    Language.Swift: {
        "names": {
            "Package.swift",
            "Package.resolved",
            "Config.xcconfig",
            "Info.plist",
            "project.pbxproj",
            ".swiftlint.yml",
            ".swiftformat",
            "Cartfile",
            "Cartfile.resolved",
            "Podfile",
            "Podfile.lock",
        },
        "globs": [],
    },
    Language.Scala: {
        "names": {
            "build.sbt",
        },
        "globs": [],
    },
}

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    "*cache*",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    "target",
    "*test*",
    "out",
    "bin",
    "obj",
}


TEST_GLOBS = {
    Language.Python: [
        "test*",  # Python
        "*test.py",  # Python
    ],
    Language.JavaScript: [
        "*.spec.js",  # JavaScript
        "*.test.js",  # JavaScript
    ],
    Language.TypeScript: [
        "*.spec.ts",  # TypeScript
        "*.test.ts",  # TypeScript
    ],
    Language.Java: [
        "*Test.java",  # Java
    ],
    Language.Kotlin: [
        "*Test.kt",  # Kotlin
    ],
    Language.Go: [
        "*_test.go",  # Go
    ],
    Language.Ruby: [
        "*_test.rb",  # Ruby
    ],
    Language.CSharp: [
        "*.Tests.cs",  # C#
    ],
    Language.Swift: [
        "*Test.swift",  # Swift
    ],
}


EXCLUDE_DIRS = [
    "assets",
    "target",
    "build",
    ".gradle",
    ".mvn",
    ".idea",
    "out",
    "src/test",
    "tests",
    "__tests__",
    "spec",
    ".venv",
    "__pycache__",
    "dist",
    ".tox",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
    ".cache",
    "vendor",
    ".composer",
    "bin",
    "obj",
    ".vs",
    "packages",
    ".vscode",
    "pkg",
    ".bundle",
    "tmp",
    ".build",
    "Carthage",
    "Pods",
    "DerivedData",
    "cache",
    ".ruff_cache",
    ".metals",
    ".bloop",
    "wwwroot",
    "plugin",
    "plugins",
    "libraries",
    "target/deps",
    ".stack-work",
    "dist-newstyle",
    ".dart_tool",
    "deps",
    "_build",
    "checkouts",
    "target/scala-*",
    "*.min.js",
    "*.min.css",
    "*.jar",
    "*.war",
    "*.ear",
    "*.jmod",
    "*.nupkg",
    "*.gem",
    "*.phar*",
    "*.so",
    "*.dll",
    "*.dylib",
    "*.a",
    "*.lib",
    "*.rlib",
    "*.rs.bk",
    "*.rs",
    "Cargo.lock",
    "Cargo.toml",
    "gradlew*",
    "*mock*",
]


TEST_FILES = [x for item in TEST_GLOBS.values() for x in item]
