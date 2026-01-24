from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class MessageTypeWebhookV2Beta(Enums.KnownString):
    V2_BETAAPPCONFIGURATIONUPDATED = "v2-beta.app.configuration.updated"
    V2_BETACANVASCREATED = "v2-beta.canvas.created"
    V2_APPACTIVATEREQUESTED = "v2.app.activateRequested"
    V2_APPDEACTIVATED = "v2.app.deactivated"
    V2_APPINSTALLED = "v2.app.installed"
    V2_ASSAYRUNCREATED = "v2.assayRun.created"
    V2_ASSAYRUNUPDATEDFIELDS = "v2.assayRun.updated.fields"
    V2_AUTOMATIONFILETRANSFORMUPDATEDSTATUSFAILED = "v2.automationFileTransform.updated.status.failed"
    V2_AUTOMATIONFILETRANSFORMUPDATEDSTATUSPENDING = "v2.automationFileTransform.updated.status.pending"
    V2_AUTOMATIONFILETRANSFORMUPDATEDSTATUSRUNNING = "v2.automationFileTransform.updated.status.running"
    V2_AUTOMATIONFILETRANSFORMUPDATEDSTATUSSUCCEEDED = "v2.automationFileTransform.updated.status.succeeded"
    V2_CANVASCREATED = "v2.canvas.created"
    V2_CANVASINITIALIZED = "v2.canvas.initialized"
    V2_CANVASUSERINTERACTED = "v2.canvas.userInteracted"
    V2_ENTITYREGISTERED = "v2.entity.registered"
    V2_ENTRYCREATED = "v2.entry.created"
    V2_ENTRYUPDATEDFIELDS = "v2.entry.updated.fields"
    V2_ENTRYUPDATEDREVIEWRECORD = "v2.entry.updated.reviewRecord"
    V2_REQUESTCREATED = "v2.request.created"
    V2_REQUESTUPDATEDFIELDS = "v2.request.updated.fields"
    V2_REQUESTUPDATEDSTATUS = "v2.request.updated.status"
    V2_WORKFLOWOUTPUTCREATED = "v2.workflowOutput.created"
    V2_WORKFLOWOUTPUTUPDATEDFIELDS = "v2.workflowOutput.updated.fields"
    V2_WORKFLOWTASKCREATED = "v2.workflowTask.created"
    V2_WORKFLOWTASKUPDATEDASSIGNEE = "v2.workflowTask.updated.assignee"
    V2_WORKFLOWTASKUPDATEDFIELDS = "v2.workflowTask.updated.fields"
    V2_WORKFLOWTASKUPDATEDSCHEDULEDON = "v2.workflowTask.updated.scheduledOn"
    V2_WORKFLOWTASKUPDATEDSTATUS = "v2.workflowTask.updated.status"
    V2_WORKFLOWTASKGROUPCREATED = "v2.workflowTaskGroup.created"
    V2_WORKFLOWTASKGROUPMAPPINGCOMPLETED = "v2.workflowTaskGroup.mappingCompleted"
    V2_WORKFLOWTASKGROUPUPDATEDWATCHERS = "v2.workflowTaskGroup.updated.watchers"
    V3_CUSTOMENTITYCREATED = "v3.customEntity.created"
    V3_CUSTOMENTITYUPDATED = "v3.customEntity.updated"
    V3_DNAOLIGOCREATED = "v3.dnaOligo.created"
    V3_DNAOLIGOUPDATED = "v3.dnaOligo.updated"
    V3_DNASEQUENCECREATED = "v3.dnaSequence.created"
    V3_DNASEQUENCEUPDATED = "v3.dnaSequence.updated"
    V3_ENTRYCREATED = "v3.entry.created"
    V3_PROJECTCREATED = "v3.project.created"
    V3_PROJECTUPDATED = "v3.project.updated"
    V3_RNAOLIGOCREATED = "v3.rnaOligo.created"
    V3_RNAOLIGOUPDATED = "v3.rnaOligo.updated"
    V3_RNASEQUENCECREATED = "v3.rnaSequence.created"
    V3_RNASEQUENCEUPDATED = "v3.rnaSequence.updated"
    V3_RUNCREATED = "v3.run.created"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "MessageTypeWebhookV2Beta":
        if not isinstance(val, str):
            raise ValueError(f"Value of MessageTypeWebhookV2Beta must be a string (encountered: {val})")
        newcls = Enum("MessageTypeWebhookV2Beta", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(MessageTypeWebhookV2Beta, getattr(newcls, "_UNKNOWN"))
