"""
OneEnv Core Module with Pydantic Models and Entry-points Support

Enhanced version of OneEnv that supports both legacy decorator-based templates
and new entry-points based plugins with Pydantic model validation.
"""

import sys
import locale
import os
from typing import Dict, List, Any, Optional, Callable

# Handle different Python versions for importlib.metadata
if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points

try:
    from .models import (
        EnvVarConfig, 
        EnvTemplate, 
        TemplateCollection,
        EnvOption,
        dict_to_env_var_config,
        env_var_config_to_dict,
        template_function_to_env_template,
        validate_scaffolding_format,
        scaffolding_template_function_to_env_options,
        env_var_config_to_dict
    )
except ImportError:
    # Fallback for development/testing
    import sys
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from models import (
        EnvVarConfig, 
        EnvTemplate, 
        TemplateCollection,
        EnvOption,
        dict_to_env_var_config,
        env_var_config_to_dict,
        template_function_to_env_template,
        validate_scaffolding_format,
        scaffolding_template_function_to_env_options,
        env_var_config_to_dict
    )


class OneEnvCore:
    """
    Core OneEnv functionality with support for both legacy and new systems
    レガシーシステムと新システムの両方をサポートするOneEnvコア機能
    """
    
    def __init__(self, entry_point_group: str = "oneenv.templates"):
        self.entry_point_group = entry_point_group
        self.template_collection = TemplateCollection()
        self._legacy_registry: List[Callable] = []
    
    def _detect_locale(self) -> str:
        """
        Detect system locale to determine language for section headers
        システムロケールを検出してセクションヘッダーの言語を決定
        
        Returns:
            "ja" for Japanese locale, "en" for others
        """
        try:
            # Check environment variables first
            lang = os.environ.get('LANG', '').lower()
            if 'ja' in lang or 'jp' in lang:
                return "ja"
            
            # Check system locale
            current_locale = locale.getlocale()[0]
            if current_locale and ('ja' in current_locale.lower() or 'jp' in current_locale.lower()):
                return "ja"
                
            # Check default locale
            default_locale = locale.getdefaultlocale()[0]
            if default_locale and ('ja' in default_locale.lower() or 'jp' in default_locale.lower()):
                return "ja"
                
        except Exception:
            # If any error occurs, default to English
            pass
            
        return "en"
    
    def _get_importance_headers(self, detected_locale: str = None) -> Dict[str, str]:
        """
        Get importance section headers based on locale
        ロケールに基づいて重要度セクションヘッダーを取得
        
        Args:
            detected_locale: Override locale detection (for testing)
        
        Returns:
            Dictionary mapping importance levels to localized headers
        """
        if detected_locale is None:
            detected_locale = self._detect_locale()
        
        if detected_locale == "ja":
            return {
                "critical": "# ========== CRITICAL: 必須設定項目 ==========",
                "important": "# ========== IMPORTANT: 重要設定項目 ==========", 
                "optional": "# ========== OPTIONAL: デフォルトで十分 =========="
            }
        else:
            return {
                "critical": "# ========== CRITICAL: Essential Settings for Application Operation ==========",
                "important": "# ========== IMPORTANT: Settings to Configure for Production Use ==========",
                "optional": "# ========== OPTIONAL: Fine-tuning Settings (Defaults are Sufficient) =========="
            }
    
    def register_legacy_function(self, func: Callable) -> Callable:
        """
        Register a legacy decorator-based template function
        レガシーデコレータベースのテンプレート関数を登録
        """
        self._legacy_registry.append(func)
        return func
    
    def discover_entry_point_templates(self, debug: bool = False) -> List[EnvTemplate]:
        """
        Discover and load templates from entry-points
        Entry-pointsからテンプレートを発見・読み込み
        """
        discovered_templates = []
        
        try:
            template_eps = entry_points(group=self.entry_point_group)
            
            for ep in template_eps:
                try:
                    # Load the entry-point function
                    template_func = ep.load()
                    
                    # Call the function to get template data
                    template_result = template_func()
                    
                    # Convert to EnvTemplate with validation
                    env_template = self._convert_template_result_to_model(
                        template_result, f"plugin:{ep.name}"
                    )
                    
                    discovered_templates.append(env_template)
                    
                    if debug:
                        print(f"Loaded template plugin: {ep.name}")
                        
                except Exception as e:
                    if debug:
                        print(f"Failed to load template plugin {ep.name}: {e}")
                        
        except Exception as e:
            if debug:
                print(f"Error discovering template plugins: {e}")
        
        return discovered_templates
    
    def discover_legacy_templates(self, debug: bool = False) -> List[EnvTemplate]:
        """
        Convert legacy decorator-based templates to EnvTemplate models
        レガシーデコレータベースのテンプレートをEnvTemplateモデルに変換
        """
        legacy_templates = []
        
        for func in self._legacy_registry:
            try:
                # Call the legacy function
                template_dict = func()
                
                # Convert to EnvTemplate with validation
                env_template = template_function_to_env_template(func.__name__, template_dict)
                legacy_templates.append(env_template)
                
                if debug:
                    print(f"Loaded legacy template: {func.__name__}")
                    
            except Exception as e:
                if debug:
                    print(f"Failed to load legacy template {func.__name__}: {e}")
        
        return legacy_templates
    
    def _convert_template_result_to_model(self, template_result: Any, source: str) -> EnvTemplate:
        """
        Convert template function result to EnvTemplate model with validation
        Supports both legacy format and new groups format
        テンプレート関数の結果をEnvTemplateモデルに変換（検証付き）
        レガシー形式と新しいgroups形式の両方をサポート
        """
        if isinstance(template_result, dict):
            # Use the enhanced template_function_to_env_template function
            # which supports both legacy and groups format
            return template_function_to_env_template(source, template_result)
        
        elif isinstance(template_result, EnvTemplate):
            # Already an EnvTemplate
            template_result.source = source  # Override source
            return template_result
        
        else:
            raise ValueError(f"Invalid template result type: {type(template_result)}")
    
    def collect_all_templates(self, 
                            discover_plugins: bool = True, 
                            discover_legacy: bool = True,
                            debug: bool = False) -> TemplateCollection:
        """
        Collect templates from all sources (legacy and plugins)
        すべてのソース（レガシーとプラグイン）からテンプレートを収集
        """
        collection = TemplateCollection()
        
        # Collect legacy templates
        if discover_legacy:
            legacy_templates = self.discover_legacy_templates(debug)
            for template in legacy_templates:
                collection.add_template(template)
        
        # Collect plugin templates
        if discover_plugins:
            plugin_templates = self.discover_entry_point_templates(debug)
            for template in plugin_templates:
                collection.add_template(template)
        
        # Validate all templates
        validation_errors = collection.validate_all_templates()
        if validation_errors and debug:
            print("Template validation errors:")
            for error in validation_errors:
                print(f"  - {error}")
        
        return collection
    
    def generate_env_example_content(self, 
                                   discover_plugins: bool = True,
                                   discover_legacy: bool = True,
                                   debug: bool = False) -> str:
        """
        Generate .env.example content with enhanced template processing
        拡張されたテンプレート処理で.env.exampleコンテンツを生成
        """
        if debug:
            print("\nDiscovering templates from all sources...")
        
        # Collect all templates
        collection = self.collect_all_templates(discover_plugins, discover_legacy, debug)
        
        if debug:
            legacy_count = len(self._legacy_registry) if discover_legacy else 0
            plugin_count = len(collection.templates) - legacy_count if discover_plugins else 0
            
            print(f"\nTemplate sources:")
            print(f"  - Legacy decorator functions: {legacy_count}")
            print(f"  - Plugin entry-point functions: {plugin_count}")
            
            # Report duplicates
            duplicates = collection.get_duplicate_variables()
            if duplicates:
                print(f"\nDuplicate variables found:")
                for var_name, sources in duplicates.items():
                    print(f"  - {var_name}: {', '.join(sources)}")
            print("")
        
        # Get grouped variables organized by importance and group
        grouped_variables = collection.get_grouped_variables()
        
        # Generate content
        lines = []
        lines.append("# Auto-generated by OneEnv")
        lines.append("")
        
        # Process by importance levels
        importance_levels = ["critical", "important", "optional"]
        
        for importance in importance_levels:
            if not grouped_variables[importance]:
                continue
                
            # Add importance section header based on locale
            importance_headers = self._get_importance_headers()
            lines.append(importance_headers[importance])
            lines.append("")
            
            # Sort groups alphabetically within each importance level
            sorted_groups = sorted(grouped_variables[importance].items())
            
            for group_name, group_vars in sorted_groups:
                # Add group header if there are multiple groups or it's not "General"
                if len(sorted_groups) > 1 or group_name != "General":
                    lines.append(f"# ----- {group_name} -----")
                    lines.append("")
                
                # Sort variables within group alphabetically
                sorted_vars = sorted(group_vars.items())
                
                for var_name, info in sorted_vars:
                    config = info["config"]
                    sources = info["sources"]
                    
                    # Add source information
                    sources_str = ", ".join(sorted(sources))
                    lines.append(f"# (Defined in: {sources_str})")
                    
                    # Use Pydantic model attributes
                    description = config.description
                    default_value = config.default
                    required_value = config.required
                    choices_value = config.choices
                    
                    # Add description lines (now includes merged descriptions from all sources)
                    for line in description.splitlines():
                        stripped_line = line.strip()
                        if stripped_line:
                            # Skip source attribution lines that start with "# From"
                            if not stripped_line.startswith("# From "):
                                lines.append(f"# {stripped_line}")
                            else:
                                # Add source attribution as-is
                                lines.append(f"{stripped_line}")
                    
                    # Add required marker
                    if required_value:
                        lines.append("# Required")
                    
                    # Add choices
                    if choices_value:
                        lines.append(f"# Choices: {', '.join(choices_value)}")
                    
                    # Add variable assignment
                    lines.append(f"{var_name}={default_value}")
                    lines.append("")
                
                # Add extra space between groups
                if len(sorted_groups) > 1:
                    lines.append("")
        
        return "\n".join(lines)
    
    def get_legacy_compatible_templates(self) -> Dict[str, Dict[str, Any]]:
        """
        Return templates in legacy dictionary format for backward compatibility
        後方互換性のためにレガシー辞書形式でテンプレートを返す
        """
        collection = self.collect_all_templates()
        merged_variables = collection.get_merged_variables()
        
        legacy_format = {}
        for var_name, info in merged_variables.items():
            legacy_format[var_name] = {
                "config": env_var_config_to_dict(info["config"]),
                "sources": info["sources"]
            }
        
        return legacy_format


