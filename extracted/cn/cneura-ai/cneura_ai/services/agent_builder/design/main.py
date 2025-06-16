import os
from dotenv import load_dotenv  
from datetime import datetime, timezone
from cneura_ai.logger import logger
from cneura_ai.messaging import MessageWorker
from cneura_ai.agent_design import AgentDesign 
from cneura_ai.llm import GeminiLLM

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
INPUT_QUEUE = os.getenv("INPUT_QUEUE", "agent.design.in")
OUTPUT_QUEUE = os.getenv("OUTPUT_QUEUE", "agent.design.out")
OUT_QUEUE = os.getenv("OUTPUT_QUEUE", "tool.code.synth")
ERROR_QUEUE = os.getenv("ERROR_QUEUE", "agent.design.error")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LOGGER_SERVER = os.getenv("LOGGER_SERVER", "ws://logger:8765")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")


if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing! Check your .env file.")

def main(message):
    data = message.get("body")
    task_id = data.get("task_id")
    agent_description = data.get("agent_description")
    timestamp = str(datetime.now(timezone.utc))
    
    try:
        logger.info(f"Task {task_id} started processing.")
        
        llm = GeminiLLM(api_key=GEMINI_API_KEY)
        agent_design = AgentDesign(llm=llm, mongo_uri=MONGO_URI, host=RABBITMQ_HOST, username=RABBITMQ_USER, password=RABBITMQ_PASS, tool_queue=OUT_QUEUE)
        design = agent_design.generate_and_store_agent_design()
        
        return {"data":{"header":{"from": "agent_design", "timestamp":timestamp},"body":{"task_id": task_id, "design": design, **data}}, "queue": OUTPUT_QUEUE}
    
    except Exception as e:
        logger.error(f"Error processing task {task_id}: {e}")
        return {"data":{"header":{"from": "agent_design", "timestamp":timestamp},"body":{"task_id": task_id, "error": str(e)}}, "queue": ERROR_QUEUE}

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
