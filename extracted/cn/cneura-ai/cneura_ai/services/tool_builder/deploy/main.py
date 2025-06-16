import asyncio
import os
from dotenv import load_dotenv  # type: ignore
from datetime import datetime, timezone
from cneura_ai.logger import logger
from cneura_ai.messaging import MessageWorker
from cneura_ai.tool_deploy import ToolDeployer
from cneura_ai.utils import decode_base64, send_log
from cneura_ai.llm import GeminiLLM
from cneura_ai.memory import MemoryManager
from cneura_ai.credential import CredentialManager, SecureCredential
from cneura_ai.agent_design import AgentDesign



load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
INPUT_QUEUE = os.getenv("INPUT_QUEUE", "tool.code.deploy")
OUTPUT_QUEUE = os.getenv("OUTPUT_QUEUE", "meta.agent.in")
ERROR_QUEUE = os.getenv("ERROR_QUEUE", "tool.deploy.error")
REMOTE_URL = os.getenv("REMOTE_URL") 
MONGO_URI = os.getenv("MONGO_URI")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LOGGER_SERVER = os.getenv("LOGGER_SERVER", "ws://logger:8765")
CHROMA_HOST = os.getenv("CHROMA_HOST", "chromadb")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", 8888))
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
SECRET_KEY = os.getenv("SECRET_KEY", "my_secret")
TOOL_MEMORY_NAMESPACE = os.getenv("TOOL_MEMORY_NAMESPACE","tool")


if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing! Check your .env file.")


def main(message):
    data = message.get("body")
    task_id = data.get("task_id")
    code = data.get("code")
    design_id = data.get("design_id")
    tool_name = data.get("tool_name")
    credential_id = data.get("credential_id", None)
    timestamp = str(datetime.now(timezone.utc))

    try:
        logger.info(f"Received task {task_id}: Start deploying...")
        asyncio.run(send_log("tool_deploy", f"Received task {task_id}: Start deploying...", LOGGER_SERVER))
        code = decode_base64(code)
        schema = {
            "name": {
                "description": "A short, clear name for the tool class, ideally using camel case or PascalCase."
            },
            "description": {
                "description": "A concise summary of what the tool class does, including its purpose, input behavior, and output behavior."
            },
            "params": {
                "description": "A list of parameters with their types, required when running or invoking the tool class."
            },
            "returns": {
                "description": "The expected return type or output of the tool class after execution."
            },
            "credentials": {
                "description": "A list of third-party credentials required for the tool class to function properly (e.g., API keys, access tokens, client secrets). Specify the service name and credential type needed."
            }
        }

        llm = GeminiLLM(api_key=GEMINI_API_KEY)
        prompt = [("system", "Your job is that give suitable name and description for the given python class. the given class is use as tool for llms. The description must be detailed and llms must can understand what does this tool. "),
                  ("user", f"Tool class: {code}")]
        
        result = llm.query(prompt, schema)
        tool = result.get("data")
        name = tool.get("name", "tool")
        name = name.replace(" ", "-")
        name = name.lower()
        tool.update(name=name)
        description = tool.get("description", "description")

        manager = CredentialManager(secret_key=SECRET_KEY, mongo_uri=MONGO_URI)
        if credential_id is not None:
            with SecureCredential(manager.get_credentials(credential_id)) as creds:
                register_id, run, doc, parameters = ToolDeployer(code, REMOTE_URL, MONGO_URI, name, description=tool, configs=creds).deploy()

        else:
            register_id, run, doc, parameters = ToolDeployer(code, REMOTE_URL, MONGO_URI, name, tool).deploy()
        logger.info(f"completed task {task_id}: Tool deployed!")

        memory_manager = MemoryManager(host=CHROMA_HOST, port=CHROMA_PORT, llm=llm)
        asyncio.run(memory_manager.store_to_abilities(TOOL_MEMORY_NAMESPACE, register_id, description))
        asyncio.run(send_log("tool_deploy", f"the tool description saved - {register_id} - {description}", LOGGER_SERVER))

        asyncio.run(send_log("tool_deploy", f"completed task {task_id}: {name} Tool deployed! - {description}", LOGGER_SERVER))

        if design_id and tool_name:
            logger.info("updating the design state.")
            agent_design = AgentDesign(llm=llm, mongo_uri=MONGO_URI, mq=False)
            response = agent_design.update_tool_by_design_id(design_id, tool_name, updates={"status": "generated", "run": run, "doc": doc, "parameters": parameters})
            if response.get("success", False):
                logger.info(response.get("message"))
            else:
                logger.error(response.get("error"))

        return {"data":{"header":{"from": "tool_deploy", "timestamp":timestamp},"body":{"task_id": task_id, "status": "completed", **data}}, "queue": OUTPUT_QUEUE}

    except Exception as e:
        logger.error(f"Error processing task {task_id}: {e}")
        return {"data":{"header":{"from": "tool_deploy", "timestamp":timestamp},"body":{"task_id": task_id, "error": str(e)}}, "queue": ERROR_QUEUE}

if __name__ == "__main__":
    try:
        worker = MessageWorker(
            input_queue=INPUT_QUEUE,
            process_message=main,
            host=RABBITMQ_HOST,
            username=RABBITMQ_USER,
            password=RABBITMQ_PASS
        )
        logger.info("MessageWorker started successfully.")
        worker.start()
    except Exception as e:
        logger.error(f"Failed to start MessageWorker: {e}")
