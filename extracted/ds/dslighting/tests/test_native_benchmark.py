"""
测试新的 Native Benchmark 系统

验证：
1. 配置文件读取 (grader.name, dataset.answers)
2. 答案文件路径解析（相对于 data_parent_dir）
3. ID 列和目标列的自动推断
4. 评分流程的端到端功能
"""

import pytest
import tempfile
import yaml
from pathlib import Path
import pandas as pd
import sys

# 添加项目根目录到 sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dslighting.benchmark.native.task import NativeTask
from dslighting.benchmark.native.grader import grade_submission, METRIC_FUNCTIONS
from dslighting.benchmark.native.evaluator import NativeBenchmarkEvaluator


class TestNativeGrader:
    """测试评分器和指标函数"""

    def test_metric_registry_contains_required_metrics(self):
        """验证指标注册表包含必需的指标"""
        assert "accuracy" in METRIC_FUNCTIONS, "Missing 'accuracy' metric"
        assert "rmsle" in METRIC_FUNCTIONS, "Missing 'rmsle' metric"

    def test_accuracy_metric(self):
        """测试准确率指标计算"""
        y_true = pd.Series([1, 0, 1, 1, 0])
        y_pred = pd.Series([1, 0, 0, 1, 0])  # 4/5 correct = 0.8

        score = grade_submission(
            submission_df=pd.DataFrame({"id": [1, 2, 3, 4, 5], "target": y_pred}),
            ground_truth_df=pd.DataFrame({"id": [1, 2, 3, 4, 5], "target": y_true}),
            metric="accuracy",
            id_column="id",
            target_column="target",
        )

        assert score == 0.8, f"Expected accuracy 0.8, got {score}"

    def test_grade_submission_with_missing_predictions(self):
        """测试提交中有缺失预测值的情况"""
        y_true = pd.Series([1, 0, 1])
        y_pred = pd.Series([1, 0, 0])  # 2/3 correct

        # Submission has an extra row not in ground truth
        score = grade_submission(
            submission_df=pd.DataFrame({"id": [1, 2, 3, 4], "target": [1, 0, 0, 1]}),
            ground_truth_df=pd.DataFrame({"id": [1, 2, 3], "target": y_true}),
            metric="accuracy",
            id_column="id",
            target_column="target",
        )

        assert score == pytest.approx(2/3), f"Expected accuracy ~0.667, got {score}"


