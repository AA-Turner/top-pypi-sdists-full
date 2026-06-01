from typing import Any

import structlog
import temporalio.client
import temporalio.worker
import temporalio.workflow
from temporalio import activity

from mistralai.workflows.core.encoding.fields_offloader import FieldsOffloader, OffloadableModel
from mistralai.workflows.core.temporal.utils import require_activity_context_value

logger = structlog.get_logger(__name__)


class ActivityInOutOffloadingInterceptorInboundInterceptor(temporalio.worker.ActivityInboundInterceptor):
    """Inbound interceptors runs in the workflow context"""

    def __init__(self, next: temporalio.worker.ActivityInboundInterceptor, offloader: FieldsOffloader):
        super().__init__(next)
        self.offloader = offloader

    async def execute_activity(self, input: temporalio.worker.ExecuteActivityInput) -> Any:
        """Restore offloaded fields before activity execution."""
        new_args = []
        for arg in input.args:
            if isinstance(arg, OffloadableModel):
                arg = await self.offloader.restore_if_needed(arg)
            new_args.append(arg)
        input.args = new_args

        # Execute activity
        result = await super().execute_activity(input)

        # Offloaded result if needed
        if isinstance(result, OffloadableModel):
            info = activity.info()
            result = await self.offloader.offload_if_needed(
                result,
                namespace=require_activity_context_value(
                    info.workflow_namespace,
                    field_name="workflow_namespace",
                ),
                run_id=require_activity_context_value(
                    info.workflow_run_id,
                    field_name="workflow_run_id",
                ),
            )
        return result


class ActivityInOutOffloadingInterceptor(temporalio.client.Interceptor, temporalio.worker.Interceptor):
    def __init__(self, offloader: FieldsOffloader):
        self.offloader = offloader

    def intercept_client(self, next: temporalio.client.OutboundInterceptor) -> temporalio.client.OutboundInterceptor:
        return next

    def intercept_activity(
        self, next: temporalio.worker.ActivityInboundInterceptor
    ) -> temporalio.worker.ActivityInboundInterceptor:
        return ActivityInOutOffloadingInterceptorInboundInterceptor(next, self.offloader)
