"""
Create a Parrot AI Agent for FlowTask.
"""
from abc import ABC, abstractmethod
import contextlib
from typing import Any, Dict, Optional, List
from pathlib import Path
from datetime import datetime
import aiofiles
from datamodel import BaseModel
from asyncdb import AsyncDB  # noqa  pylint: disable=E0611
from navconfig import config, BASE_DIR  # noqa  pylint: disable=E0611
from navconfig.logging import logging
from querysource.conf import default_dsn
# Parrot:
from parrot.bots.agent import BasicAgent
from parrot.clients import AbstractClient
from parrot.tools.abstract import AbstractTool
from parrot.models.responses import AgentResponse


class AgentBase(ABC):
    """AgentBase.

    Interface for creating new Parrot AI Agents to be used directly as Flowtask Components.

    """
    _agent_name: str = 'ParrotAgent'
    agent_id: str = 'parrot_agent'
    _agent_class: type = BasicAgent
    _backstory: Optional[str] = None
    _agent_response: type = AgentResponse  # Default response type
    _max_tokens: int = 16000
    _tools: List[AbstractTool] = []

    def __init__(self, *args, **kwargs):
        self._agent_name: str = kwargs.get('agent_name', self._agent_name)
        self._name_: str = kwargs.get('name', self._agent_name)
        self.agent_id: str = kwargs.get('agent_id', self.agent_id)
        self.backstory: Optional[str] = kwargs.get('backstory_file', "backstory.txt")
        self._backstory: str = kwargs.get('backstory', None)
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self._name_}")
        self._use_taskstorage = kwargs.get('use_taskstorage', True)
        # Agent Configuration:
        self._agent: Optional[BasicAgent] = None
        self._llm: Optional[AbstractClient] = kwargs.get('llm', None)
        self._model: Optional[str] = kwargs.get('model', None)
        self._tools: List[AbstractTool] = kwargs.pop('tools', [])
        self._config: Dict[str, Any] = kwargs.get('config', {})
        self._max_tokens: int = kwargs.get('max_tokens', self._max_tokens)
        super(AgentBase, self).__init__(*args, **kwargs)

    @abstractmethod
    def _define_tools(self, base_dir: Path) -> List[AbstractTool]:
        """Define the tools for the agent."""
        raise NotImplementedError(
            "Subclasses must implement _define_tools method."
        )

    def db_connection(
        self,
        driver: str = 'pg',
        dsn: str = None,
        credentials: dict = None
    ) -> AsyncDB:
        """Return a database connection."""
        if not dsn:
            dsn = config.get(f'{driver.upper()}_DSN', fallback=default_dsn)
        if not dsn and credentials:
            dsn = credentials.get('dsn', default_dsn)
        if not dsn:
            raise ValueError(
                f"DSN for {driver} is not provided."
            )
        return AsyncDB(driver, dsn=dsn, credentials=credentials)

    async def open_prompt(self, prompt_file: str = None, base_dir: Path = None) -> str:
        """
        Opens a prompt file and returns its content.
        """
        if not prompt_file:
            raise ValueError("No prompt file specified.")
        if not base_dir:
            base_dir = BASE_DIR
        file = base_dir.joinpath('prompts', self.agent_id, prompt_file)
        try:
            async with aiofiles.open(file, 'r') as f:
                content = await f.read()
            return content
        except Exception as e:
            raise RuntimeError(
                f"Failed to read prompt file {prompt_file}: {e}"
            )

    async def open_file(self, file: str, prefix: str = 'files') -> str:
        """
        Opens a prompt file and returns its content.
        """
        filename = self.directory.joinpath(prefix, self.agent_id, file)
        if not filename.exists() or not filename.is_file():
            raise FileNotFoundError(
                f"File {filename} does not exist in the directory {self.directory}."
            )
        try:
            async with aiofiles.open(filename, 'r') as f:
                content = await f.read()
            return content
        except Exception as e:
            self.logger.warning(
                f"Failed to read prompt file {filename}: {e}"
            )
            return None

    async def create_agent(
        self,
        llm: Any = None,
        model: str = None,
        tools: Optional[List[Any]] = None,
        backstory: Optional[str] = None
    ) -> BasicAgent:
        """Create and configure a BasicAgent instance."""
        try:
            tools = self._define_tools(self.destination)
            if not isinstance(tools, list):
                raise TypeError(
                    "Tools must be a list of AbstractTool instances."
                )
            if not all(isinstance(tool, AbstractTool) for tool in tools):
                raise TypeError(
                    "All tools must be instances of AbstractTool."
                )
            agent = self._agent_class(
                name=self._agent_name,
                llm=llm,
                model=model,
                tools=tools,
                max_tokens=self._max_tokens,
                backstory=backstory or self._backstory,
            )
            agent.set_response(self._agent_response)
            await agent.configure()
            # define the main agent:
            self._agent = agent
            self.logger.info(
                f"Agent {self._agent_name} created and configured successfully."
            )
            return agent
        except Exception as e:
            raise RuntimeError(
                f"Failed to create agent {self._agent_name}: {str(e)}"
            ) from e

    async def start(self, **kwargs):
        """Check for File and Directory information."""
        if hasattr(self, "directory"):
            self.directory = Path(self.directory).resolve()
        else:
            if self._use_taskstorage:
                self.directory = self._taskstore.get_path().joinpath(self._program)
            else:
                self.directory = self._filestore.get_directory('').parent
        # Define destination:
        if hasattr(self, 'destination'):
            self.destination = Path(self.destination).resolve()
        else:
            self.destination = self._filestore.get_directory('', program=self._program)
        if not self.destination.exists():
            self.destination.mkdir(parents=True, exist_ok=True)
            # Also, create the subdirectory for the agent:
            self.destination.joinpath(self._agent_name).mkdir(parents=True, exist_ok=True)
        await super().start(**kwargs)
        # Open the Backstory prompt if it exists
        backstory = None
        with contextlib.suppress(FileNotFoundError):
            backstory = await self.open_file(self.backstory)
        # Create the Agent:
        if not self._agent:
            self._agent = await self.create_agent(
                llm=self._llm,
                model=self._model,
                tools=self._tools,
                backstory=backstory
            )
        if not self._agent:
            raise RuntimeError(
                f"Agent {self.agent_name} could not be created. "
                "Ensure that the LLM and tools are properly configured."
            )
        return True

    async def ask_agent(
        self,
        userid: str,
        query: str = None,
        prompt_file: str = None,
        *args,
        **kwargs
    ) -> tuple[AgentResponse, BaseModel]:
        """
        Asks the agent a question and returns an Object response.
        """
        if not query:
            if prompt_file:
                query = await self.open_prompt(
                    prompt_file=prompt_file,
                    base_dir=self.directory
                )
            else:
                raise ValueError(
                    "Query or prompt file must be provided."
                )
        self.logger.info(
            f"Asking agent {self._agent_name} with query: {query}"
        )
        # Answer is the string version of the query:
        question = query.format(**kwargs)
        # response is a BaseModel instance with the response data
        response = await self._agent.ask(
            question=question,
            max_tokens=16000,
            use_vector_context=False,
            use_conversation_history=False
        )
        if isinstance(response, Exception):
            raise response

        # Create the response object
        final_report = response.output.strip()
        # when final report is made, then generate the transcript, pdf and podcast:
        response_data = self._agent_response(
            user_id=str(userid),
            agent_name=self.agent_name,
            attributes=kwargs.pop('attributes', {}),
            data=final_report,
            status="success",
            created_at=datetime.now(),
            output=response.output,
            **kwargs
        )
        return response_data, response