class TestNativeTask:
    """测试 NativeTask 加载和列推断"""

    def test_infer_columns_with_id_column(self):
        """测试有明确 'id' 列的情况"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("PassengerId,Survived\n")
            f.write("1,0\n")
            f.write("2,1\n")
            f.flush()
            temp_path = Path(f.name)

        try:
            id_col, target_col = NativeTask._infer_columns(temp_path)
            assert id_col == "PassengerId", f"Expected 'PassengerId', got '{id_col}'"
            assert target_col == "Survived", f"Expected 'Survived', got '{target_col}'"
        finally:
            temp_path.unlink()

    def test_infer_columns_without_explicit_id(self):
        """测试没有明确 'id' 列的情况，应使用启发式规则"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("col1,col2\n")
            f.write("1,0\n")
            f.write("2,1\n")
            f.flush()
            temp_path = Path(f.name)

        try:
            id_col, target_col = NativeTask._infer_columns(temp_path)
            assert id_col == "col1", f"Expected 'col1' (first column), got '{id_col}'"
            assert target_col == "col2", f"Expected 'col2' (second column), got '{target_col}'"
        finally:
            temp_path.unlink()

    def test_load_task_from_registry(self, tmp_path):
        """测试从注册表目录加载任务"""
        # 创建注册表结构
        registry_dir = tmp_path / "registry"
        data_dir = tmp_path / "data" / "competitions"
        task_registry = registry_dir / "titanic"
        task_data = data_dir / "titanic" / "prepared" / "private"
        task_registry.mkdir(parents=True)
        task_data.mkdir(parents=True)

        # 创建配置文件 (mle-config 格式)
        config = {
            "id": "titanic",
            "name": "Titanic",
            "description": "Predict survival on the Titanic",
            "grader": {
                "name": "accuracy",  # 关键：使用 'name' 而不是 'metric'
            },
            "dataset": {
                "answers": "titanic/prepared/private/test_answer.csv"  # 关键：相对于 data_parent_dir
            }
        }
        with open(task_registry / "config.yaml", 'w') as f:
            yaml.dump(config, f)

        # 创建答案文件
        answers_df = pd.DataFrame({
            "PassengerId": [1, 2, 3],
            "Survived": [0, 1, 1]
        })
        answers_df.to_csv(task_data / "test_answer.csv", index=False)

        # 加载任务
        task = NativeTask.from_registry(
            registry_dir=registry_dir,
            task_id="titanic",
            data_dir=data_dir
        )

        assert task is not None, "Failed to load task"
        assert task.task_id == "titanic"
        assert task.metric == "accuracy", f"Expected metric 'accuracy', got '{task.metric}'"
        assert task.id_column == "PassengerId", f"Expected id_column 'PassengerId', got '{task.id_column}'"
        assert task.target_column == "Survived", f"Expected target_column 'Survived', got '{task.target_column}'"
        assert task.answers_file.exists(), "Answers file path does not exist"

    def test_load_task_with_relative_answer_path(self, tmp_path):
        """测试答案文件路径相对于 data_parent_dir 解析"""
        # 测试 dataset.answers 是相对于 data_parent_dir 而不是 registry_dir
        registry_dir = tmp_path / "registry"
        data_dir = tmp_path / "data" / "competitions"
        task_registry = registry_dir / "test_task"
        task_data = data_dir / "test_task" / "prepared" / "private"

        task_registry.mkdir(parents=True)
        task_data.mkdir(parents=True)

        # 配置文件使用相对路径
        config = {
            "grader": {"name": "accuracy"},
            "dataset": {
                "answers": "test_task/prepared/private/test_answer.csv"  # 相对于 data/competitions
            }
        }
        with open(task_registry / "config.yaml", 'w') as f:
            yaml.dump(config, f)

        # 创建答案文件
        pd.DataFrame({"id": [1, 2], "target": [0, 1]}).to_csv(
            task_data / "test_answer.csv", index=False
        )

        # 加载任务
        task = NativeTask.from_registry(registry_dir, "test_task", data_dir)

        assert task is not None
        # 验证路径正确解析（应该是 data_dir + relative_path）
        assert task.answers_file == task_data / "test_answer.csv"
        assert task.answers_file.exists()


