from enum import Enum


class AgentType(str, Enum):
    default = "default"
    planner = "planner"
    react = "react"
    reflection = "reflection"
    router = "router"
    classifier = "classifier"
    supervisor = "supervisor"
    judge = "judge"
