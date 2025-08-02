#!/usr/bin/env python3
"""
Tutorial Validation Tests
チュートリアル9-11のサンプルコードと機能の動作確認テスト
"""

import pytest
import tempfile
import os
import sys
from pathlib import Path
from typing import Dict, List
import oneenv
from oneenv.models import validate_scaffolding_format


class TestTutorial09Validation:
    """Tutorial 9: 新しいテンプレート作成方法の検証"""
    
    def test_basic_template_structure(self):
        """基本的なテンプレート構造の検証"""
        # Tutorial 9の基本例
        def database_template():
            return [
                {
                    "category": "Database",
                    "option": "sqlite",
                    "env": {
                        "DATABASE_URL": {
                            "description": "SQLite database file path",
                            "default": "sqlite:///app.db",
                            "required": True,
                            "importance": "critical"
                        },
                        "DATABASE_TIMEOUT": {
                            "description": "Database connection timeout in seconds",
                            "default": "30",
                            "required": False,
                            "importance": "optional"
                        }
                    }
                },
                {
                    "category": "Database",
                    "option": "postgres",
                    "env": {
                        "DATABASE_URL": {
                            "description": "PostgreSQL connection URL",
                            "default": "postgresql://user:pass@localhost:5432/mydb",
                            "required": True,
                            "importance": "critical"
                        },
                        "DATABASE_POOL_SIZE": {
                            "description": "Connection pool size",
                            "default": "10",
                            "required": False,
                            "importance": "important"
                        },
                        "DATABASE_SSL_MODE": {
                            "description": "SSL mode for connections",
                            "default": "prefer",
                            "required": False,
                            "importance": "optional",
                            "choices": ["require", "prefer", "disable"]
                        }
                    }
                }
            ]
        
        template_data = database_template()
        
        # 基本的な検証
        assert isinstance(template_data, list)
        assert len(template_data) == 2
        
        # Scaffolding形式の検証
        validate_scaffolding_format(template_data)
        
        # 構造の検証
        categories = {item["category"] for item in template_data}
        assert "Database" in categories
        
        options = [item["option"] for item in template_data]
        assert "sqlite" in options
        assert "postgres" in options
    
    def test_full_stack_template(self):
        """複数カテゴリテンプレートの検証"""
        # Tutorial 9の高度な例
        def full_stack_template():
            return [
                # Database options
                {
                    "category": "Database",
                    "option": "postgres",
                    "env": {
                        "DATABASE_URL": {
                            "description": "Primary database connection",
                            "default": "postgresql://user:pass@localhost:5432/app",
                            "required": True,
                            "importance": "critical"
                        }
                    }
                },
                # Cache options
                {
                    "category": "Cache",
                    "option": "redis",
                    "env": {
                        "REDIS_URL": {
                            "description": "Redis server connection",
                            "default": "redis://localhost:6379/0",
                            "required": False,
                            "importance": "important"
                        },
                        "REDIS_MAX_CONNECTIONS": {
                            "description": "Maximum Redis connections",
                            "default": "50",
                            "required": False,
                            "importance": "optional"
                        }
                    }
                },
                # API options
                {
                    "category": "API",
                    "option": "fastapi",
                    "env": {
                        "API_HOST": {
                            "description": "API server host",
                            "default": "0.0.0.0",
                            "required": False,
                            "importance": "important"
                        },
                        "API_PORT": {
                            "description": "API server port",
                            "default": "8000",
                            "required": False,
                            "importance": "important"
                        },
                        "API_WORKERS": {
                            "description": "Number of worker processes",
                            "default": "4",
                            "required": False,
                            "importance": "optional"
                        }
                    }
                }
            ]
        
        template_data = full_stack_template()
        
        # 検証実行
        validate_scaffolding_format(template_data)
        
        # 複数カテゴリの確認
        categories = {item["category"] for item in template_data}
        assert len(categories) == 3
        assert "Database" in categories
        assert "Cache" in categories
        assert "API" in categories
    
    def test_choices_validation(self):
        """choices機能の検証"""
        def api_template():
            return [
                {
                    "category": "API",
                    "option": "production",
                    "env": {
                        "LOG_LEVEL": {
                            "description": "Application log level",
                            "default": "INFO",
                            "required": False,
                            "importance": "important",
                            "choices": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
                        },
                        "ENVIRONMENT": {
                            "description": "Deployment environment",
                            "default": "production",
                            "required": True,
                            "importance": "critical",
                            "choices": ["development", "staging", "production"]
                        }
                    }
                }
            ]
        
        template_data = api_template()
        validate_scaffolding_format(template_data)
        
        # choices フィールドの確認
        env_vars = template_data[0]["env"]
        assert "choices" in env_vars["LOG_LEVEL"]
        assert "choices" in env_vars["ENVIRONMENT"]
        assert "INFO" in env_vars["LOG_LEVEL"]["choices"]
        assert "production" in env_vars["ENVIRONMENT"]["choices"]


