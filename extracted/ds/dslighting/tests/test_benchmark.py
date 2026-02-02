"""
DSLighting Benchmark 系统测试
"""

import pytest
import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

from dslighting.benchmark import (
    BaseBenchmark,
    MLELiteBenchmark,
    CustomBenchmark,
    BenchmarkFactory,
)
from dsat.models.task import TaskDefinition


# ============================================================================
# 测试 BaseBenchmark
# ============================================================================

class TestBaseBenchmark:
    """测试基础 Benchmark 类"""

    def test_init(self):
        """测试初始化"""
        tasks = [
            TaskDefinition(task_id="test1", task_type="kaggle", payload={}),
            TaskDefinition(task_id="test2", task_type="kaggle", payload={}),
        ]

        benchmark = BaseBenchmark("test-bench", tasks)

        assert benchmark.name == "test-bench"
        assert len(benchmark.tasks) == 2
        assert benchmark.log_path.exists()

    @pytest.mark.asyncio
    async def test_run_evaluation(self):
        """测试批量评估"""
        tasks = [
            TaskDefinition(task_id="test1", task_type="kaggle", payload={}),
            TaskDefinition(task_id="test2", task_type="kaggle", payload={}),
        ]

        benchmark = BaseBenchmark("test-bench", tasks)

        # Mock 评估函数
        async def eval_fn(task, **kwargs):
            return {
                "score": 0.85,
                "cost": 0.1,
                "duration": 60.0,
            }

        results = await benchmark.run_evaluation(eval_fn)

        assert len(results) == 2
        assert results[0]["score"] == 0.85
        assert results[1]["score"] == 0.85

    def test_get_statistics(self):
        """测试统计分析"""
        tasks = [
            TaskDefinition(task_id="test1", task_type="kaggle", payload={}),
        ]

        benchmark = BaseBenchmark("test-bench", tasks)

        # Mock 结果
        benchmark.results = [
            {"score": 0.8, "cost": 0.1, "duration": 60.0},
            {"score": 0.9, "cost": 0.2, "duration": 70.0},
            {"score": None, "cost": 0.0, "duration": 0.0},  # 失败的任务
        ]

        stats = benchmark.get_statistics()

        assert stats["total_tasks"] == 3
        assert stats["successful_tasks"] == 2
        assert stats["failed_tasks"] == 1
        assert stats["avg_score"] == 0.85
        assert stats["success_rate"] == 2/3


# ============================================================================
# 测试 MLELiteBenchmark
# ============================================================================

class TestMLELiteBenchmark:
    """测试 MLE-Bench Lite 类"""

    def test_init_default(self):
        """测试使用默认精选任务初始化"""
        benchmark = MLELiteBenchmark()

        assert benchmark.name == "mle-lite"
        assert len(benchmark.competitions) == 10
        assert "bike-sharing-demand" in benchmark.competitions

    def test_init_custom(self):
        """测试自定义任务列表"""
        competitions = ["bike-sharing-demand", "titanic"]
        benchmark = MLELiteBenchmark(competitions=competitions)

        assert len(benchmark.competitions) == 2
        assert benchmark.competitions == competitions

    def test_get_default_competitions(self):
        """测试获取默认精选任务"""
        default_comps = MLELiteBenchmark.get_default_competitions()

        assert len(default_comps) == 10
        assert "bike-sharing-demand" in default_comps

    def test_list_available_competitions(self):
        """测试列出可用竞赛"""
        # 需要真实的数据目录
        data_dir = Path("data/competitions")

        if data_dir.exists():
            available = MLELiteBenchmark.list_available_competitions(data_dir)
            assert isinstance(available, list)


# ============================================================================
# 测试 CustomBenchmark
# ============================================================================

class TestCustomBenchmark:
    """测试自定义 Benchmark 类"""

    def test_init(self):
        """测试初始化"""
        tasks = [
            TaskDefinition(task_id="custom1", task_type="kaggle", payload={}),
        ]

        benchmark = CustomBenchmark("custom", tasks)

        assert benchmark.name == "custom"
        assert len(benchmark.tasks) == 1


# ============================================================================
# 测试 BenchmarkFactory
# ============================================================================

class TestBenchmarkFactory:
    """测试工厂类"""

    def test_init(self):
        """测试初始化"""
        factory = BenchmarkFactory(
            config_path=Path("config.yaml"),
            registry_dir=Path("dslighting/registry"),
            data_dir=Path("data/competitions"),
        )

        assert factory.config_path == Path("config.yaml")
        assert factory.registry_dir == Path("dslighting/registry")

    def test_list_benchmarks(self):
        """测试列出 Benchmark"""
        factory = BenchmarkFactory(config_path=Path("config.yaml"))

        if factory.config:
            benchmarks = factory.list_benchmarks()
            assert isinstance(benchmarks, list)
            assert "mle-lite" in benchmarks


# ============================================================================
# 运行测试
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
