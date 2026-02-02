
import pytest
import dslighting
import pandas as pd
from pathlib import Path
import shutil
import yaml
import sys
from unittest.mock import AsyncMock, MagicMock

# Add project root to sys.path to resolve module imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dsat.config import LLMConfig

# A mock script that the LLM will "generate"
MOCK_LLM_CODE = """
import pandas as pd
try:
    test_df = pd.read_csv('test.csv')
    submission_df = pd.DataFrame({'PassengerId': test_df['PassengerId'], 'Survived': 0})
    submission_df.to_csv('submission.csv', index=False)
except FileNotFoundError:
    # Handle case where files might be in a parent dir in sandbox
    test_df = pd.read_csv('../test.csv')
    submission_df = pd.DataFrame({'PassengerId': test_df['PassengerId'], 'Survived': 0})
    submission_df.to_csv('submission.csv', index=False)
"""

MOCK_LLM_RESPONSE_CONTENT = f"리뷰 및 개선:\n- 최종 코드는 주어진 문제를 해결하기 위한 것입니다.\n- 코드는 먼저 `test.csv`를 읽고, 모든 승객의 'Survived'를 0으로 예측하는 `submission.csv` 파일을 생성합니다.\n\n코드:\n```python\n{MOCK_LLM_CODE}\n```"

# Mark all tests in this file as 'e2e'
pytestmark = pytest.mark.e2e

@pytest.fixture(scope="function")
def agent(monkeypatch):
    """
    Provides a default dslighting agent for testing and mocks the LLM call.
    """
    # 1. Mock get_api_keys to bypass the LLMService __init__ check
    monkeypatch.setattr(LLMConfig, "get_api_keys", lambda self: ["DUMMY_KEY"])

    # 2. Mock the actual API call function to avoid network requests
    mock_completion = AsyncMock()
    
    # Create a mock response object that mimics litellm's response structure
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = MOCK_LLM_RESPONSE_CONTENT
    mock_response.usage = MagicMock() # Add usage attribute
    mock_response.usage.prompt_tokens = 100
    mock_response.usage.completion_tokens = 100
    mock_response.usage.total_tokens = 200
    
    mock_completion.return_value = mock_response
    monkeypatch.setattr("litellm.acompletion", mock_completion)

    # 3. Return the agent
    return dslighting.Agent(workflow="aide", model="mock-model")

class TestEndToEndGrading:
    """
    End-to-end tests to ensure the grading pipeline returns valid scores.
    """

    def test_builtin_task_grading(self, agent):
        """
        Tests grading for a built-in Kaggle task using explicit paths.
        """
        data_dir = str(project_root / "competitions" / "titanic")
        # The registry for built-in tasks is inside the dslighting package itself
        registry_dir = str(project_root / "dslighting" / "registry")
        
        # Check if the data directory exists before running the test
        if not Path(data_dir).exists() or not (Path(data_dir) / "prepared" / "public").exists():
            pytest.skip(f"Built-in test data not found or not structured correctly at {data_dir}")

        result = agent.run(
            task_id="titanic",
            data_dir=data_dir,
            registry_dir=registry_dir
        )

        assert result.success is True, f"Agent run failed: {result.error}"
        assert result.score is not None, "Score is None, grading failed."
        assert isinstance(result.score, float), f"Score is not a float, but {type(result.score)}"
        assert 0.0 <= result.score <= 1.0, f"Score {result.score} is out of the expected range [0, 1]"

    def test_custom_task_grading(self, agent, tmp_path_factory):
        """
        Tests grading for a user-registered task with a custom grade.py.
        """
        root_dir = tmp_path_factory.mktemp("custom_task")
        registry_dir = root_dir / "registry"
        data_dir = root_dir / "data"

        task_registry_dir = registry_dir / "titanic"
        task_data_dir = data_dir / "competitions" / "titanic"
        
        public_data_dir = task_data_dir / "prepared" / "public"
        private_data_dir = task_data_dir / "prepared" / "private"
        
        public_data_dir.mkdir(parents=True, exist_ok=True)
        private_data_dir.mkdir(parents=True, exist_ok=True)
        task_registry_dir.mkdir(parents=True, exist_ok=True)

        config_content = {
            "id": "titanic", "name": "Titanic", "competition_type": "standard",
            "description": "A test competition.",
            "dataset": {
                "answers": "competitions/titanic/prepared/private/test_answer.csv",
                "sample_submission": "competitions/titanic/prepared/public/sampleSubmission.csv"
            },
            "grader": {"name": "accuracy", "grade_fn": "grade:grade" }
        }
        with open(task_registry_dir / "config.yaml", "w") as f:
            yaml.dump(config_content, f)

        grade_py_content = """
import pandas as pd
from sklearn.metrics import accuracy_score
def grade(answer_df: pd.DataFrame, submission_df: pd.DataFrame) -> float:
    merged_df = pd.merge(answer_df, submission_df, on='PassengerId', suffixes=('_ans', '_sub'), how='left')
    merged_df['Survived_sub'] = merged_df['Survived_sub'].fillna(0).astype(int)
    if 'Survived_ans' not in merged_df or 'Survived_sub' not in merged_df: return 0.0
    score = accuracy_score(merged_df['Survived_ans'], merged_df['Survived_sub'])
    return float(score)
"""
        with open(task_registry_dir / "grade.py", "w") as f:
            f.write(grade_py_content)

        (public_data_dir / "train.csv").write_text("PassengerId,Survived\n1,0\n2,1")
        (public_data_dir / "test.csv").write_text("PassengerId\n3\n4")
        (private_data_dir / "test_answer.csv").write_text("PassengerId,Survived\n3,1\n4,0")
        (public_data_dir / "sampleSubmission.csv").write_text("PassengerId,Survived\n3,0\n4,0")

        result = agent.run(
            task_id="titanic", 
            data_dir=str(task_data_dir), 
            registry_dir=str(task_registry_dir.parent)
        )

        assert result.success is True, f"Agent run failed: {result.error}"
        assert result.score is not None, "Score is None, grading failed."
        assert isinstance(result.score, float), f"Score is not a float, but {type(result.score)}"
        assert 0.0 <= result.score <= 1.0, f"Score {result.score} is out of the expected range [0, 1]"

