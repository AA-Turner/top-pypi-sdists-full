from enum import Enum


class JobAutomationMode(Enum):
    TRAIN = "training"
    EVALUATE = "evaluation"
    SCORE = "scoring"
    DEPLOY = "deployment"


class JobRunnerMode(Enum):
    TRAIN = "Train"
    EVALUATE = "Evaluate"
    SCORE = "Score"


class JobRunnerEngine(Enum):
    PYTHON = "python"
    R = "R"
    SQL = "sql"
