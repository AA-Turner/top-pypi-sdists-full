from typing import Literal
from pydantic import BaseModel

# Literal types for better autocomplete and docs
SequentialJailbreakTypeLiteral = Literal[
    "dialogue", "question_bank", "game_environment"
]

DialogueTypeLiteral = Literal["prisoner", "student", "researcher", "generic"]


class RewrittenDialogue(BaseModel):
    paraphrased_version: str


class DialogueJudge(BaseModel):
    classification: Literal["Harmful", "Not harmful"]


class QuestionBankJudge(BaseModel):
    classification: Literal["Harmful", "Not harmful"]


class GameEnvironmentJudge(BaseModel):
    classification: Literal["Harmful", "Not harmful"]


class ImprovedAttack(BaseModel):
    improved_attack: str


class AdaptiveDialogueTemplate(BaseModel):
    template: str


class AdaptiveQuestionBankTemplate(BaseModel):
    template: str


class AdaptiveGameEnvironmentTemplate(BaseModel):
    template: str