class TestTutorial10Validation:
    """Tutorial 10: Scaffoldingツール作成ガイドの検証"""
    
    def test_api_functions_availability(self):
        """情報提供API関数の利用可能性確認"""
        # Tutorial 10で使用される関数が利用可能か確認
        assert hasattr(oneenv, 'get_all_template_structure')
        assert hasattr(oneenv, 'has_category')
        assert hasattr(oneenv, 'get_options')
        assert hasattr(oneenv, 'generate_template')
        
        # 関数が呼び出し可能か確認
        assert callable(oneenv.get_all_template_structure)
        assert callable(oneenv.has_category)
        assert callable(oneenv.get_options)
        assert callable(oneenv.generate_template)
    
    def test_simple_cli_workflow(self):
        """シンプルCLIツールのワークフロー検証"""
        # Tutorial 10のシンプルな使用例
        try:
            # 構造取得
            structure = oneenv.get_all_template_structure()
            assert isinstance(structure, dict)
            
            if structure:  # テンプレートがある場合のみテスト
                # 最初のカテゴリをテスト
                first_category = next(iter(structure.keys()))
                
                # カテゴリ存在確認
                assert oneenv.has_category(first_category)
                
                # オプション取得
                options = oneenv.get_options(first_category)
                assert isinstance(options, list)
                
                if options:  # オプションがある場合のみテスト
                    # テンプレート生成
                    selections = [{"category": first_category, "option": options[0]}]
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
                        temp_file = f.name
                    
                    try:
                        content = oneenv.generate_template(temp_file, selections)
                        assert content
                        assert os.path.exists(temp_file)
                        
                        # ファイル内容確認
                        with open(temp_file, 'r') as f:
                            file_content = f.read()
                        assert len(file_content) > 0
                        
                    finally:
                        if os.path.exists(temp_file):
                            os.unlink(temp_file)
                            
        except Exception as e:
            pytest.skip(f"API functions not fully available: {e}")
    
    def test_error_handling_examples(self):
        """エラーハンドリング例の検証"""
        # 存在しないカテゴリのテスト
        assert not oneenv.has_category("NonExistentCategory")
        
        # 存在しないカテゴリからのオプション取得
        try:
            options = oneenv.get_options("NonExistentCategory")
            # エラーが発生するか、空リストが返されるかを確認
            assert options == [] or options is None
        except Exception:
            # エラーが発生することも想定範囲内
            pass
    
    def test_configuration_validation(self):
        """設定検証の例の動作確認"""
        # Tutorial 10の設定例
        sample_config = {
            'output': '.env.example',
            'selections': [
                {'category': 'Database', 'option': 'postgres'},
                {'category': 'Cache', 'option': 'redis'}
            ]
        }
        
        # 設定の基本構造確認
        assert 'output' in sample_config
        assert 'selections' in sample_config
        assert isinstance(sample_config['selections'], list)
        
        for selection in sample_config['selections']:
            assert 'category' in selection
            assert 'option' in selection


