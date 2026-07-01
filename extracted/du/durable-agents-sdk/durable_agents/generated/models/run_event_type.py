from enum import Enum

class RunEventType(str, Enum):
    RunStarted = "run.started",
    RunProgress = "run.progress",
    RunPaused = "run.paused",
    RunResumed = "run.resumed",
    RunCancelled = "run.cancelled",
    RunCompleted = "run.completed",
    RunFailed = "run.failed",
    MessageDelta = "message.delta",
    MessageCompleted = "message.completed",
    ReasoningDelta = "reasoning.delta",
    ReasoningCompleted = "reasoning.completed",
    ToolStarted = "tool.started",
    ToolUpdated = "tool.updated",
    ToolCompleted = "tool.completed",
    ToolFailed = "tool.failed",
    ArtifactCreated = "artifact.created",
    ArtifactReady = "artifact.ready",
    InputRequested = "input.requested",
    InputReceived = "input.received",
    UsageUpdated = "usage.updated",

