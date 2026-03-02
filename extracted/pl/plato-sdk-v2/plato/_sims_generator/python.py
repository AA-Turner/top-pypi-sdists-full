"""Python SDK generator."""

import json
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import yaml
from jinja2 import Environment, FileSystemLoader

from .parser import API, Endpoint


def to_snake_case(name: str) -> str:
    """Convert PascalCase to snake_case."""
    import re

    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()


@dataclass
class OAuthConfig:
    """OAuth configuration for client credentials flow."""

    client_id: str
    client_secret: str
    token_endpoint: str = "/oauth/token"
    scope: str = ""


@dataclass
class BearerTokenConfig:
    """Bearer token configuration."""

    default_token: str
    header: str = "Authorization"
    prefix: str = "Bearer"


@dataclass
class BasicAuthConfig:
    """Basic auth configuration."""

    default_username: str
    default_password: str


@dataclass
class SessionAuthConfig:
    """Session-based auth configuration."""

    login_endpoint: str
    default_username: str
    default_password: str


@dataclass
class AuthConfig:
    """Authentication configuration parsed from auth.yaml."""

    type: Literal["oauth", "bearer_token", "basic", "session"]
    env_prefix: str
    oauth: OAuthConfig | None = None
    bearer_token: BearerTokenConfig | None = None
    basic: BasicAuthConfig | None = None
    session: SessionAuthConfig | None = None
    base_path: str = ""  # API base path suffix (e.g., "/api/v1")

    @classmethod
    def from_yaml(cls, path: Path) -> "AuthConfig":
        """Parse auth config from YAML file."""
        with open(path) as f:
            data = yaml.safe_load(f)

        auth_type = data["type"]
        env_prefix = data["env_prefix"]
        base_path = data.get("base_path", "")

        oauth = None
        bearer_token = None
        basic = None
        session = None

        if auth_type == "oauth":
            oauth_data = data["oauth"]
            oauth = OAuthConfig(
                client_id=oauth_data["default_client_id"],
                client_secret=oauth_data["default_client_secret"],
                token_endpoint=oauth_data["token_endpoint"],
                scope=oauth_data.get("scope", ""),
            )
        elif auth_type == "bearer_token":
            bt_data = data["bearer_token"]
            bearer_token = BearerTokenConfig(
                default_token=bt_data["default_token"],
                header=bt_data.get("header", "Authorization"),
                prefix=bt_data.get("prefix", "Bearer"),
            )
        elif auth_type == "basic":
            basic_data = data["basic"]
            basic = BasicAuthConfig(
                default_username=basic_data["default_username"],
                default_password=basic_data["default_password"],
            )
        elif auth_type == "session":
            session_data = data["session"]
            session = SessionAuthConfig(
                login_endpoint=session_data["login_endpoint"],
                default_username=session_data["default_username"],
                default_password=session_data["default_password"],
            )

        return cls(
            type=auth_type,
            env_prefix=env_prefix,
            oauth=oauth,
            bearer_token=bearer_token,
            basic=basic,
            session=session,
            base_path=base_path,
        )