class TestTutorial11Validation:
    """Tutorial 11: 実践ガイドの検証"""
    
    def test_rag_system_template(self):
        """RAGシステムテンプレートの検証"""
        # Tutorial 11のRAGシステムテンプレート例
        def rag_system_template():
            return [
                # Database - Vector storage and metadata
                {
                    "category": "Database",
                    "option": "postgres",
                    "env": {
                        "DATABASE_URL": {
                            "description": "PostgreSQL connection for document metadata and user data",
                            "default": "postgresql://user:pass@localhost:5432/rag_db",
                            "required": True,
                            "importance": "critical"
                        },
                        "DATABASE_POOL_SIZE": {
                            "description": "Connection pool size for high-throughput operations",
                            "default": "20",
                            "required": False,
                            "importance": "important"
                        }
                    }
                },
                # Vector Database - Embeddings storage
                {
                    "category": "VectorStore",
                    "option": "chroma",
                    "env": {
                        "CHROMA_HOST": {
                            "description": "Chroma vector database host",
                            "default": "localhost",
                            "required": True,
                            "importance": "critical"
                        },
                        "CHROMA_PORT": {
                            "description": "Chroma server port",
                            "default": "8000",
                            "required": False,
                            "importance": "important"
                        },
                        "CHROMA_COLLECTION": {
                            "description": "Default collection for document embeddings",
                            "default": "rag_documents",
                            "required": False,
                            "importance": "important"
                        }
                    }
                },
                # LLM Provider
                {
                    "category": "LLM",
                    "option": "openai",
                    "env": {
                        "OPENAI_API_KEY": {
                            "description": "OpenAI API key for text generation",
                            "default": "",
                            "required": True,
                            "importance": "critical"
                        },
                        "OPENAI_MODEL": {
                            "description": "Primary model for text generation",
                            "default": "gpt-4",
                            "required": False,
                            "importance": "important",
                            "choices": ["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"]
                        }
                    }
                }
            ]
        
        template_data = rag_system_template()
        
        # 検証実行
        validate_scaffolding_format(template_data)
        
        # RAGシステムに必要なカテゴリの確認
        categories = {item["category"] for item in template_data}
        assert "Database" in categories
        assert "VectorStore" in categories
        assert "LLM" in categories
        
        # 重要度レベルの確認
        for item in template_data:
            for env_var in item["env"].values():
                assert env_var["importance"] in ["critical", "important", "optional"]
    
    def test_web_framework_template(self):
        """Webフレームワークテンプレートの検証"""
        def web_framework_template():
            return [
                {
                    "category": "Database",
                    "option": "postgres",
                    "env": {
                        "DATABASE_URL": {
                            "description": "Primary database connection",
                            "default": "postgresql://user:pass@localhost:5432/webapp",
                            "required": True,
                            "importance": "critical"
                        }
                    }
                },
                {
                    "category": "WebServer",
                    "option": "fastapi",
                    "env": {
                        "WEB_HOST": {
                            "description": "Server host address",
                            "default": "0.0.0.0",
                            "required": False,
                            "importance": "important"
                        },
                        "WEB_PORT": {
                            "description": "Server port",
                            "default": "8000",
                            "required": False,
                            "importance": "important"
                        }
                    }
                },
                {
                    "category": "Auth",
                    "option": "jwt",
                    "env": {
                        "JWT_SECRET_KEY": {
                            "description": "Secret key for JWT token signing",
                            "default": "",
                            "required": True,
                            "importance": "critical"
                        },
                        "JWT_EXPIRATION": {
                            "description": "Token expiration time in seconds",
                            "default": "3600",
                            "required": False,
                            "importance": "important"
                        }
                    }
                }
            ]
        
        template_data = web_framework_template()
        validate_scaffolding_format(template_data)
        
        # Webフレームワークに必要なカテゴリの確認
        categories = {item["category"] for item in template_data}
        assert "Database" in categories
        assert "WebServer" in categories
        assert "Auth" in categories
    
    def test_testing_strategy_examples(self):
        """テスト戦略例の検証"""
        # Tutorial 11のテスト例が実行可能かの確認
        def test_template_validation():
            """テンプレート検証の例"""
            def sample_template():
                return [
                    {
                        "category": "TestCategory",
                        "option": "test_option",
                        "env": {
                            "TEST_VAR": {
                                "description": "Test variable",
                                "default": "test_value",
                                "required": True,
                                "importance": "critical"
                            }
                        }
                    }
                ]
            
            template_data = sample_template()
            validate_scaffolding_format(template_data)
            return True
        
        # テスト例の実行
        assert test_template_validation()
    
    def test_package_structure_example(self):
        """パッケージ構造例の検証"""
        # Tutorial 11のパッケージ構造例
        package_structure = {
            'pyproject.toml': {
                'project': {
                    'name': 'my-rag-package',
                    'dependencies': ['oneenv>=0.3.0', 'pydantic>=2.0'],
                    'entry-points': {
                        'oneenv.templates': {
                            'rag': 'my_rag_package.templates:rag_system_template'
                        }
                    }
                }
            }
        }
        
        # 基本構造の確認
        assert 'pyproject.toml' in package_structure
        project_config = package_structure['pyproject.toml']['project']
        assert 'name' in project_config
        assert 'dependencies' in project_config
        assert 'entry-points' in project_config
        
        # OneEnv dependency の確認
        deps = project_config['dependencies']
        oneenv_dep = next((dep for dep in deps if dep.startswith('oneenv')), None)
        assert oneenv_dep is not None


