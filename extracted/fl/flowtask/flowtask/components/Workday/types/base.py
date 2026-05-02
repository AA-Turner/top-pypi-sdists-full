# types/base.py

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from zeep.helpers import serialize_object


class WorkdayTypeBase(ABC):
    """
    Base class for Workday operation types.

    Provides:
      - Default payload structure for all Workday operations.
      - Generic pagination logic with retries and logging.
      - Common SOAP response handling utilities.
    """

    def __init__(
        self,
        component: Any,
        max_retries: int = 3,
        retry_delay: float = 0.5,
    ):
        """
        Initialize the base type handler.
        
        :param component: Component instance (used for run, logger, metrics).
        :param max_retries: Maximum number of retry attempts per page on failure.
        :param retry_delay: Seconds to wait between retry attempts.
        """
        self.component = component
        self._logger: logging.Logger = getattr(
            component, "_logger", logging.getLogger(__name__)
        )
        self.request_payload: Dict[str, Any] = self._get_default_payload()
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def _get_default_payload(self) -> Dict[str, Any]:
        """
        Base payload structure sent in all Workday calls.
        Override this method in subclasses to provide operation-specific defaults.
        """
        return {
            "Response_Filter": {},
            "Response_Group": {},
        }

    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """
        Execute the specific operation logic.
        Must be implemented by subclasses.
        """
        raise NotImplementedError

    async def _paginate_soap_operation(
        self,
        operation: str,
        data_path: List[str],
        results_path: List[str],
        all_pages: bool = True,
        page: int = 1,
        count: int = 100,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        """
        Generic logic for paginating Workday SOAP responses.

        :param operation: SOAP operation name (e.g., "Get_Workers", "Get_Organizations").
        :param data_path: List of keys to extract items (e.g., ["Response_Data", "Worker"]).
        :param results_path: List of keys to extract pagination info (e.g., ["Response_Results"]).
        :param all_pages: If False, only fetch the first page.
        :param page: Initial page (default 1).
        :param count: Page size (items per call).
        :param kwargs: Other SOAP filters or arguments.
        :returns: Accumulated list of dicts with items from all pages.
        """
        accumulated: List[Dict[str, Any]] = []
        current_page = page
        total_pages: Optional[int] = None

        while True:
            # Construir payload de paginación
            response_filter = dict(self.request_payload.get("Response_Filter") or {})
            response_filter.update({"Page": current_page, "Count": count})

            payload = {
                **self.request_payload,
                "Response_Filter": response_filter,
            }
            request_args = {**kwargs, **payload}

            # Retry attempts
            raw = None
            for attempt in range(1, self.max_retries + 1):
                try:
                    raw = await self.component.run(operation=operation, **request_args)
                    break
                except Exception as exc:
                    self._logger.warning(
                        f"[{operation}] Error on page {current_page} "
                        f"(attempt {attempt}/{self.max_retries}): {exc}"
                    )
                    if attempt == self.max_retries:
                        self._logger.error(
                            f"[{operation}] Failed page {current_page} after "
                            f"{self.max_retries} attempts."
                        )
                        raise
                    await asyncio.sleep(self.retry_delay)

            # Serializar objeto Zeep a dict puro
            data = serialize_object(raw)

            # Extract items list
            items: Any = data
            for key in data_path:
                if not isinstance(items, dict):
                    self._logger.warning(
                        f"[{operation}] Expected dict while traversing data_path {data_path}, "
                        f"got {type(items).__name__}"
                    )
                    items = {}
                    break
                items = items.get(key) or {}
            if isinstance(items, dict):
                items = [items]
            elif not isinstance(items, list):
                self._logger.warning(
                    f"[{operation}] Expected list/dict in data_path {data_path}, "
                    f"got {type(items).__name__}; skipping."
                )
                items = []

            accumulated.extend(items)

            # Extract pagination info
            info: Any = data
            for key in results_path:
                if not isinstance(info, dict):
                    info = {}
                    break
                info = info.get(key) or {}
            
            # Handle case where info might be a list
            if isinstance(info, list) and info:
                info = info[0]  # Take first element if it's a list
            elif not isinstance(info, dict):
                info = {}
                
            try:
                total_pages = int(info.get("Total_Pages", 1))
            except (TypeError, ValueError):
                total_pages = 1

            self._logger.info(
                f"[{operation}] Page {current_page}/{total_pages} -> "
                f"{len(items)} items fetched."
            )

            # Continue paginating?
            if not all_pages or current_page >= total_pages:
                break
            current_page += 1

        return accumulated
