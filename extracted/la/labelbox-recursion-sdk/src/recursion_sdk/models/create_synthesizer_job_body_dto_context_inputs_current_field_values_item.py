from enum import StrEnum

class CreateSynthesizerJobBodyDtoContextInputsCurrentFieldValuesItem(StrEnum):
    ALLOWEDDOMAINS = "allowedDomains"
    CONTAINERIMAGE = "containerImage"
    CONTAINERSIZE = "containerSize"
    GPUTYPE = "gpuType"
    GRADERRUNCONFIGVERSIONID = "graderRunConfigVersionId"
    GRADINGCONFIG = "gradingConfig"
    INSTALLEDPACKAGEMANAGERS = "installedPackageManagers"
    ISSUETEMPLATE = "issueTemplate"
    MAXTURNS = "maxTurns"
    PRIVILEGED = "privileged"
    PROMPT = "prompt"
    QARUNCONFIGVERSIONID = "qaRunConfigVersionId"
    SINGLEAGENTRUBRIC = "singleAgentRubric"
    SOLVERRUNCONFIGVERSIONID = "solverRunConfigVersionId"
    SYNTHESIZERRUNCONFIGVERSIONID = "synthesizerRunConfigVersionId"
    TIMEOUTSECONDS = "timeoutSeconds"
    TOOLS = "tools"
    TOOLTIMEOUTS = "toolTimeouts"

    def __str__(self) -> str:
        return str(self.value)
