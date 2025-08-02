import difflib
import sys
import os
import pkgutil
import importlib
from abc import ABC, abstractmethod

from dotenv import load_dotenv as dotenv_load_dotenv  # English: Import load_dotenv from python-dotenv.
                                                    # Japanese: python-dotenvからload_dotenvをインポートします。
from dotenv import dotenv_values as _dotenv_values  # English: Import dotenv_values from python-dotenv.
                                                   # Japanese: python-dotenvからdotenv_valuesをインポートします。

# Import new enhanced system
from .core import (
    template_enhanced, 
    collect_templates_enhanced, 
    report_duplicates_enhanced,
    oneenv as oneenv_decorator_enhanced,
    _oneenv_core,
    # New Scaffolding API
    get_all_template_structure,
    has_category,
    get_options,
    generate_template
)

# Import info API for advanced usage
from .info_api import (
    get_structure_info,
    get_category_info, 
    get_option_preview,
    get_detailed_structure
)

# Global registry for template functions  # English: Global registry for storing functions decorated with @oneenv.
                                           # Japanese: @oneenvデコレータが付与された関数を格納するグローバルレジストリ。
_TEMPLATE_REGISTRY = []

def oneenv(func):
    """
    English: Decorator that registers a function providing environment variable templates.
    Input:
      - func: The function that returns a dictionary of environment variable settings.
    Output:
      - The original function with the side-effect of being registered.
    Japanese: 環境変数テンプレートを提供する関数を登録するデコレータです。
    入力:
      - func: 環境変数設定の辞書を返す関数。
    出力:
      - 登録の副作用を持ち、元の関数を返します。
    """
    # Register the function in both legacy and new registries
    _TEMPLATE_REGISTRY.append(func)
    oneenv_decorator_enhanced(func)
    return func

class OneEnv(ABC):
    """
    English: Abstract base class for defining environment variable templates.
    Japanese: 環境変数テンプレートを定義するための抽象基本クラスです。
    """
    @abstractmethod
    def get_template(self) -> dict:
        """
        English: Returns the template dictionary for environment variables.
        Japanese: 環境変数のテンプレート辞書を返します。
        """
        pass

def collect_templates():
    """
    English: Collects and combines environment variable templates from registered functions.
    Returns a dictionary mapping keys to their configuration and list of sources (function names).
    Now enhanced with Pydantic models and entry-points support.
    Output format:
       { key: { "config": { ... }, "sources": [func_name, ...] }, ... }
    Japanese: 登録された関数から環境変数テンプレートを収集し、統合します。
    各キーに対して、その設定情報と定義元の関数名リストを含む辞書を返します。
    Pydanticモデルとentry-pointsサポートで拡張されました。
    出力形式:
       { key: { "config": { ... }, "sources": [関数名, ...] }, ... }
    """
    # Use enhanced collection with both legacy and plugin support
    return collect_templates_enhanced()

def report_duplicates():
    """
    English: Reports duplicate environment variable keys across multiple templates.
             Prints warnings if duplicate keys are found.
             Now enhanced with Pydantic models and entry-points support.
    Japanese: 複数のテンプレート間で重複している環境変数のキーを検出し、警告を出力します。
             Pydanticモデルとentry-pointsサポートで拡張されました。
    """
    # Use enhanced duplicate reporting
    report_duplicates_enhanced()

def template(debug=False):
    """
    English: Generates the text content of the .env.example file based on collected templates.
             Each variable includes its description, source, and default value.
             Now enhanced with Pydantic models and entry-points support.
    Output:
      - A string with the content for .env.example.
    Japanese: 収集したテンプレートに基づいて、.env.exampleファイルのテキスト内容を生成します。
             各環境変数は説明、定義元の関数、既定値を含みます。
             Pydanticモデルとentry-pointsサポートで拡張されました。
    出力:
      - .env.example用の内容を持つ文字列を返します。
    """
    # Use the enhanced template generation system
    # Import all modules to discover @oneenv decorated functions (legacy support)
    imported_modules = import_templates(debug)
    
    # Use enhanced template generation with both legacy and plugin support
    return template_enhanced(debug)

