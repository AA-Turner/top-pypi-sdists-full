"""
OneEnv Pydantic Models for Environment Variable Templates

This module defines Pydantic models for type-safe environment variable templates.
環境変数テンプレート用のPydanticモデルを定義するモジュールです。
"""

from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field, field_validator, model_validator
import sys

if sys.version_info < (3, 10):
    from typing_extensions import Literal
else:
    from typing import Literal


class EnvVarConfig(BaseModel):
    """
    Configuration for a single environment variable
    単一の環境変数の設定
    """
    description: str = Field(
        ..., 
        min_length=1,
        description="Description of the environment variable (required)"
    )
    default: str = Field(
        default="",
        description="Default value for the environment variable"
    )
    required: bool = Field(
        default=False,
        description="Whether this environment variable is required"
    )
    choices: Optional[List[str]] = Field(
        default=None,
        description="List of valid choices for this environment variable"
    )
    group: Optional[str] = Field(
        default=None,
        description="Group name for organizing related environment variables"
    )
    importance: Literal["critical", "important", "optional"] = Field(
        default="important",
        description="Importance level for sorting (critical, important, optional)"
    )
    
    @field_validator('description')
    @classmethod
    def description_must_not_be_empty(cls, v):
        """Ensure description is not empty after stripping whitespace"""
        if not v.strip():
            raise ValueError('Description cannot be empty')
        return v.strip()
    
    @field_validator('choices')
    @classmethod
    def choices_must_not_be_empty(cls, v):
        """If choices are provided, they must not be an empty list"""
        if v is not None and len(v) == 0:
            raise ValueError('Choices list cannot be empty if provided')
        return v
    
    @model_validator(mode='after')
    def validate_default_in_choices(self):
        """If choices are provided and default is not empty, it must be in choices"""
        if self.choices and self.default and self.default not in self.choices:
            raise ValueError(f'Default value "{self.default}" must be one of the choices: {self.choices}')
        return self


class EnvTemplate(BaseModel):
    """
    Template containing multiple environment variables
    複数の環境変数を含むテンプレート
    """
    variables: Dict[str, EnvVarConfig] = Field(
        ...,
        description="Dictionary of environment variable names to their configurations"
    )
    source: str = Field(
        ...,
        description="Source identifier for this template (function name, plugin name, etc.)"
    )
    
    @field_validator('variables')
    @classmethod
    def variables_must_not_be_empty(cls, v):
        """Template must contain at least one environment variable"""
        if not v:
            raise ValueError('Template must contain at least one environment variable')
        return v
    
    @field_validator('source')
    @classmethod
    def source_must_not_be_empty(cls, v):
        """Source identifier must not be empty"""
        if not v.strip():
            raise ValueError('Source identifier cannot be empty')
        return v.strip()


