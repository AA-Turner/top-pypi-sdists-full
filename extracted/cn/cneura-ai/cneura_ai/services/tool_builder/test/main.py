import asyncio
import os
from dotenv import load_dotenv  # type: ignore
from datetime import datetime, timezone
from cneura_ai.logger import logger
from cneura_ai.messaging import MessageWorker
from cneura_ai.code import CodeGenerator
from cneura_ai.utils import decode_base64, encode_base64, send_log
from cneura_ai.llm import GeminiLLM

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
INPUT_QUEUE = os.getenv("INPUT_QUEUE", "tool.code.test")
OUTPUT_QUEUE = os.getenv("OUTPUT_QUEUE", "tool.code.deps")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ERROR_QUEUE = os.getenv("ERROR_QUEUE", "tool.test.error")
LOGGER_SERVER = os.getenv("LOGGER_SERVER", "ws://logger:8765")



if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing! Check your .env file.")

def main(message):
    data = message.get("body")
    task_id = data.get("task_id")
    code = data.get("code")
    iterations = data.get("iterations", 0)
    timestamp = str(datetime.now(timezone.utc))


    if not code:
        logger.error(f"code is missing for task_id: {task_id}")
        asyncio.run(send_log("code_test", f"code is missing for task_id: {task_id}",LOGGER_SERVER))
        return {"data":{"header":{"from": "code_test", "timestamp":timestamp},"body":{"task_id": task_id, "error": "Missing code"}}, "queue": ERROR_QUEUE}
    
    try:
        logger.info(f"Task {task_id} started processing.")
        asyncio.run(send_log("code_test", f"Task {task_id} started processing.",LOGGER_SERVER))
        
        llm = GeminiLLM(api_key=GEMINI_API_KEY)
        generator = CodeGenerator(llm=llm)

        decoded_code = decode_base64(code)
        testcases = generator.generate_test_script(decoded_code)
        logger.info(f"Generated test script for code {task_id}: {testcases}")
        asyncio.run(send_log("code_test", f"Generated test script for code {task_id}",LOGGER_SERVER))

        logger.info(f"Task {task_id} generated test script.")
        asyncio.run(send_log("code_test", f"Task {task_id} generated test script.",LOGGER_SERVER))

        encoded_test_script = encode_base64(testcases)
        logger.info(f"Task {task_id} test script encoded.")
        asyncio.run(send_log("code_test", f"Task {task_id} test script encoded.",LOGGER_SERVER))

        
        return {"data":{"header":{"from": "code_test", "timestamp":timestamp},"body":{"task_id": task_id, "code": code, "testcases": encoded_test_script, "iterations":iterations, **data}}, "queue": OUTPUT_QUEUE}
    
    except Exception as e:
        logger.error(f"Error processing task {task_id}: {e}")
        asyncio.run(send_log("code_test", f"Error processing task {task_id}: {e}",LOGGER_SERVER))
        return {"data":{"header":{"from": "code_test", "timestamp":timestamp},"body":{"task_id": task_id, "error": str(e)}}, "queue": ERROR_QUEUE}

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
