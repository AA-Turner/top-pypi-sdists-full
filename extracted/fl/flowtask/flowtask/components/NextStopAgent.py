"""
NextStop Agent.

Run queries using the NextStop Agent.
"""
from typing import Optional, Any
from collections.abc import Callable
import asyncio
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, Field
import pandas as pd
# Parrot AI Agent:
from parrot.agents.nextstop import NextStop
# Tools:
from parrot.tools.nextstop import (
    StoreInfo,
    EmployeeToolkit
)
from parrot.models.responses import AgentResponse
# Inherited interfaces:
from ..interfaces.parrot import AgentBase
from .flow import FlowComponent

class NextStopResponse(AgentResponse):
    """
    NextStopResponse is a model that defines the structure of the response
    for the NextStop agent.
    """
    user_id: Optional[str] = Field(
        default=None,
        description="ID of the user associated with the session (in flowtask context will be null)"
    )
    program_slug: str = Field(default="hisense", description="Program slug for the agent")
    kind: Optional[str] = Field(
        default=None,
        description="Kind of response, e.g., 'visit_report'"
    )
    content: str = Field(
        default="",
        description="Description of Generated Report."
    )
    store_id: Optional[str] = Field(
        default=None,
        description="ID of the store associated with the session"
    )
    employee_id: Optional[str] = Field(
        default=None,
        description="ID of the employee associated with the session"
    )
    manager_id: Optional[str] = Field(
        default=None,
        description="ID of the manager associated with the session"
    )

class NextStopAgent(AgentBase, FlowComponent):
    """
    NextStopAgent.

    Overview:
        The NextStopAgent class is a FlowComponent that integrates with the Parrot AI Agent framework to run queries
        using the NextStop Agent. It extends the AgentBase class and provides methods for creating and managing the
        agent's lifecycle within a FlowTask.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          NextStopAgent:
          # attributes here
        ```
    """
    _version = "1.0.0"
    _agent_class: type = NextStop
    _agent_name: str = 'NextStopAgent'
    agent_id: str = 'nextstop_agent'
    _agent_response: type = NextStopResponse  # Default response type

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        # Method to be executed by agent:
        self._report = kwargs.get('report', 'for_employee')
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    def _define_tools(self, base_dir: Path):
        """Define tools for the NextStop Agent."""
        program = getattr(self, '_program', 'hisense')
        tools = StoreInfo(program=program).get_tools()
        tools.extend(EmployeeToolkit(program=program).get_tools())
        return tools

    async def start(self, **kwargs):
        """
        start.

            Initialize (if needed) a task
        """
        if self.previous:
            self.data = self.input
        # check if previous data is an iterable:
        if isinstance(self.data, pd.DataFrame):
            self._iterable = self.data.iterrows()
        await super().start(**kwargs)

    async def close(self):
        pass

    async def _process_row(self, row, report):
        """
        Process each row with the report.

        Args:
            row: A single row from the DataFrame.
            report: The report to be processed.
        """
        # Here you would implement the logic to process each row with the report
        # For example, you might call a method on the agent to handle the row
        self.logger.info(f"Processing row: {row} with report: {report}")
        try:
            data = row.to_dict()
            response = await self._agent.report(
                prompt_file=report,
                program_slug=self._program,
                **data
            )
            response.manager_id = row.get('manager_id', None)
            response.employee_id = row.get('employee_id', None)
            response.program_slug = self._program
        except Exception as e:
            self.logger.error(
                f"Error processing row {row}: {e}"
            )
            return None
        self.logger.info(
            f"Processed row successfully: {response}"
        )
        return response

    async def run(self):
        """
        run.

            Run the NextStop Agent with the provided data.
        """
        try:
            # calling a report for every row in the DataFrame:
            results = []
            if isinstance(self.data, pd.DataFrame):
                for _, row in self.data.iterrows():
                    report = f"{self._report}.txt"
                    # Process each row with the report
                    result = await self._process_row(row, report)
                    if result:
                        # Define the kind and content:
                        if self._report == 'for_employee':
                            result.kind = "_nextstop_employee"
                            result.content = f"Employee: {row.get('employee_id', '')}"
                        elif self._report == 'team_performance':
                            result.kind = "_team_performance"
                            result.content = f"Team Performance for: {row.get('manager_id', '')}"
                        results.append(result)
                    else:
                        # there is no info for this employee:
                        self.logger.warning(
                            f"No result for row: {row}"
                        )
                        continue
            # Convert results to a DataFrame if needed
            if results:
                # responses: list[NextStopResponse]
                self._result = pd.DataFrame(
                    [
                        r.model_dump(mode="json", exclude_none=True) for r in results
                    ]
                )
                # Add Column "request_date" with today's date:
                self._result['request_date'] = datetime.now().isoformat()
            self._print_data_(
                self._result,
                title="NextStop Agent Results"
            )
            return self._result
        except Exception as e:
            self.logger.error(
                f"Error occurred while running NextStopAgent: {e}"
            )
            return None