class TestNativeEvaluator:
    """测试端到端评估流程"""

    def test_evaluate_submission_end_to_end(self, tmp_path):
        """端到端测试：创建任务、提交、评估"""
        # 1. 设置目录结构
        registry_dir = tmp_path / "registry"
        data_dir = tmp_path / "data" / "competitions"
        task_registry = registry_dir / "simple_task"
        task_data = data_dir / "simple_task" / "prepared" / "private"
        task_registry.mkdir(parents=True)
        task_data.mkdir(parents=True)

        # 2. 创建配置文件
        config = {
            "id": "simple_task",
            "name": "Simple Task",
            "description": "A simple test task",
            "grader": {"name": "accuracy"},
            "dataset": {"answers": "simple_task/prepared/private/answers.csv"}
        }
        with open(task_registry / "config.yaml", 'w') as f:
            yaml.dump(config, f)

        # 3. 创建答案文件（3个样本：0, 1, 1）
        answers_df = pd.DataFrame({
            "sample_id": [1, 2, 3],
            "label": [0, 1, 1]
        })
        answers_df.to_csv(task_data / "answers.csv", index=False)

        # 4. 创建提交文件（预测：0, 1, 0 - 正确率 2/3）
        submission_df = pd.DataFrame({
            "sample_id": [1, 2, 3],
            "label": [0, 1, 0]
        })
        submission_path = tmp_path / "submission.csv"
        submission_df.to_csv(submission_path, index=False)

        # 5. 创建评估器并评估
        evaluator = NativeBenchmarkEvaluator(
            task_id="simple_task",
            registry_parent_dir=str(registry_dir),
            data_parent_dir=str(data_dir)
        )

        score = evaluator.evaluate(submission_path)

        # 6. 验证分数
        assert score == pytest.approx(2/3), f"Expected score ~0.667, got {score}"
        assert 0.0 <= score <= 1.0, f"Score {score} not in valid range [0, 1]"

    def test_evaluate_with_custom_id_column(self, tmp_path):
        """测试使用自定义ID列名的情况"""
        registry_dir = tmp_path / "registry"
        data_dir = tmp_path / "data" / "competitions"
        task_registry = registry_dir / "custom_id"
        task_data = data_dir / "custom_id" / "prepared" / "private"

        task_registry.mkdir(parents=True)
        task_data.mkdir(parents=True)

        # 使用不同的ID列名
        config = {
            "grader": {"name": "accuracy"},
            "dataset": {"answers": "custom_id/prepared/private/answers.csv"}
        }
        with open(task_registry / "config.yaml", 'w') as f:
            yaml.dump(config, f)

        # 使用 'row_id' 而不是 'id'
        pd.DataFrame({
            "row_id": [1, 2],
            "prediction": [1, 0]
        }).to_csv(task_data / "answers.csv", index=False)

        evaluator = NativeBenchmarkEvaluator(
            task_id="custom_id",
            registry_parent_dir=str(registry_dir),
            data_parent_dir=str(data_dir)
        )

        # 创建提交（全部正确）
        submission_path = tmp_path / "submission.csv"
        pd.DataFrame({
            "row_id": [1, 2],
            "prediction": [1, 0]
        }).to_csv(submission_path, index=False)

        score = evaluator.evaluate(submission_path)
        assert score == 1.0, f"Expected perfect score 1.0, got {score}"


class TestMleConfigCompatibility:
    """测试与 mle-config 格式的兼容性"""

    def test_grader_name_not_metric(self, tmp_path):
        """验证使用 grader.name 而不是 grader.metric"""
        registry_dir = tmp_path / "registry"
        data_dir = tmp_path / "data" / "competitions"
        task_registry = registry_dir / "test"
        task_data = data_dir / "test" / "prepared" / "private"

        task_registry.mkdir(parents=True)
        task_data.mkdir(parents=True)

        # 使用正确的 mle-config 格式：grader.name
        config = {
            "grader": {"name": "accuracy"},  # 正确
            "dataset": {"answers": "test/prepared/private/answers.csv"}
        }
        with open(task_registry / "config.yaml", 'w') as f:
            yaml.dump(config, f)

        pd.DataFrame({"id": [1], "target": [0]}).to_csv(task_data / "answers.csv", index=False)

        task = NativeTask.from_registry(registry_dir, "test", data_dir)
        assert task is not None
        assert task.metric == "accuracy"

    def test_dataset_answers_relative_to_data_dir(self, tmp_path):
        """验证 dataset.answers 相对于 data_parent_dir 解析"""
        registry_dir = tmp_path / "my_registry"
        data_dir = tmp_path / "my_data" / "competitions"
        task_registry = registry_dir / "my_task"
        task_data = data_dir / "my_task" / "prepared" / "private"

        task_registry.mkdir(parents=True)
        task_data.mkdir(parents=True)

        # 配置中的相对路径
        config = {
            "grader": {"name": "accuracy"},
            "dataset": {
                "answers": "my_task/prepared/private/answers.csv"  # 相对于 my_data/competitions
            }
        }
        with open(task_registry / "config.yaml", 'w') as f:
            yaml.dump(config, f)

        # 创建答案文件在正确的位置
        pd.DataFrame({"id": [1], "value": [42]}).to_csv(task_data / "answers.csv", index=False)

        task = NativeTask.from_registry(registry_dir, "my_task", data_dir)

        # 验证路径正确
        assert task.answers_file == task_data / "answers.csv"
        assert str(task.answers_file).startswith(str(data_dir))


# 运行测试的主函数
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
