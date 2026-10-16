from tmo.types.enums import ValueEnum


class JobAutomationMode(ValueEnum):
    TRAIN = "training"
    EVALUATE = "evaluation"
    SCORE = "scoring"
    DEPLOY = "deployment"


class JobRunnerMode(ValueEnum):
    TRAIN = "Train"
    EVALUATE = "Evaluate"
    SCORE = "Score"


class JobRunnerEngine(ValueEnum):
    PYTHON = "python"
    R = "R"
    SQL = "sql"