# Global instance for compatibility with existing API
_oneenv_core = OneEnvCore()

# Decorator for legacy compatibility
def oneenv(func: Callable) -> Callable:
    """
    Legacy decorator for registering template functions
    テンプレート関数を登録するレガシーデコレータ
    """
    return _oneenv_core.register_legacy_function(func)

# Enhanced functions that use the new core
def collect_templates_enhanced(debug: bool = False) -> Dict[str, Dict[str, Any]]:
    """Enhanced version of collect_templates using Pydantic models"""
    return _oneenv_core.get_legacy_compatible_templates()

def template_enhanced(debug: bool = False) -> str:
    """Enhanced version of template generation using Pydantic models"""
    return _oneenv_core.generate_env_example_content(debug=debug)

def report_duplicates_enhanced(debug: bool = False) -> None:
    """Enhanced version of duplicate reporting"""
    collection = _oneenv_core.collect_all_templates(debug=debug)
    duplicates = collection.get_duplicate_variables()
    
    for var_name, sources in duplicates.items():
        print(f"Warning: Duplicate key '{var_name}' defined in {', '.join(sources)}")

# Export the global registry for backward compatibility
def get_template_registry() -> List[Callable]:
    """Get the legacy template function registry"""
    return _oneenv_core._legacy_registry

