import os
import asyncio
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
INPUT_QUEUE = os.getenv("INPUT_QUEUE", "tool.code.debug")
OUTPUT_QUEUE = os.getenv("OUTPUT_QUEUE", "tool.code.test")
ERROR_QUEUE = os.getenv("ERROR_QUEUE", "tool.debug.error")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LOGGER_SERVER = os.getenv("LOGGER_SERVER", "ws://logger:8765")


if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing! Check your .env file.")


def main(message):
    data = message.get("body")
    task_id = data.get("task_id")
    code = data.get("code")
    testcases = data.get("testcases")
    detail = data.get("detail")
    timestamp = str(datetime.now(timezone.utc))



    if not code or not testcases:
        logger.error(f"code or testcases is missing for task_id: {task_id}")
        asyncio.run(send_log("code_debug", f"code or testcases is missing for task_id: {task_id}",LOGGER_SERVER))
        return {"data":{"header":{"from": "code_debug", "timestamp":timestamp},"body":{"task_id": task_id, "error": "Missing code or testcases"}}, "queue": ERROR_QUEUE}
        
    try:
        logger.info(f"Task {task_id} started processing.")
        asyncio.run(send_log("code_debug", f"Task {task_id} started processing.",LOGGER_SERVER))

        
        decoded_code = decode_base64(code)
        if not decoded_code:
            logger.error("The code decode failed.")
            asyncio.run(send_log("code_debug", "The code decode failed.",LOGGER_SERVER))
            return {"data":{"header":{"from": "code_debug", "timestamp":timestamp},"body":{"task_id": task_id, "error":"The code decode failed."}}, "queue": ERROR_QUEUE}
        

        llm = GeminiLLM(api_key=GEMINI_API_KEY)
        generator = CodeGenerator(llm=llm)
        instructions = str(generator.instruct(decoded_code, detail))
        logger.info(f"The debug instructions generated.")
        asyncio.run(send_log("code_debug", f"The debug instructions generated.",LOGGER_SERVER))

        code = generator.debug(decoded_code, instructions)
        logger.info(f"The code debugged.")
        asyncio.run(send_log("code_debug", f"The code debugged.",LOGGER_SERVER))
        encoded_code = encode_base64(code)
        data.pop("code")
        data.pop("testcases")
        data.pop("detail")

        if not encoded_code:
            logger.error("The code encode failed.")
            asyncio.run(send_log("code_debug", "The code encode failed.",LOGGER_SERVER))
            return {"data":{"header":{"from": "code_debug", "timestamp":timestamp},"body":{"task_id": task_id, "error": "The code encode failed."}}, "queue": ERROR_QUEUE}

        return {"data":{"header":{"from": "code_debug", "timestamp":timestamp},"body":{"task_id": task_id, "code": encoded_code, **data }}, "queue": OUTPUT_QUEUE}

    
    except Exception as e:
        logger.error(f"Error processing task {task_id}: {e}")
        asyncio.run(send_log("code_debug", f"Error processing task {task_id}: {e}" ,LOGGER_SERVER))
        return {"data":{"header":{"from": "code_debug", "timestamp":timestamp},"body":{"task_id": task_id, "error": str(e)}}, "queue": ERROR_QUEUE}

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
