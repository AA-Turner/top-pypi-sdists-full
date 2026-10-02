from enum import StrEnum

class SynthesizerListDtoItemsUserTargetFieldsItem(StrEnum):
    ALLOWEDDOMAINS = "allowedDomains"
    CONTAINERIMAGE = "containerImage"
    CONTAINERSIZE = "containerSize"
    FORMANSWERS = "formAnswers"
    GPUTYPE = "gpuType"
    GRADERRUNCONFIGVERSIONID = "graderRunConfigVersionId"
    GRADERSUPPORTFILES = "graderSupportFiles"
    GRADINGCONFIG = "gradingConfig"
    INSTALLEDPACKAGEMANAGERS = "installedPackageManagers"
    ISSUETEMPLATE = "issueTemplate"
    MAXTURNS = "maxTurns"
    PRIVILEGED = "privileged"
    PROBLEMFILES = "problemFiles"
    PROMPT = "prompt"
    QARUNCONFIGVERSIONID = "qaRunConfigVersionId"
    RUBRICS = "rubrics"
    SINGLEAGENTRUBRIC = "singleAgentRubric"
    SOLVERRUNCONFIGVERSIONID = "solverRunConfigVersionId"
    SUPPORTINGFILES = "supportingFiles"
    SYNTHESIZERRUNCONFIGVERSIONID = "synthesizerRunConfigVersionId"
    TIMEOUTSECONDS = "timeoutSeconds"
    TOOLS = "tools"
    TOOLTIMEOUTS = "toolTimeouts"

    def __str__(self) -> str:
        return str(self.value)