def clear_template_registry() -> None:
    """Clear the legacy template function registry (useful for testing)"""
    _oneenv_core._legacy_registry.clear()


# ==========================================
# Scaffolding API Implementation
# ==========================================

class ScaffoldingTemplateProcessor:
    """
    Scaffolding形式専用のテンプレート処理
    """
    
    def __init__(self, entry_point_group: str = "oneenv.templates"):
        self.entry_point_group = entry_point_group
        self.env_options: List[EnvOption] = []
    
    def load_all_scaffolding_templates(self, debug: bool = False) -> None:
        """
        インストールされた全パッケージからScaffolding形式テンプレートを読み込み
        """
        self.env_options.clear()
        
        try:
            template_eps = entry_points(group=self.entry_point_group)
            
            for ep in template_eps:
                try:
                    # Load the entry-point function
                    template_func = ep.load()
                    
                    # Call the function to get template data
                    template_data = template_func()
                    
                    # Scaffolding形式のみ受け入れ
                    validate_scaffolding_format(template_data)
                    
                    # EnvOptionリストに変換
                    options = scaffolding_template_function_to_env_options(ep.name, template_data)
                    self.env_options.extend(options)
                    
                    if debug:
                        print(f"✅ Loaded scaffolding template: {ep.name} ({len(options)} options)")
                        
                except Exception as e:
                    # 不正な形式は無視（ログ出力）
                    if debug:
                        print(f"⚠️  Skipping invalid template {ep.name}: {e}")
                        
        except Exception as e:
            if debug:
                print(f"❌ Error discovering template plugins: {e}")
    
    def get_template_structure(self) -> Dict[str, List[str]]:
        """
        カテゴリ別オプション構造を返却
        """
        structure = {}
        
        for option in self.env_options:
            category = option.category
            if category not in structure:
                structure[category] = []
            
            if option.option not in structure[category]:
                structure[category].append(option.option)
        
        # オプションをソート
        for category in structure:
            structure[category].sort()
        
        return structure
    
    def has_category(self, category: str) -> bool:
        """
        指定カテゴリの存在確認
        """
        return any(option.category == category for option in self.env_options)
    
    def get_options(self, category: str) -> List[str]:
        """
        カテゴリ内の全オプション取得
        """
        options = []
        for option in self.env_options:
            if option.category == category and option.option not in options:
                options.append(option.option)
        return sorted(options)
    
    def generate_by_selection(self, generation_range: List[Dict[str, str]]) -> Dict[str, Dict[str, Any]]:
        """
        選択範囲に基づいて環境変数を生成
        
        Returns:
            {
                "var_name": {
                    "config": EnvVarConfig,
                    "category": str,
                    "option": str
                }
            }
        """
        selected_vars = {}
        
        for selection in generation_range:
            category = selection["category"]
            option = selection.get("option")  # None = 全オプション
            
            for env_option in self.env_options:
                if env_option.category == category:
                    if option is None or env_option.option == option:
                        # 環境変数追加
                        for var_name, var_config in env_option.env.items():
                            # 同じ変数名が複数のオプションで定義されている場合、
                            # オプション名をプレフィックスとして追加
                            if option is None:  # 全オプション選択の場合
                                unique_var_name = f"{env_option.option.upper()}_{var_name}"
                            else:
                                unique_var_name = var_name
                            
                            selected_vars[unique_var_name] = {
                                "config": var_config,
                                "category": env_option.category,
                                "option": env_option.option
                            }
        
        return selected_vars


