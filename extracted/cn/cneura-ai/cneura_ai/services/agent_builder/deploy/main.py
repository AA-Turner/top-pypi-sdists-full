import os
import uuid
import requests
from dotenv import load_dotenv  
from datetime import datetime, timezone
from cneura_ai.logger import logger
from pymongo import MongoClient
from cneura_ai.messaging import MessageWorker
from cneura_ai.agent_deploy import AgentDeployer
from cneura_ai.memory import AgentsMemory
from cneura_ai.agent_registry import AgentRegistry
from cneura_ai.llm import GeminiLLM

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
INPUT_QUEUE = os.getenv("INPUT_QUEUE", "agent.deploy.in")
OUTPUT_QUEUE = os.getenv("OUTPUT_QUEUE", "agent.deploy.out")
ERROR_QUEUE = os.getenv("ERROR_QUEUE", "agent.deploy.error")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LOGGER_SERVER = os.getenv("LOGGER_SERVER", "ws://logger:8765")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
CHROMA_HOST = os.getenv("CHROMA_HOST", "chromadb")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", 8888))
REMOTE_URL = os.getenv("REMOTE_URL") 
AGENT_MEMORY_NAMESPACE = os.getenv("AGENT_MEMORY_NAMESPACE", "agent")
DEPLOY_OUTPUT_DIR = "./output"

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing! Check your .env file.")


def main(message):
    data = message.get("body")
    task_id = data.get("task_id")
    design_id = data.get("design_id")
    timestamp = str(datetime.now(timezone.utc))

    try:
        logger.info(f"Task {task_id} started processing.")

        client = MongoClient(MONGO_URI)
        db = client["agentdb"]
        collection = db["agent_designs"]
        context = collection.find_one({"design_id": design_id})

        if not context:
            logger.error(f"No design found for design_id: {design_id}")
            return {
                "data": {
                    "header": {"from": "agent_design", "timestamp": timestamp},
                    "body": {
                        "task_id": task_id,
                        "error": f"Design not found for design_id {design_id}"
                    }
                },
                "queue": ERROR_QUEUE
            }

        tools = context.get("tools", [])
        if not tools:
            logger.warning(f"No tools defined for design_id: {design_id}")
            return {
                "data": {
                    "header": {"from": "agent_design", "timestamp": timestamp},
                    "body": {
                        "task_id": task_id,
                        "error": f"No tools found in design_id {design_id}"
                    }
                },
                "queue": ERROR_QUEUE
            }

        incomplete = [tool for tool in tools if tool.get("status") != "completed"]
        if incomplete:
            logger.warning(f"Some tools are not completed for design_id: {design_id}")
            return {
                "data": {
                    "header": {"from": "agent_design", "timestamp": timestamp},
                    "body": {
                        "task_id": task_id,
                        "error": f"Not all tools are completed for design_id {design_id}"
                    }
                },
                "queue": ERROR_QUEUE
            }
        
        def create_tool_func(run_url, param_names):
            import requests

            def tool_func(*args, **kwargs):
                if len(args) > len(param_names):
                    raise TypeError(f"Too many positional arguments: expected max {len(param_names)}, got {len(args)}")
                payload = dict(zip(param_names, args))
                for k in kwargs:
                    if k not in param_names:
                        raise TypeError(f"Unexpected keyword argument: {k}")
                    payload[k] = kwargs[k]

                response = requests.post(run_url, json=payload)
                response.raise_for_status()
                return response.json()

            return tool_func
        
        tool_docs = []
        tool_funcs = {}

        for tool in context.get("tools", []):
            tool_name = tool.get("tool_name")
            doc_url = tool.get("doc")
            run_url = tool.get("run")
            parameters = tool.get("parameters", [])

            if doc_url:
                try:
                    response = requests.get(doc_url)
                    response.raise_for_status()
                    json_data = response.json()
                    tool_docs.append(json_data)
                except Exception as e:
                    logger.error(f"Failed to fetch tool from {doc_url}: {e}")
                    raise ValueError(f"Invalid doc_url in tool: {doc_url}")
            else:
                tool_docs.append(tool)

            if run_url:
                tool_funcs[tool_name] = create_tool_func(run_url, parameters)

        queue_prefix =  f"{context["agent_name"]}.{str(uuid.uuid4())}"
        context["tool_docs"] = tool_docs
        context["tools"] = tool_funcs
        context["input_queue"] = f"{queue_prefix}.in"
        context["output_queue"] = f"{queue_prefix}.out"
        context["error_queue"] = f"{queue_prefix}.error" 

        configs = {
            "agent": context,
            "env": {
                "RABBITMQ_HOST" : os.getenv("RABBITMQ_HOST", "localhost"),
                "RABBITMQ_USER" : os.getenv("RABBITMQ_USER", "guest"),
                "RABBITMQ_PASS" : os.getenv("RABBITMQ_PASS", "guest"),
                "INPUT_QUEUE" : f"{queue_prefix}.in",
                "OUTPUT_QUEUE" : f"{queue_prefix}.out",
                "ERROR_QUEUE" : f"{queue_prefix}.error",
                "MONGO_URI" : os.getenv("MONGO_URI"),
                "GEMINI_API_KEY" : os.getenv("GEMINI_API_KEY"),
                "CHROMA_HOST" : os.getenv("CHROMA_HOST", "chromadb"),
                "CHROMA_PORT" : os.getenv("CHROMA_PORT", 8000),
                "RESEARCH_API_URL" : os.getenv("RESEARCH_API_URL", "http://host.docker.internal:8500/search"),
                "SHELL_EXEC_API_URL" : os.getenv("SHELL_EXEC_API_URL", "http://host.docker.internal:8600/command/run"),
                "TOOL_API_URL" : os.getenv("TOOL_API_URL", "http://host.docker.internal:8800/tools/query"),
                "AGENT_ID": queue_prefix
            }
        }

        llm = GeminiLLM(api_key=GEMINI_API_KEY)

        agents_memory = AgentsMemory(host=CHROMA_HOST, port=CHROMA_PORT, namespace=AGENT_MEMORY_NAMESPACE)
        registry = AgentRegistry(mongo_uri=MONGO_URI, memory=agents_memory)
        deployer = AgentDeployer(agent_registry=registry, remote_url=REMOTE_URL)
        agent_id = queue_prefix
        output_dir = os.path.join(DEPLOY_OUTPUT_DIR, agent_id)

        agent_name = context.get("agent_name")
        if not agent_name:
            raise ValueError("Missing agent_name in design document.")

        image_tag = f"{agent_name.lower()}:{agent_id[:8]}"
        container_name = f"{agent_name.lower()}-container-{agent_id[:6]}"

        container, deployed_agent_id = deployer.deploy(
            output_path=output_dir,
            image_tag=image_tag,
            container_name=container_name,
            context=configs
        )

        return {
            "data": {
                "header": {"from": "agent_design", "timestamp": timestamp},
                "body": {
                    "task_id": task_id,
                    "message": "Agent created and deployed successfully.",
                    "agent_id": deployed_agent_id,
                    "container_id": container.id,
                    "image_tag": image_tag
                }
            },
            "queue": OUTPUT_QUEUE
        }

    except Exception as e:
        logger.error(f"Error processing task {task_id}: {e}")
        return {
            "data": {
                "header": {"from": "agent_design", "timestamp": timestamp},
                "body": {
                    "task_id": task_id,
                    "error": str(e)
                }
            },
            "queue": ERROR_QUEUE
        }


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
