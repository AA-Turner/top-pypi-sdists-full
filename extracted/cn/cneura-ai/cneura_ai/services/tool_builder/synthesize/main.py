import os
import asyncio
from dotenv import load_dotenv  
from datetime import datetime, timezone
from cneura_ai.logger import logger
from cneura_ai.messaging import MessageWorker
from cneura_ai.code import CodeGenerator
from cneura_ai.utils import encode_base64, send_log
from cneura_ai.llm import GeminiLLM

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
INPUT_QUEUE = os.getenv("INPUT_QUEUE", "tool.code.synth")
OUTPUT_QUEUE = os.getenv("OUTPUT_QUEUE", "tool.code.test")
ERROR_QUEUE = os.getenv("ERROR_QUEUE", "tool.synth.error")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LOGGER_SERVER = os.getenv("LOGGER_SERVER", "ws://logger:8765")


if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing! Check your .env file.")

def main(message):
    data = message.get("body")
    task_id = data.get("task_id")
    task = data.get("task_description")
    timestamp = str(datetime.now(timezone.utc))

    if not task:
        logger.error(f"Task is missing for task_id: {task_id}")
        asyncio.run(send_log("code_synthesize", f"Task is missing for task_id: {task_id}",LOGGER_SERVER))
        return {"data":{"header":{"from": "code_synthesize", "timestamp":timestamp},"body":{"task_id": task_id, "error": "Missing task description"}}, "queue": ERROR_QUEUE}
    
    try:
        logger.info(f"Task {task_id} started processing.")
        asyncio.run(send_log("code_synthesize", f"Task {task_id} started processing." ,LOGGER_SERVER))
        
        llm = GeminiLLM(api_key=GEMINI_API_KEY)
        generator = CodeGenerator(llm=llm)
        
        plan = generator.plan(task)
        logger.info(f"Generated plan for task {task_id}: {plan}")
        asyncio.run(send_log("code_synthesize", f"Generated plan for task {task_id}" ,LOGGER_SERVER))

        logger.info(f"Task {task_id} started synthesizing code.")
        asyncio.run(send_log("code_synthesize", f"Task {task_id} started synthesizing code." ,LOGGER_SERVER))
        synth = generator.synthesize(plan)
        
        encoded_code = encode_base64(synth)
        logger.info(f"Task {task_id} code synthesized and encoded.")
        asyncio.run(send_log("code_synthesize", f"Task {task_id} code synthesized and encoded." ,LOGGER_SERVER))

        logger.info(f"Task {task_id} completed successfully.")
        asyncio.run(send_log("code_synthesize", f"Task {task_id} completed successfully." ,LOGGER_SERVER))

        
        return {"data":{"header":{"from": "code_synthesize", "timestamp":timestamp},"body":{"task_id": task_id, "code": encoded_code, **data}}, "queue": OUTPUT_QUEUE}
    
    except Exception as e:
        logger.error(f"Error processing task {task_id}: {e}")
        asyncio.run(send_log("code_synthesize", f"Error processing task {task_id}: {e}" ,LOGGER_SERVER))
        return {"data":{"header":{"from": "code_synthesize", "timestamp":timestamp},"body":{"task_id": task_id, "error": str(e)}}, "queue": ERROR_QUEUE}

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