# Global scaffolding processor instance
_scaffolding_processor = ScaffoldingTemplateProcessor()


def get_all_template_structure() -> Dict[str, List[str]]:
    """
    全テンプレート構造をカテゴリ別オプション一覧で返却
    
    Returns:
        カテゴリ名をキー、オプション名のリストを値とする辞書
        
    Example:
        {
            "Database": ["sqlite", "postgres", "mysql"],
            "VectorStore": ["chroma", "weaviate", "pinecone"],
            "LLM": ["openai", "anthropic", "ollama"]
        }
    
    Raises:
        ImportError: entry-pointsの読み込みに失敗した場合
        ValueError: 不正なScaffolding形式テンプレートが見つかった場合
    """
    # テンプレートが既に読み込まれていない場合のみ読み込み
    if not _scaffolding_processor.env_options:
        _scaffolding_processor.load_all_scaffolding_templates()
    return _scaffolding_processor.get_template_structure()


def has_category(category: str) -> bool:
    """
    指定されたカテゴリが利用可能かどうかを確認
    
    Args:
        category: 確認するカテゴリ名（例: "Database", "VectorStore"）
        
    Returns:
        カテゴリが存在する場合True、存在しない場合False
        
    Example:
        >>> has_category("Database")
        True
        >>> has_category("NonExistent")
        False
    
    Raises:
        TypeError: categoryが文字列でない場合
        ValueError: categoryが空文字列の場合
    """
    if not isinstance(category, str):
        raise TypeError(f"Category must be string, got {type(category)}")
    
    if not category.strip():
        raise ValueError("Category cannot be empty")
    
    # テンプレートが既に読み込まれていない場合のみ読み込み
    if not _scaffolding_processor.env_options:
        _scaffolding_processor.load_all_scaffolding_templates()
    return _scaffolding_processor.has_category(category.strip())