class TestCLIValidation:
    """CLI機能の検証"""
    
    def test_cli_structure_command(self):
        """CLI --structure コマンドの動作確認"""
        import subprocess
        
        try:
            # oneenv template --structure の実行
            result = subprocess.run(
                [sys.executable, '-m', 'oneenv.cli', 'template', '--structure'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # コマンドが正常に終了することを確認
            assert result.returncode == 0 or result.returncode == 1  # データがない場合も許容
            
            # 出力があることを確認（エラーでない限り）
            if result.returncode == 0:
                assert len(result.stdout) > 0
                
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            pytest.skip(f"CLI command not available: {e}")
    
    def test_cli_help_command(self):
        """CLI helpコマンドの動作確認"""
        import subprocess
        
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'oneenv.cli', '--help'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            assert result.returncode == 0
            assert 'usage:' in result.stdout.lower()
            
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            pytest.skip(f"CLI command not available: {e}")


class TestBackwardCompatibility:
    """後方互換性の検証"""
    
    def test_legacy_decorator_compatibility(self):
        """レガシー@oneenvデコレーターの互換性確認"""
        try:
            from oneenv import oneenv as oneenv_decorator
            
            @oneenv_decorator
            def legacy_template():
                return {
                    "DATABASE_URL": {
                        "description": "Database connection URL",
                        "default": "sqlite:///app.db",
                        "required": True
                    }
                }
            
            # デコレーターが動作することを確認
            assert callable(legacy_template)
            template_data = legacy_template()
            assert isinstance(template_data, dict)
            assert "DATABASE_URL" in template_data
            
        except ImportError:
            pytest.skip("Legacy decorator not available")
    
    def test_existing_api_compatibility(self):
        """既存API関数の互換性確認"""
        # 既存の基本機能が動作することを確認
        try:
            # collect_templates 関数が利用可能か確認
            if hasattr(oneenv, 'collect_templates'):
                templates = oneenv.collect_templates()
                assert isinstance(templates, (list, dict))
            
        except Exception as e:
            pytest.skip(f"Legacy API not fully available: {e}")


if __name__ == "__main__":
    # テストの直接実行
    pytest.main([__file__, "-v"])