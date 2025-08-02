"""
OneEnv Information API
情報提供に特化したAPI関数群
"""

import json
from typing import Dict, List, Any, Union
from .core import _scaffolding_processor


def get_structure_info(json_format: bool = False) -> Union[str, Dict]:
    """
    利用可能なカテゴリ/オプション構造を取得
    
    Args:
        json_format: JSON形式で返却するかどうか
        
    Returns:
        構造情報（文字列またはDict）
    """
    # テンプレートが既に読み込まれていない場合のみ読み込み
    if not _scaffolding_processor.env_options:
        _scaffolding_processor.load_all_scaffolding_templates()
    structure = _scaffolding_processor.get_template_structure()
    
    if not structure:
        if json_format:
            return {
                "categories": {},
                "summary": {
                    "total_categories": 0,
                    "total_options": 0,
                    "total_variables": 0
                }
            }
        else:
            return "No scaffolding templates are currently available."
    
    # 変数数カウント
    variable_counts = {}
    total_variables = 0
    
    for category, options in structure.items():
        variable_counts[category] = {}
        for option in options:
            count = _count_variables_for_option(category, option)
            variable_counts[category][option] = count
            total_variables += count
    
    if json_format:
        return {
            "categories": {
                category: {
                    "options": options,
                    "variable_counts": variable_counts[category]
                }
                for category, options in structure.items()
            },
            "summary": {
                "total_categories": len(structure),
                "total_options": sum(len(options) for options in structure.values()),
                "total_variables": total_variables
            }
        }
    else:
        lines = ["Available Template Structure:"]
        
        for category, options in sorted(structure.items()):
            category_vars = sum(variable_counts[category].values())
            lines.append(f"├── {category}")
            
            for i, option in enumerate(sorted(options)):
                var_count = variable_counts[category][option]
                prefix = "└──" if i == len(options) - 1 else "├──"
                lines.append(f"│   {prefix} {option} ({var_count} variables)")
        
        lines.append("")
        lines.append(f"Total: {len(structure)} categories, "
                    f"{sum(len(options) for options in structure.values())} options, "
                    f"{total_variables} variables")
        
        return "\n".join(lines)


def get_category_info(category: str, json_format: bool = False) -> Union[str, Dict]:
    """
    カテゴリの詳細情報を取得
    
    Args:
        category: カテゴリ名
        json_format: JSON形式で返却するかどうか
        
    Returns:
        カテゴリ詳細情報（文字列またはDict）
        
    Raises:
        ValueError: カテゴリが存在しない場合
    """
    # テンプレートが既に読み込まれていない場合のみ読み込み
    if not _scaffolding_processor.env_options:
        _scaffolding_processor.load_all_scaffolding_templates()
    
    if not _scaffolding_processor.has_category(category):
        available_categories = list(_scaffolding_processor.get_template_structure().keys())
        if available_categories:
            raise ValueError(f"Category '{category}' not found. Available categories: {', '.join(sorted(available_categories))}")
        else:
            raise ValueError(f"Category '{category}' not found. No scaffolding templates are currently available.")
    
    options = _scaffolding_processor.get_options(category)
    
    # 各オプションの詳細情報を収集
    option_details = {}
    importance_counts = {"critical": 0, "important": 0, "optional": 0}
    
    for option in options:
        variables = _get_option_variables(category, option)
        option_details[option] = variables
        
        # 重要度カウント
        for var_config in variables.values():
            importance = getattr(var_config, 'importance', 'important')
            importance_counts[importance] += 1
    
    if json_format:
        return {
            "category": category,
            "options": {
                option: {
                    "variables": {
                        var_name: {
                            "description": var_config.description,
                            "required": var_config.required,
                            "importance": getattr(var_config, 'importance', 'important'),
                            "default": var_config.default,
                            "choices": var_config.choices
                        }
                        for var_name, var_config in variables.items()
                    }
                }
                for option, variables in option_details.items()
            },
            "summary": {
                "total_options": len(options),
                "total_variables": sum(len(vars) for vars in option_details.values()),
                "importance_counts": importance_counts
            }
        }
    else:
        lines = [f"Category: {category}"]
        lines.append("Description: Configuration options for " + category.lower())
        lines.append("")
        lines.append("Available Options:")
        
        for option in sorted(options):
            variables = option_details[option]
            lines.append(f"├── {option}")
            
            for var_name, var_config in sorted(variables.items()):
                required_str = "required" if var_config.required else "optional"
                importance = getattr(var_config, 'importance', 'important')
                lines.append(f"│   ├── {var_name} ({required_str}, {importance})")
        
        lines.append("")
        lines.append("Variables Summary:")
        lines.append(f"- Critical: {importance_counts['critical']} variables")
        lines.append(f"- Important: {importance_counts['important']} variables")
        lines.append(f"- Optional: {importance_counts['optional']} variables")
        
        return "\n".join(lines)


