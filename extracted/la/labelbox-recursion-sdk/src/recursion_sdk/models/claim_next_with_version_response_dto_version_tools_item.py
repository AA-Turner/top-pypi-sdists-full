from enum import StrEnum

class ClaimNextWithVersionResponseDtoVersionToolsItem(StrEnum):
    ASKUSERQUESTION = "AskUserQuestion"
    BASH = "Bash"
    EDIT = "Edit"
    ENTERPLANMODE = "EnterPlanMode"
    EXITPLANMODE = "ExitPlanMode"
    GLOB = "Glob"
    GREP = "Grep"
    NOTEBOOKEDIT = "NotebookEdit"
    READ = "Read"
    SKILL = "Skill"
    TASK = "Task"
    TASKOUTPUT = "TaskOutput"
    TASKSTOP = "TaskStop"
    TODOWRITE = "TodoWrite"
    TOOLSEARCH = "ToolSearch"
    WEBFETCH = "WebFetch"
    WEBSEARCH = "WebSearch"
    WRITE = "Write"

    def __str__(self) -> str:
        return str(self.value)