def diff(previous_text, current_text):
    """
    English: Compares two .env.example texts and returns a diff string showing additions and modifications.
             For a modified line, displays the change in the format: "~ old_line → new_line".
    Input:
      - previous_text: The previous .env.example content.
      - current_text: The current .env.example content.
    Output:
      - A string representing the differences.
    Japanese: 2つの.env.exampleファイルのテキストを比較し、追加および変更箇所を示すdiff文字列を返します。
             変更箇所は "~ 古い行 → 新しい行" の形式で表示されます。
    入力:
      - previous_text: 以前の.env.exampleの内容
      - current_text: 現在の.env.exampleの内容
    出力:
      - 差分を表す文字列を返します。
    """
    previous_lines = previous_text.splitlines()
    current_lines = current_text.splitlines()
    differ = difflib.Differ()
    diff_list = list(differ.compare(previous_lines, current_lines))
    result_lines = []
    i = 0
    # English: Iterate over the diff list to process removals and additions.
    # Japanese: diffリストを反復し、削除と追加の行を処理します。
    while i < len(diff_list):
        line = diff_list[i]
        if line.startswith("- "):
            # English: Check if the next line is an addition to combine as a modification.
            # Japanese: 次の行が追加であれば、変更として結合します。
            if i + 1 < len(diff_list) and diff_list[i + 1].startswith("+ "):
                old_line = line[2:]
                new_line = diff_list[i + 1][2:]
                if not old_line.startswith("#") and "=" in old_line:
                    result_lines.append(f"~ {old_line} → {new_line}")
                    i += 2
                    continue
            result_lines.append(f"- {line[2:]}")
        elif line.startswith("+ "):
            result_lines.append(f"+ {line[2:]}")
        i += 1
    return "\n".join(result_lines)

def generate_env_example(output_path, debug=False):
    """
    English: Generates the .env.example file at the specified output path using the current templates.
    Input:
      - output_path: The file path where the .env.example should be written.
      - debug: Enable debug output (default: False)
    Japanese: 現在のテンプレートを用いて、指定された出力パスに.env.exampleファイルを生成します。
    入力:
      - output_path: .env.exampleを書き込むファイルパス
      - debug: デバッグ出力を有効にする（デフォルト: False）
    """
    content = template(debug=debug)
    # English: Write the generated content to the specified file.
    # Japanese: 生成された内容を指定されたファイルに書き込みます。
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(content)

def load_dotenv(dotenv_path=None, override=False):
    """
    English: Loads environment variables from a .env file using python-dotenv.
    Input:
      - dotenv_path: The path to the .env file (optional).
      - override: Whether to override existing environment variables (default False).
    Output:
      - Returns a boolean indicating success.
    Japanese: python-dotenvを使用して、.envファイルから環境変数を読み込みます。
    入力:
      - dotenv_path: .envファイルへのパス（オプション）
      - override: 既存の環境変数を上書きするかどうか（デフォルトはFalse）
    出力:
      - 成功を示すブール値を返します。
    """
    return dotenv_load_dotenv(dotenv_path=dotenv_path, override=override)

def dotenv_values(dotenv_path=None, encoding='utf-8'):
    """
    English: Returns the environment variables from a .env file as a dictionary using python-dotenv.
    Input:
      - dotenv_path: The path to the .env file (optional).
      - encoding: The encoding for reading the .env file (default 'utf-8').
    Output:
      - A dictionary containing the environment variables.
    Japanese: python-dotenvを使用して、.envファイルから環境変数を辞書形式で返します。
    入力:
      - dotenv_path: .envファイルへのパス（オプション）
      - encoding: .envファイルを読み込む際のエンコーディング（デフォルトは'utf-8'）
    出力:
      - 環境変数が格納された辞書を返します。
    """
    return _dotenv_values(dotenv_path=dotenv_path, encoding=encoding)