def get_options(category: str) -> List[str]:
    """
    指定されたカテゴリ内の全オプション名を取得
    
    Args:
        category: 対象カテゴリ名（例: "Database"）
        
    Returns:
        オプション名のリスト（カテゴリが存在しない場合は空リスト）
        
    Example:
        >>> get_options("Database")
        ["sqlite", "postgres", "mysql"]
        >>> get_options("NonExistent")
        []
    
    Raises:
        TypeError: categoryが文字列でない場合
        ValueError: categoryが空文字列の場合または存在しないカテゴリの場合
    """
    if not isinstance(category, str):
        raise TypeError(f"Category must be string, got {type(category)}")
    
    if not category.strip():
        raise ValueError("Category cannot be empty")
    
    # テンプレートが既に読み込まれていない場合のみ読み込み
    if not _scaffolding_processor.env_options:
        _scaffolding_processor.load_all_scaffolding_templates()
    
    # カテゴリが存在しない場合、利用可能なカテゴリを提案
    if not _scaffolding_processor.has_category(category.strip()):
        available_categories = list(_scaffolding_processor.get_template_structure().keys())
        if available_categories:
            raise ValueError(f"Category '{category}' not found. Available categories: {', '.join(sorted(available_categories))}")
        else:
            raise ValueError(f"Category '{category}' not found. No scaffolding templates are currently available.")
    
    return _scaffolding_processor.get_options(category.strip())


def generate_env_file_content(variables: Dict[str, Dict[str, Any]]) -> str:
    """
    環境変数辞書から.envファイル内容を生成
    重要度（critical/important/optional）とカテゴリ/オプション別に分類
    
    Args:
        variables: {
            "var_name": {
                "config": EnvVarConfig,
                "category": str, 
                "option": str
            }
        }
    """
    lines = []
    
    # 重要度別にグループ化
    importance_groups = {"critical": {}, "important": {}, "optional": {}}
    
    for var_name, var_info in variables.items():
        config = var_info["config"]
        category = var_info.get("category", "General")
        option = var_info.get("option", "default")
        
        # 重要度を取得（デフォルトは"important"）
        importance = getattr(config, 'importance', 'important')
        
        # カテゴリ/オプション別のキー
        key = f"{category} ({option})"
        
        if key not in importance_groups[importance]:
            importance_groups[importance][key] = []
        importance_groups[importance][key].append((var_name, var_info))
    
    # 重要度レベル別に出力
    importance_levels = ["critical", "important", "optional"]
    
    for importance in importance_levels:
        if not importance_groups[importance]:
            continue
            
        # 重要度セクションヘッダー
        if importance == "critical":
            lines.append("# ========== CRITICAL: Essential Settings for Application Operation ==========")
        elif importance == "important":
            lines.append("# ========== IMPORTANT: Settings to Configure for Production Use ==========")
        else:  # optional
            lines.append("# ========== OPTIONAL: Fine-tuning Settings (Defaults are Sufficient) ==========")
        lines.append("")
        
        # カテゴリ/オプション別に出力
        for group_name, group_vars in sorted(importance_groups[importance].items()):
            lines.append(f"# ----- {group_name} -----")
            lines.append("")
            
            for var_name, var_info in sorted(group_vars):
                config = var_info["config"]
                
                # コメント行（説明）
                if hasattr(config, 'description') and config.description:
                    lines.append(f"# {config.description}")
                
                # 必須マーカー
                if hasattr(config, 'required') and config.required:
                    lines.append("# Required")
                
                # 選択肢
                if hasattr(config, 'choices') and config.choices:
                    lines.append(f"# Choices: {', '.join(config.choices)}")
                
                # 変数行
                default_value = getattr(config, 'default', '')
                lines.append(f"{var_name}={default_value}")
                lines.append("")
            
            lines.append("")  # グループ間の空行
    
    return "\n".join(lines)