class TemplateCollection(BaseModel):
    """
    Collection of templates from various sources with conflict resolution
    複数のソースからのテンプレートコレクション（競合解決機能付き）
    """
    templates: List[EnvTemplate] = Field(
        default_factory=list,
        description="List of environment variable templates"
    )
    
    def add_template(self, template: EnvTemplate) -> None:
        """Add a template to the collection"""
        self.templates.append(template)
    
    def get_merged_variables(self) -> Dict[str, Dict[str, Any]]:
        """
        Merge all templates and return variables with their sources
        重複した変数は説明を集約し、他の設定は最初のパッケージの情報を使用
        
        Returns:
            Dict[var_name, {"config": EnvVarConfig, "sources": List[str]}]
        """
        merged = {}
        
        for template in self.templates:
            for var_name, var_config in template.variables.items():
                if var_name in merged:
                    # Variable already exists - merge descriptions and track sources
                    existing_config = merged[var_name]["config"]
                    
                    # Collect descriptions from all sources
                    existing_desc = existing_config.description.strip()
                    new_desc = var_config.description.strip()
                    
                    # Merge descriptions if they're different
                    if new_desc and new_desc not in existing_desc:
                        merged_description = f"{existing_desc}\n\n# From {template.source}:\n{new_desc}"
                    else:
                        merged_description = existing_desc
                    
                    # Create new config with merged description but keep other settings from first source
                    merged_config = EnvVarConfig(
                        description=merged_description,
                        default=existing_config.default,  # Keep first source's default
                        required=existing_config.required,  # Keep first source's required
                        choices=existing_config.choices,    # Keep first source's choices
                        group=existing_config.group,        # Keep first source's group
                        importance=existing_config.importance  # Keep first source's importance
                    )
                    
                    merged[var_name]["config"] = merged_config
                    
                    # Add source if not already present
                    if template.source not in merged[var_name]["sources"]:
                        merged[var_name]["sources"].append(template.source)
                else:
                    # New variable
                    merged[var_name] = {
                        "config": var_config,
                        "sources": [template.source]
                    }
        
        return merged
    
    def get_duplicate_variables(self) -> Dict[str, List[str]]:
        """
        Get variables that are defined in multiple sources
        複数のソースで定義されている変数を取得
        
        Returns:
            Dict[var_name, List[source_names]]
        """
        merged = self.get_merged_variables()
        return {
            var_name: info["sources"]
            for var_name, info in merged.items()
            if len(info["sources"]) > 1
        }
    
    def get_grouped_variables(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """
        Get variables organized by importance and group
        重要度とグループで整理された変数を取得
        
        Returns:
            Dict[importance, Dict[group_name, Dict[var_name, var_info]]]
        """
        merged = self.get_merged_variables()
        grouped = {"critical": {}, "important": {}, "optional": {}}
        
        for var_name, var_info in merged.items():
            config = var_info["config"]
            importance = config.importance
            group = config.group or "General"  # Default group for ungrouped variables
            
            if group not in grouped[importance]:
                grouped[importance][group] = {}
            
            grouped[importance][group][var_name] = var_info
        
        return grouped
    
    def validate_all_templates(self) -> List[str]:
        """
        Validate all templates and return list of validation errors
        すべてのテンプレートを検証し、検証エラーのリストを返す
        
        Returns:
            List of error messages
        """
        errors = []
        
        for i, template in enumerate(self.templates):
            try:
                # Pydantic validation is automatic, but we can add custom checks
                if not template.variables:
                    errors.append(f"Template {i} from source '{template.source}' has no variables")
            except Exception as e:
                errors.append(f"Template {i} from source '{template.source}' validation error: {str(e)}")
        
        return errors


# Legacy compatibility functions for existing dictionary-based system
def dict_to_env_var_config(config_dict: Dict[str, Any]) -> EnvVarConfig:
    """
    Convert legacy dictionary configuration to EnvVarConfig model
    レガシーの辞書設定をEnvVarConfigモデルに変換
    """
    return EnvVarConfig(**config_dict)


def env_var_config_to_dict(config: EnvVarConfig) -> Dict[str, Any]:
    """
    Convert EnvVarConfig model to dictionary (for backward compatibility)
    EnvVarConfigモデルを辞書に変換（後方互換性のため）
    """
    result = {
        "description": config.description,
        "default": config.default,
        "required": config.required,
    }
    
    if config.choices is not None:
        result["choices"] = config.choices
    
    if config.group is not None:
        result["group"] = config.group
    
    if config.importance != "important":  # Only include if not default
        result["importance"] = config.importance
    
    return result


def template_function_to_env_template(func_name: str, template_dict: Dict[str, Any]) -> EnvTemplate:
    """
    Convert template function result to EnvTemplate model
    Support both legacy format and new groups format
    テンプレート関数結果をEnvTemplateモデルに変換
    レガシー形式と新しいgroups形式の両方をサポート
    """
    variables = {}
    
    # Check if this is the new groups format
    if "groups" in template_dict:
        # Process grouped variables
        groups_data = template_dict["groups"]
        if isinstance(groups_data, dict):
            for group_name, group_vars in groups_data.items():
                if isinstance(group_vars, dict):
                    for var_name, var_config in group_vars.items():
                        if isinstance(var_config, dict):
                            # Add group to config if not already specified
                            config_copy = var_config.copy()
                            if "group" not in config_copy:
                                config_copy["group"] = group_name
                            variables[var_name] = dict_to_env_var_config(config_copy)
                        else:
                            raise ValueError(f"Invalid variable config type for {var_name} in group {group_name}")
                else:
                    raise ValueError(f"Invalid group data type for group {group_name}")
        else:
            raise ValueError("Groups data must be a dictionary")
    
    # Process any variables defined outside of groups (legacy format or mixed)
    for key, value in template_dict.items():
        if key != "groups" and isinstance(value, dict):
            # This is a variable definition
            variables[key] = dict_to_env_var_config(value)
    
    if not variables:
        raise ValueError("Template must contain at least one environment variable")
    
    return EnvTemplate(
        variables=variables,
        source=func_name
    )


# Scaffolding System Models
class EnvOption(BaseModel):
    """
    スキャフォールディング用の環境変数オプション
    カテゴリ内の選択可能オプション（例：VectorStore内のChroma）
    """
    category: str = Field(
        ...,
        min_length=1,
        description="カテゴリ名（例：Database, VectorStore, RAG）"
    )
    option: str = Field(
        ...,
        min_length=1,
        description="オプション名（例：sqlite, chroma, openai）"
    )
    env: Dict[str, EnvVarConfig] = Field(
        ...,
        description="このオプション選択時に有効になる環境変数設定"
    )
    
    @field_validator('category')
    @classmethod
    def category_must_not_be_empty(cls, v):
        """Ensure category is not empty after stripping whitespace"""
        if not v.strip():
            raise ValueError('Category cannot be empty')
        return v.strip()
    
    @field_validator('option')
    @classmethod
    def option_must_not_be_empty(cls, v):
        """Ensure option is not empty after stripping whitespace"""
        if not v.strip():
            raise ValueError('Option cannot be empty')
        return v.strip()
    
    @field_validator('env')
    @classmethod
    def env_must_not_be_empty(cls, v):
        """Option must contain at least one environment variable"""
        if not v:
            raise ValueError('Option must contain at least one environment variable')
        return v


def dict_to_env_option(option_dict: Dict[str, Any]) -> EnvOption:
    """
    辞書形式の新テンプレートをEnvOptionモデルに変換
    """
    # env部分をEnvVarConfigに変換
    env_configs = {}
    env_data = option_dict.get("env", {})
    
    for var_name, var_config in env_data.items():
        if isinstance(var_config, dict):
            env_configs[var_name] = dict_to_env_var_config(var_config)
        else:
            raise ValueError(f"Invalid environment variable config for {var_name}")
    
    return EnvOption(
        category=option_dict["category"],
        option=option_dict["option"],
        env=env_configs
    )


def env_option_to_dict(env_option: EnvOption) -> Dict[str, Any]:
    """
    EnvOptionモデルを辞書形式に変換（後方互換性のため）
    """
    env_dict = {}
    for var_name, var_config in env_option.env.items():
        env_dict[var_name] = env_var_config_to_dict(var_config)
    
    return {
        "category": env_option.category,
        "option": env_option.option,
        "env": env_dict
    }


def validate_scaffolding_format(template_data: Any) -> bool:
    """
    Scaffolding形式のテンプレートデータを検証
    
    Args:
        template_data: テンプレート関数から返されたデータ
        
    Returns:
        検証成功時True
        
    Raises:
        ValueError: 不正な形式の場合
    """
    # 1. リスト形式必須
    if not isinstance(template_data, list):
        raise ValueError("Template must be a list of options")
    
    # 2. 空リスト禁止
    if not template_data:
        raise ValueError("Template cannot be empty")
    
    # 3. 各要素の検証
    category_option_pairs = set()
    
    for i, item in enumerate(template_data):
        # 辞書形式必須
        if not isinstance(item, dict):
            raise ValueError(f"Option {i}: Must be a dictionary")
        
        # 必須キー確認
        required_keys = {"category", "option", "env"}
        missing_keys = required_keys - set(item.keys())
        if missing_keys:
            raise ValueError(f"Option {i}: Missing required keys: {missing_keys}")
        
        # カテゴリ/オプション検証
        category = item["category"]
        option = item["option"]
        
        if not isinstance(category, str) or not category.strip():
            raise ValueError(f"Option {i}: category must be non-empty string")
        
        if not isinstance(option, str) or not option.strip():
            raise ValueError(f"Option {i}: option must be non-empty string")
        
        # 一意性検証
        pair = (category.strip(), option.strip())
        if pair in category_option_pairs:
            raise ValueError(f"Option {i}: Duplicate category/option pair: {category}/{option}")
        category_option_pairs.add(pair)
        
        # env検証
        env_data = item["env"]
        if not isinstance(env_data, dict) or not env_data:
            raise ValueError(f"Option {i}: env must be non-empty dictionary")
        
        # env内の各環境変数検証
        for var_name, var_config in env_data.items():
            if not isinstance(var_name, str) or not var_name.strip():
                raise ValueError(f"Option {i}: Environment variable name must be non-empty string")
            
            if not isinstance(var_config, dict):
                raise ValueError(f"Option {i}: Environment variable {var_name} config must be dictionary")
            
            # 必須フィールド確認
            if "description" not in var_config:
                raise ValueError(f"Option {i}: Environment variable {var_name} missing description")
    
    return True


def scaffolding_template_function_to_env_options(func_name: str, template_list: List[Dict[str, Any]]) -> List[EnvOption]:
    """
    新スキャフォールディング形式のテンプレート関数結果をEnvOptionリストに変換
    """
    env_options = []
    
    for option_dict in template_list:
        try:
            env_option = dict_to_env_option(option_dict)
            env_options.append(env_option)
        except Exception as e:
            raise ValueError(f"Invalid option in template function {func_name}: {str(e)}")
    
    return env_options


# Example usage and validation
if __name__ == "__main__":
    # Example environment variable configuration
    example_config = EnvVarConfig(
        description="Database connection URL",
        default="postgresql://localhost:5432/mydb",
        required=True,
        choices=None
    )
    
    print("Example EnvVarConfig:")
    print(example_config.model_dump_json(indent=2))
    
    # Example template
    example_template = EnvTemplate(
        variables={
            "DATABASE_URL": example_config,
            "DEBUG_MODE": EnvVarConfig(
                description="Enable debug mode",
                default="false",
                required=False,
                choices=["true", "false"]
            )
        },
        source="example_template"
    )
    
    print("\nExample EnvTemplate:")
    print(example_template.model_dump_json(indent=2))
    
    # Example collection
    collection = TemplateCollection()
    collection.add_template(example_template)
    
    merged = collection.get_merged_variables()
    print("\nMerged variables:")
    for var_name, info in merged.items():
        print(f"  {var_name}: {info['config'].description} (from: {', '.join(info['sources'])})")
    
    # Example scaffolding option
    example_scaffolding_option = EnvOption(
        category="Database",
        option="postgres",
        env={
            "DATABASE_URL": EnvVarConfig(
                description="PostgreSQL connection URL",
                default="postgresql://user:pass@localhost:5432/dbname",
                required=True
            ),
            "DATABASE_POOL_SIZE": EnvVarConfig(
                description="Connection pool maximum size",
                default="10",
                required=False
            )
        }
    )
    
    print("\nExample EnvOption:")
    print(example_scaffolding_option.model_dump_json(indent=2))
    
    # Test format validation
    scaffolding_data = [
        {
            "category": "Database",
            "option": "sqlite",
            "env": {
                "DATABASE_URL": {
                    "description": "SQLite database URL",
                    "default": "sqlite:///app.db",
                    "required": True
                }
            }
        }
    ]
    
    print(f"\nFormat validation:")
    try:
        validate_scaffolding_format(scaffolding_data)
        print("✅ Valid scaffolding format")
    except ValueError as e:
        print(f"❌ Invalid format: {e}")
    
    # Test invalid format
    invalid_data = {
        "DATABASE_URL": {
            "description": "Database connection URL",
            "default": "sqlite:///app.db"
        }
    }
    
    try:
        validate_scaffolding_format(invalid_data)
        print("❌ Should have failed validation")
    except ValueError as e:
        print(f"✅ Correctly rejected invalid format: {e}")
    
    # Test scaffolding conversion
    options = scaffolding_template_function_to_env_options("test_func", scaffolding_data)
    print(f"\nConverted to {len(options)} EnvOption(s)")
    for option in options:
        print(f"  {option.category}/{option.option}: {len(option.env)} env vars")