def set_key(dotenv_path, key_to_set, value_to_set):
    """
    English: Sets or updates an environment variable in the specified .env file.
    Input:
      - dotenv_path: The path to the .env file.
      - key_to_set: The environment variable name to set.
      - value_to_set: The value to assign to the environment variable.
    Japanese: 指定された.envファイルに対して、環境変数の値を設定または更新します。
    入力:
      - dotenv_path: .envファイルへのパス
      - key_to_set: 設定する環境変数の名前
      - value_to_set: 環境変数に割り当てる値
    """
    try:
        # English: Attempt to read the existing .env file.
        # Japanese: 既存の.envファイルを読み込もうと試みます。
        with open(dotenv_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        # English: If not found, start with an empty list.
        # Japanese: ファイルが見つからない場合、空のリストから開始します。
        lines = []
    key_prefix = f"{key_to_set}="
    found = False
    new_lines = []
    # English: Iterate through each line and update the target key if it exists.
    # Japanese: 各行を処理し、対象のキーが存在する場合は更新します。
    for line in lines:
        if line.startswith(key_prefix):
            new_lines.append(f"{key_to_set}={value_to_set}\n")
            found = True
        else:
            new_lines.append(line)
    if not found:
        # English: If key is not present, append it.
        # Japanese: キーが存在しない場合、新たに追加します。
        new_lines.append(f"{key_to_set}={value_to_set}\n")
    # English: Write the updated content back to the .env file.
    # Japanese: 更新された内容を.envファイルに書き戻します。
    with open(dotenv_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

def unset_key(dotenv_path, key_to_unset):
    """
    English: Removes an environment variable from the specified .env file.
    Input:
      - dotenv_path: The path to the .env file.
      - key_to_unset: The environment variable name to remove.
    Japanese: 指定された.envファイルから環境変数を削除します。
    入力:
      - dotenv_path: .envファイルへのパス
      - key_to_unset: 削除する環境変数の名前
    """
    try:
        # English: Attempt to read the existing .env file.
        # Japanese: 既存の.envファイルを読み込もうと試みます。
        with open(dotenv_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        # English: If the file is not found, there is nothing to remove.
        # Japanese: ファイルが存在しなければ、削除する内容はありません。
        lines = []
    new_lines = []
    key_prefix = f"{key_to_unset}="
    # English: Exclude the line corresponding to the specified key.
    # Japanese: 指定されたキーに該当する行を除外します。
    for line in lines:
        if not line.startswith(key_prefix):
            new_lines.append(line)
    # English: Write the filtered content back to the .env file.
    # Japanese: フィルタリングされた内容を.envファイルに書き戻します。
    with open(dotenv_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

# 新規: sys.path 内のモジュールを自動探索・インポートする仕組み
# New: Automatically discover and import modules in sys.path to trigger the @oneenv decorators.
def import_templates(debug=False):
    """
    English: Automatically discovers and imports modules within directories under the current working directory in sys.path.
    This triggers the registration of all functions decorated with @oneenv.
    Japanese: 現在の作業ディレクトリ以下にあるsys.path上のディレクトリ内のモジュールを自動探索・インポートします。
    これにより、@oneenvデコレータが付与されたすべての関数が登録されることを保証します。
    Output:
      - A list of successfully imported module names.
      - 登録に成功したモジュール名のリストを返します。
    """

    cwd = os.getcwd()  # English: Get the current working directory.
                      # Japanese: 現在の作業ディレクトリを取得します。
    imported_modules = []
    for path_item in sys.path:
        abs_path = os.path.abspath(path_item)
        if not os.path.isdir(abs_path):
            continue
        # Restrict search to directories under the current working directory to avoid system libraries.
        # 現在の作業ディレクトリ下にあるディレクトリに限定して探索し、システムライブラリを除外します。
        if not abs_path.startswith(cwd):
            continue
        for finder, modname, ispkg in pkgutil.iter_modules([abs_path]):
            try:
                importlib.import_module(modname)
                imported_modules.append(modname)
                if debug:
                    print(f"Imported module: {modname}")
            except Exception as e:
                print(f"OneEnv import_templates: Could not import module {modname} from {abs_path}: {e}")
    return imported_modules

def import_all_modules(package, debug=False):
    """
    English: Import all modules in the given package.
    Japanese: 指定されたパッケージ内のすべてのモジュールをインポートします。
    """
    import pkgutil
    import importlib
    imported = []
    if hasattr(package, '__path__'):
        for finder, module_name, ispkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
            try:
                importlib.import_module(module_name)
                imported.append(module_name)
                if debug:
                    print(f"Imported module: {module_name}")
            except Exception as e:
                print(f"Error importing module {module_name}: {e}")
    return imported


# Named environment system
class NamedEnvironment:
    """
    English: Named environment instance that manages environment variables with namespacing.
    Japanese: 環境変数を名前空間で管理する名前付き環境インスタンスです。
    """
    
    def __init__(self, name=None):
        """
        English: Initialize named environment.
        Input:
          - name: Environment name (None for common environment)
        Japanese: 名前付き環境を初期化します。
        入力:
          - name: 環境名（共通環境の場合はNone）
        """
        self.name = name
        self._env_vars = {}
    
    def load_dotenv(self, dotenv_path=None, override=False):
        """
        English: Load environment variables from a .env file into this named environment.
        Input:
          - dotenv_path: Path to the .env file
          - override: Whether to override existing variables
        Output:
          - Returns True if successful
        Japanese: .envファイルから環境変数をこの名前付き環境に読み込みます。
        入力:
          - dotenv_path: .envファイルへのパス
          - override: 既存の変数を上書きするかどうか
        出力:
          - 成功した場合Trueを返します
        """
        if dotenv_path is None:
            return False
        
        try:
            # Check if file exists first
            if not os.path.exists(dotenv_path):
                return False
            
            env_values = _dotenv_values(dotenv_path=dotenv_path)
            if env_values is None:
                return False
            if override:
                self._env_vars = env_values.copy()
            else:
                for key, value in env_values.items():
                    if key not in self._env_vars:
                        self._env_vars[key] = value
            return True
        except Exception:
            return False
    
    def get(self, key, default=None):
        """
        English: Get environment variable value with fallback logic.
        For named environments, falls back to common environment if not found.
        Input:
          - key: Environment variable name
          - default: Default value if not found
        Output:
          - Environment variable value or default
        Japanese: 環境変数の値をフォールバック論理で取得します。
        名前付き環境の場合、見つからなければ共通環境にフォールバックします。
        入力:
          - key: 環境変数名
          - default: 見つからない場合のデフォルト値
        出力:
          - 環境変数の値またはデフォルト値
        """
        # First check this environment's variables
        if key in self._env_vars:
            return self._env_vars[key]
        
        # For named environments, fall back to common environment
        if self.name is not None:
            common_env = _get_common_environment()
            if key in common_env._env_vars:
                return common_env._env_vars[key]
        
        # Finally, check OS environment variables
        return os.environ.get(key, default)


# Global registry for named environments
_named_environments = {}


def _get_common_environment():
    """
    English: Get or create the common environment instance.
    Japanese: 共通環境インスタンスを取得または作成します。
    """
    if None not in _named_environments:
        _named_environments[None] = NamedEnvironment(None)
    return _named_environments[None]


def env(name=None):
    """
    English: Get or create a named environment instance.
    Input:
      - name: Environment name (None for common environment)
    Output:
      - NamedEnvironment instance
    Japanese: 名前付き環境インスタンスを取得または作成します。
    入力:
      - name: 環境名（共通環境の場合はNone）
    出力:
      - NamedEnvironment インスタンス
    """
    if name not in _named_environments:
        _named_environments[name] = NamedEnvironment(name)
    return _named_environments[name]
 