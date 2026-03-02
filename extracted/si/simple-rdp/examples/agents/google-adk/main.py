import os
from asyncio import run
from contextlib import contextmanager
from datetime import datetime
from logging import getLogger
from pathlib import Path
from warnings import catch_warnings
from warnings import filterwarnings

from dotenv import load_dotenv
from google.adk import Runner
from google.adk.agents import LlmAgent
from google.adk.apps.app import App
from google.adk.plugins.multimodal_tool_results_plugin import MultimodalToolResultsPlugin
from google.adk.sessions import Session
from google.adk.sessions.database_session_service import DatabaseSessionService
from google.genai.types import Content
from google.genai.types import FinishReason
from google.genai.types import Part
from openinference.instrumentation.google_adk import GoogleADKInstrumentor
from rich.logging import RichHandler

from simple_rdp import RDPClient

load_dotenv()
logger = getLogger("adk_agent")

GoogleADKInstrumentor().instrument()

instruction = """
You are an Autonomous agent with a desktop computer. 
You need to share you thinking throughout the process.
"""


def get_agent(tools: list) -> LlmAgent:
    return LlmAgent(
        name="computer_use_agent",
        model="gemini-3-pro-preview",  # Or your preferred Gemini model
        instruction=instruction,
        description="An autonomous agent with Desktop Computer capabilities.",
        tools=tools,
    )


async def get_rdp_client() -> RDPClient:
    recoring_path = Path(".") / "sessions"
    recoring_path.mkdir(exist_ok=True)
    recoring_path = recoring_path / "google_adk_agent"
    recoring_path.mkdir(exist_ok=True)
    recoring_path = recoring_path / (datetime.now().strftime("%Y%m%d_%H%M%S") + ".mp4")
    recoring_path = str(recoring_path)
    client = RDPClient(
        host=os.environ.get("RDP_HOST", ""),
        username=os.environ.get("RDP_USER", ""),
        password=os.environ.get("RDP_PASS", ""),
        show_wallpaper=True,
        record_to=recoring_path,
    )
    return client


async def main(question: str, session_id: str | None = None):
    user = "user123"
    app_name = "adk_agent"
    session_service = await get_session_service()

    rdp_client = await get_rdp_client()
    tools = rdp_client.get_agentic_tools(for_framework="google-adk")
    agent = get_agent(tools=tools)

    # We need to use app to enable MultimodalToolResultsPlugin which allows image + text responses
    app = App(
        name=app_name,
        root_agent=agent,
        plugins=[MultimodalToolResultsPlugin()],
    )
    async with rdp_client:  # Alternatively, you can do rdp_client.connect() and rdp_client.disconnect() manually
        runner = Runner(
            session_service=session_service,
            app=app,
        )
        session = await get_session(
            session_service=session_service,
            user_id=user,
            session_id=session_id,
            app_name=app_name,
        )
        runner = runner.run_async(
            user_id=user,
            session_id=session.id,
            new_message=Content(
                role="user",
                parts=[Part(text=question)],
            ),
        )
        async for response in runner:
            if response.finish_reason == FinishReason.STOP:
                if not response.content:
                    logger.warning("Agent finished without a response.")
                    raise ValueError("Agent finished without a response.")
                if not response.content.parts:
                    logger.warning("Agent finished without a response.")
                    raise ValueError("Agent finished without a response.")
                logger.info(f"Agents response: [bold blue]\n\t{response.content.parts[-1].text}[/bold blue]\n")


async def get_session_service() -> DatabaseSessionService:
    return DatabaseSessionService(db_url="sqlite+aiosqlite:///./adk_agent_data.db")


async def get_session(
    session_service: DatabaseSessionService,
    user_id: str,
    *,
    session_id: str | None = None,
    app_name: str = "adk-agent",
) -> Session:
    if session_id is None:
        logger.info("No session ID provided. Creating a new session...")
        session = await session_service.create_session(app_name=app_name, user_id=user_id)
        logger.info(f"Created new session with ID: {session.id}")
        return session
    logger.info(f"Retrieving session with ID: {session_id}...")
    session = await session_service.get_session(app_name=app_name, session_id=session_id, user_id=user_id)
    if session:
        logger.info(f"Session found: {session.id}")
        return session
    raise ValueError(f"Session with ID {session_id} not found")


@contextmanager
def configure_logging():
    logging.basicConfig(level=logging.INFO, format="\\[%(name)s]: %(message)s", handlers=[RichHandler(markup=True)])
    adk_logger = getLogger("google_adk.google.adk.models.google_llm")
    adk_logger.setLevel(logging.WARNING)
    httpx_logger = getLogger("httpx")
    httpx_logger.setLevel(logging.WARNING)
    adk_logger = getLogger("google_adk.google.adk.sessions.database_session_service")
    adk_logger.setLevel(logging.WARNING)
    with catch_warnings():
        filterwarnings("ignore", category=UserWarning, module="pydantic")
        yield


def configure_check_langfuse():
    # Check if Langfuse environment variables are set for logging
    lf_public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
    lf_secret_key = os.environ.get("LANGFUSE_SECRET_KEY")
    lf_base_url = os.environ.get("LANGFUSE_BASE_URL")
    if not lf_public_key or not lf_secret_key or not lf_base_url:
        return
    from langfuse import get_client

    langfuse = get_client()
    if langfuse.auth_check():
        logger.info("Langfuse client is authenticated and ready!")
    else:
        logger.warning("Authentication failed. Please check your credentials and host.")


if __name__ == "__main__":
    import logging

    with configure_logging():
        configure_check_langfuse()
        question = "Can you open browser and see navigate to google.com for me? Search for weather in new York"
        session_id = None  # Or set to an existing session ID to continue a conversation
        run(main(question, session_id))