class PythonGenerator:
    def __init__(
        self,
        api: API,
        output_path: Path,
        spec: dict | None = None,
        package_name: str = "generated",
        env_prefix: str = "API",
        auth_config: AuthConfig | None = None,
        generator_version: str | None = None,
        # Legacy params for backwards compatibility
        oauth_config: OAuthConfig | None = None,
        default_token: str | None = None,
    ):
        self.api = api
        self.output = output_path
        self.spec = spec  # Original OpenAPI spec for datamodel-codegen
        self.package_name = package_name
        self.generator_version = generator_version

        # Auth config takes precedence
        self.auth_config = auth_config
        if auth_config:
            self.env_prefix = auth_config.env_prefix
            self.oauth_config = auth_config.oauth
            self.default_token = auth_config.bearer_token.default_token if auth_config.bearer_token else None
            self.basic_config = auth_config.basic
            self.session_config = auth_config.session
            self.base_path = auth_config.base_path
        else:
            self.env_prefix = env_prefix.upper()
            self.oauth_config = oauth_config
            self.default_token = default_token
            self.basic_config = None
            self.session_config = None
            self.base_path = ""

        self.template_dir = Path(__file__).parent / "templates" / "python"
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        # Add custom filters
        self.env.filters["snake"] = to_snake_case

    def generate(self):
        """Generate the full SDK."""
        # Create output structure
        self.output.mkdir(parents=True, exist_ok=True)

        # Generate errors module
        self._generate_errors()

        # Generate models
        self._generate_models()

        # Generate API modules by tag
        self._generate_api()

        # Generate client
        self._generate_client()

        # Generate package init
        self._generate_init()

        # Generate py.typed marker
        self._generate_py_typed()

        # Format with ruff
        self._format()

    def _generate_errors(self):
        """Generate the errors module."""
        template = self.env.get_template("errors.py.jinja")
        content = template.render(api=self.api)
        (self.output / "errors.py").write_text(content)

    def _inject_inline_schemas(self, spec: dict) -> dict:
        """Inject inline request body schemas into the OpenAPI spec.

        These are schemas parsed from inline request bodies that need to be
        added to the spec so datamodel-codegen can generate them.
        """
        import copy

        spec = copy.deepcopy(spec)

        # Ensure components/schemas exists
        if "components" not in spec:
            spec["components"] = {}
        if "schemas" not in spec["components"]:
            spec["components"]["schemas"] = {}

        # Add inline schemas that aren't already in the spec
        for name, schema in self.api.schemas.items():
            if name not in spec["components"]["schemas"] and schema.properties:
                # Convert our Schema object to OpenAPI schema format
                schema_dict: dict = {
                    "type": "object",
                    "properties": {},
                }
                required_fields = []

                for prop in schema.properties:
                    prop_dict: dict = {}

                    # Map Type to OpenAPI type
                    prop_type = prop.type
                    # Unwrap optional to get inner type
                    if prop_type.kind.value == "optional" and prop_type.inner:
                        prop_type = prop_type.inner

                    type_mapping = {
                        "string": "string",
                        "int": "integer",
                        "float": "number",
                        "bool": "boolean",
                        "any": "object",
                        "map": "object",
                        "list": "array",
                    }
                    openapi_type = type_mapping.get(prop_type.kind.value, "string")
                    prop_dict["type"] = openapi_type

                    if prop.description:
                        prop_dict["description"] = prop.description

                    schema_dict["properties"][prop.name] = prop_dict

                    if prop.required:
                        required_fields.append(prop.name)

                if required_fields:
                    schema_dict["required"] = required_fields

                if schema.description:
                    schema_dict["description"] = schema.description

                spec["components"]["schemas"][name] = schema_dict

        return spec

    def _generate_models(self):
        """Generate Pydantic models using datamodel-code-generator."""
        import shutil

        from datamodel_code_generator import InputFileType, generate
        from datamodel_code_generator.enums import DataModelType

        models_dir = self.output / "models"
        # Clean up existing models directory
        if models_dir.exists():
            shutil.rmtree(models_dir)
        models_dir.mkdir(parents=True, exist_ok=True)

        if self.spec is None:
            raise ValueError("OpenAPI spec required for model generation")

        # Inject inline schemas into spec
        spec_with_inline = self._inject_inline_schemas(self.spec)

        # Write spec to temp file for datamodel-codegen
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(spec_with_inline, f)
            spec_path = Path(f.name)

        try:
            # Generate all models to a single __init__.py file
            output_file = models_dir / "__init__.py"
            generate(
                input_=spec_path,
                input_file_type=InputFileType.OpenAPI,
                output=output_file,
                output_model_type=DataModelType.PydanticV2BaseModel,
                use_field_description=True,
                field_constraints=True,
                use_annotated=True,
                use_one_literal_as_default=True,
                use_default_kwarg=True,
                reuse_model=True,
                collapse_root_models=False,
                use_union_operator=True,
                set_default_enum_member=True,
                # Allow extra fields so AdaptiveObject subclass fields aren't stripped
                allow_extra_fields=True,
            )

            # Post-process to fix Pydantic inheritance issues
            self._fix_model_inheritance(output_file)
        finally:
            spec_path.unlink()  # Clean up temp file

    def _fix_model_inheritance(self, models_file: Path):
        """Fix Pydantic inheritance issues in generated models.

        Specifically handles cases where a child model tries to override a parent's
        optional field with a required field, which violates Pydantic's type safety.
        We use Field(default=...) to mark fields as required in a type-safe way.
        """
        import re

        content = models_file.read_text()
        lines = content.split("\n")

        # Track if we need to add Field import
        needs_field_import = False

        # Find class definitions and their fields
        # Pattern: class ChildClass(ParentClass):
        class_pattern = re.compile(r"^class\s+(\w+)\(([\w,\s]+)\):")
        # Pattern: field_name: Type (without default)
        field_pattern = re.compile(r"^\s{4}(\w+):\s+([^=]+)$")

        i = 0
        while i < len(lines):
            line = lines[i]
            class_match = class_pattern.match(line)

            if class_match:
                # Extract class info (group 1 = class name, group 2 = parent classes)
                _ = class_match.group(1)  # class_name - not used but needed for match
                _ = [p.strip() for p in class_match.group(2).split(",")]  # parent_names

                # Look ahead for fields without defaults (required fields)
                j = i + 1
                while j < len(lines):
                    field_match = field_pattern.match(lines[j])
                    if field_match:
                        field_name = field_match.group(1)
                        field_type = field_match.group(2).strip()

                        # If field type is NOT optional (doesn't end with | None)
                        # but parent might have it as optional, add Field(default=...)
                        if not field_type.endswith("| None") and not field_type.endswith("| None "):
                            # Check if next line is a docstring (starts with """)
                            if j + 1 < len(lines) and lines[j + 1].strip().startswith('"""'):
                                # Use Field to mark as required, add type ignore for pyright
                                # This is needed because OpenAPI specs sometimes have inheritance
                                # where child makes parent's optional field required
                                lines[j] = (
                                    f"    {field_name}: {field_type} = Field(default=...)  # type: ignore[assignment]"
                                )
                                needs_field_import = True

                    # Stop when we hit another class or end of indentation
                    if lines[j] and not lines[j].startswith("    ") and not lines[j].startswith("\t"):
                        break
                    j += 1

            i += 1

        # Add Field import if needed
        if needs_field_import:
            # Find the pydantic import line and add Field
            for i, line in enumerate(lines):
                if line.startswith("from pydantic import"):
                    if "Field" not in line:
                        # Add Field to existing import
                        lines[i] = line.rstrip() + ", Field"
                    break

        models_file.write_text("\n".join(lines))

    def _generate_api(self):
        """Generate API modules organized by tag."""
        api_dir = self.output / "api"
        api_dir.mkdir(exist_ok=True)

        # Group endpoints by tag
        by_tag: dict[str, list[Endpoint]] = {}
        for endpoint in self.api.endpoints:
            by_tag.setdefault(endpoint.tag, []).append(endpoint)

        template = self.env.get_template("endpoint.py.jinja")
        tag_dirs = []

        for tag, endpoints in sorted(by_tag.items()):
            # Create tag directory: v1.simulator -> v1/simulator
            tag_path = api_dir / tag.replace(".", "/")
            tag_path.mkdir(parents=True, exist_ok=True)
            tag_dirs.append(tag)

            # Calculate relative import depth: api/ + tag depth + file = len(tag.split('.')) + 2
            tag_depth = len(tag.split(".")) + 2
            relative_prefix = "." * tag_depth

            endpoint_names = []

            for endpoint in endpoints:
                # Detect streaming endpoints
                endpoint.streaming = self._is_streaming_endpoint(endpoint)

                content = template.render(
                    endpoint=endpoint,
                    api=self.api,
                    package_name=self.package_name,
                    relative_prefix=relative_prefix,
                )
                filename = endpoint.function_name + ".py"
                (tag_path / filename).write_text(content)
                endpoint_names.append(endpoint.function_name)

            # Generate tag __init__.py
            tag_init = self.env.get_template("tag_init.py.jinja")
            (tag_path / "__init__.py").write_text(tag_init.render(endpoints=endpoint_names))

            # Generate version __init__.py (e.g., v1/__init__.py)
            if "." in tag:
                version_dir = tag_path.parent
                self._ensure_version_init(version_dir, by_tag)

        # Generate api/__init__.py
        api_init = self.env.get_template("api_init.py.jinja")
        versions = sorted(set(t.split(".")[0] for t in tag_dirs if "." in t))
        (api_dir / "__init__.py").write_text(api_init.render(versions=versions))

    def _is_streaming_endpoint(self, endpoint: Endpoint) -> bool:
        """Detect if endpoint is a streaming endpoint."""
        if "stream" in endpoint.operation_id.lower():
            return True
        if "stream" in endpoint.path.lower():
            return True
        return False

    def _ensure_version_init(self, version_dir: Path, by_tag: dict):
        """Generate __init__.py for version directories like v1/, v2/."""
        version = version_dir.name
        # Find all tags under this version
        modules = sorted(t.split(".", 1)[1] for t in by_tag.keys() if t.startswith(f"{version}."))

        template = self.env.get_template("version_init.py.jinja")
        (version_dir / "__init__.py").write_text(template.render(modules=modules))

    def _generate_client(self):
        """Generate the HTTP client."""
        template = self.env.get_template("client.py.jinja")
        content = template.render(
            api=self.api,
            env_prefix=self.env_prefix,
            auth_config=self.auth_config,
            oauth_config=self.oauth_config,
            default_token=self.default_token,
            basic_config=self.basic_config,
            session_config=self.session_config,
            base_path=self.base_path,
        )
        (self.output / "client.py").write_text(content)

    def _generate_init(self):
        """Generate package __init__.py."""
        template = self.env.get_template("package_init.py.jinja")
        content = template.render(api=self.api, generator_version=self.generator_version)
        (self.output / "__init__.py").write_text(content)

    def _generate_py_typed(self):
        """Generate py.typed marker for PEP 561 compliance."""
        (self.output / "py.typed").write_text("")

    def _format(self):
        """Format generated code with ruff."""
        try:
            subprocess.run(
                ["ruff", "check", str(self.output), "--fix", "--quiet"],
                capture_output=True,
            )
            subprocess.run(
                ["ruff", "format", str(self.output), "--quiet"],
                capture_output=True,
            )
        except FileNotFoundError:
            pass  # ruff not installed, skip formatting

    @staticmethod
    def _to_filename(class_name: str) -> str:
        """Convert PascalCase to snake_case for filenames."""
        import re

        name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", class_name)
        return name.lower()