def generate_template(dest: str, generation_range: List[Dict[str, str]]) -> str:
    """
    指定された選択範囲に基づいて.envテンプレートファイルを生成
    
    Args:
        dest: 出力先ファイルパス（空文字列の場合はファイル出力なし）
        generation_range: 生成範囲指定のリスト
            [
                {"category": "Database", "option": "postgres"},     # 特定オプション
                {"category": "VectorStore", "option": "chroma"},    # 特定オプション  
                {"category": "LLM"}                                 # 全オプション
            ]
    
    Returns:
        生成された.envファイルの内容（文字列）
    
    Raises:
        TypeError: 引数の型が不正な場合
        ValueError: generation_rangeの形式が不正な場合
        FileNotFoundError: destの親ディレクトリが存在しない場合
        PermissionError: destファイルに書き込み権限がない場合
    """
    # 引数検証
    if not isinstance(dest, str):
        raise TypeError(f"dest must be string, got {type(dest)}")
    
    if not isinstance(generation_range, list):
        raise TypeError(f"generation_range must be list, got {type(generation_range)}")
    
    # generation_range形式検証
    for i, selection in enumerate(generation_range):
        if not isinstance(selection, dict):
            raise ValueError(f"generation_range[{i}] must be dict, got {type(selection)}. Expected format: {{\"category\": \"CategoryName\", \"option\": \"OptionName\"}}")
        
        if "category" not in selection:
            raise ValueError(f"generation_range[{i}] missing required key 'category'. Expected format: {{\"category\": \"CategoryName\", \"option\": \"OptionName\"}}")
        
        if not isinstance(selection["category"], str) or not selection["category"].strip():
            raise ValueError(f"generation_range[{i}]['category'] must be non-empty string")
        
        if "option" in selection:
            if not isinstance(selection["option"], str) or not selection["option"].strip():
                raise ValueError(f"generation_range[{i}]['option'] must be non-empty string if provided")
    
    # テンプレート読み込み・生成
    # テンプレートが既に読み込まれていない場合のみ読み込み
    if not _scaffolding_processor.env_options:
        _scaffolding_processor.load_all_scaffolding_templates()
    
    # カテゴリ存在チェック
    available_categories = list(_scaffolding_processor.get_template_structure().keys())
    for i, selection in enumerate(generation_range):
        category = selection["category"].strip()
        if not _scaffolding_processor.has_category(category):
            if available_categories:
                raise ValueError(f"generation_range[{i}]: Category '{category}' not found. Available categories: {', '.join(sorted(available_categories))}")
            else:
                raise ValueError(f"generation_range[{i}]: Category '{category}' not found. No scaffolding templates are currently available.")
    
    selected_vars = _scaffolding_processor.generate_by_selection(generation_range)
    
    # .envファイル内容生成
    env_content = generate_env_file_content(selected_vars)
    
    # ファイル出力
    if dest.strip():
        try:
            # 親ディレクトリの存在確認
            import os
            parent_dir = os.path.dirname(dest)
            if parent_dir and not os.path.exists(parent_dir):
                raise FileNotFoundError(f"Parent directory does not exist: {parent_dir}")
            
            with open(dest, 'w', encoding='utf-8') as f:
                f.write(env_content)
        except (IOError, OSError) as e:
            raise PermissionError(f"Cannot write to file {dest}: {e}")
    
    return env_content