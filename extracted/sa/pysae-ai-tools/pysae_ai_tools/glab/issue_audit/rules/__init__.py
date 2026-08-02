"""Rule registry for audit rules."""

from .assignee import AssigneeRule
from .base import Rule
from .board import BoardRule
from .labels import LabelsRule
from .required_labels import RequiredLabelsRule
from .spec import SpecRule
from .template import TemplateRule
from .title import TitleRule
from .weight import WeightRule

RULES: dict[str, Rule] = {
    "labels": LabelsRule(),
    "required_labels": RequiredLabelsRule(),
    "board": BoardRule(),
    "weight": WeightRule(),
    "assignee": AssigneeRule(),
    "spec": SpecRule(),
    "title": TitleRule(),
    "template": TemplateRule(),
}