def get_option_preview(category: str, option: str) -> str:
    """
    特定オプションのプレビューを取得
    
    Args:
        category: カテゴリ名
        option: オプション名
        
    Returns:
        プレビュー文字列
        
    Raises:
        ValueError: カテゴリまたはオプションが存在しない場合
    """
    # テンプレートが既に読み込まれていない場合のみ読み込み
    if not _scaffolding_processor.env_options:
        _scaffolding_processor.load_all_scaffolding_templates()
    
    # カテゴリ存在チェック
    if not _scaffolding_processor.has_category(category):
        available_categories = list(_scaffolding_processor.get_template_structure().keys())
        if available_categories:
            raise ValueError(f"Category '{category}' not found. Available categories: {', '.join(sorted(available_categories))}")
        else:
            raise ValueError(f"Category '{category}' not found. No scaffolding templates are currently available.")
    
    # オプション存在チェック
    available_options = _scaffolding_processor.get_options(category)
    if option not in available_options:
        raise ValueError(f"Option '{option}' not found in category '{category}'. Available options: {', '.join(sorted(available_options))}")
    
    # テンプレート生成
    from .core import generate_template
    
    generation_range = [{"category": category, "option": option}]
    content = generate_template("", generation_range)
    
    lines = [f"Preview: {category} -> {option}", ""]
    lines.extend(content.split('\n'))
    
    return '\n'.join(lines)


def _count_variables_for_option(category: str, option: str) -> int:
    """特定オプションの変数数をカウント"""
    for env_option in _scaffolding_processor.env_options:
        if env_option.category == category and env_option.option == option:
            return len(env_option.env)
    return 0


def _get_option_variables(category: str, option: str) -> Dict[str, Any]:
    """特定オプションの変数一覧を取得"""
    for env_option in _scaffolding_processor.env_options:
        if env_option.category == category and env_option.option == option:
            return env_option.env
    return {}


def get_detailed_structure() -> Dict[str, Any]:
    """
    詳細な構造情報を取得（プログラマティック利用向け）
    
    Returns:
        詳細構造情報
    """
    # テンプレートが既に読み込まれていない場合のみ読み込み
    if not _scaffolding_processor.env_options:
        _scaffolding_processor.load_all_scaffolding_templates()
    structure = _scaffolding_processor.get_template_structure()
    
    categories_detail = {}
    total_variables = 0
    
    for category, options in structure.items():
        option_details = {}
        category_var_count = 0
        importance_dist = {"critical": 0, "important": 0, "optional": 0}
        
        for option in options:
            variables = _get_option_variables(category, option)
            var_count = len(variables)
            category_var_count += var_count
            
            # 重要度分布カウント
            for var_config in variables.values():
                importance = getattr(var_config, 'importance', 'important')
                importance_dist[importance] += 1
            
            option_details[option] = {
                "variable_count": var_count,
                "variables": list(variables.keys())
            }
        
        categories_detail[category] = {
            "options": options,
            "option_details": option_details,
            "total_variables": category_var_count,
            "importance_distribution": importance_dist
        }
        
        total_variables += category_var_count
    
    return {
        "categories": categories_detail,
        "metadata": {
            "total_categories": len(structure),
            "total_options": sum(len(options) for options in structure.values()),
            "total_variables": total_variables
        }
    }