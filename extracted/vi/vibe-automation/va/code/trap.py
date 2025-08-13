import asyncio
import logging
from contextlib import AbstractContextManager
from typing import Optional, Type
from ..constants import VA_ENABLE_RECOVERY

log = logging.getLogger(__name__)


# global variable to mark whether we are performing recovery to avoid recursion
_recovery_in_progress = False


def _update_recovery_in_progress(in_progress: bool):
    global _recovery_in_progress
    _recovery_in_progress = in_progress


def _should_handle_exception(exctype: Optional[Type[Exception]]) -> bool:
    """Check if the exception should be handled by this trap."""
    if exctype is None:
        return False

    # Check if recovery is enabled
    if not VA_ENABLE_RECOVERY:
        return False

    # Don't attempt recovery recursively
    if _recovery_in_progress:
        return False

    return True


class ExceptionTrap(AbstractContextManager):
    """Universal context manager to capture exception and perform agent recovery."""

    def __enter__(self):
        return self

    def __exit__(
        self,
        exctype: Optional[Type[Exception]],
        excinst: Optional[Exception],
        exctb: Optional[object],
    ) -> bool:
        if not _should_handle_exception(exctype):
            return False

        log.info(f"ExceptionTrap caught exception: {excinst}")

        # Check if we're in an async context
        try:
            asyncio.get_running_loop()
            print(
                "🔧 In async context - letting exception propagate to async recovery handler"
            )
            return False
        except RuntimeError:
            # No running loop, run synchronously
            print("🔧 No async context - running recovery synchronously...")

        _update_recovery_in_progress(True)
        from ..agent.recovery import handle_exception_with_recovery

        try:
            success = asyncio.run(handle_exception_with_recovery(excinst, exctb))
        except Exception as e:
            log.error(f"Error during recovery: {e}")
            return False
        finally:
            _update_recovery_in_progress(False)

        if success:
            log.info("Recovery succeeded, suppressing exception")
            return True
        else:
            log.info("Recovery failed, propagating exception")
            return False

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exctype: Optional[Type[Exception]],
        excinst: Optional[Exception],
        exctb: Optional[object],
    ) -> bool:
        if not _should_handle_exception(exctype):
            return False

        log.info(f"ExceptionTrap caught exception: {excinst}")
        _update_recovery_in_progress(True)

        from ..agent.recovery import handle_exception_with_recovery

        try:
            success = await handle_exception_with_recovery(excinst, exctb)
        except Exception as e:
            log.error(f"Error during async recovery: {e}")
            return False
        finally:
            _update_recovery_in_progress(False)

        if success:
            log.info("Async recovery succeeded, suppressing exception")
            return True
        else:
            log.info("Async recovery failed, propagating exception")
            return False


# Global singleton instance - always use this instead of creating new instances
exception_trap = ExceptionTrap()
