import os
import asyncio
from dotenv import load_dotenv  # type: ignore
from datetime import datetime, timezone
from cneura_ai.logger import logger
from cneura_ai.messaging import MessageWorker
from cneura_ai.code import CodeGenerator
from cneura_ai.utils import decode_base64, send_log
from cneura_ai.llm import GeminiLLM


load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
INPUT_QUEUE = os.getenv("INPUT_QUEUE", "tool.code.deps_in")
OUTPUT_QUEUE = os.getenv("OUTPUT_QUEUE", "tool.code.exec")
DEPEND_QUEUE = os.getenv("DEPEND_QUEUE", "tool.code.deps_out")
ERROR_QUEUE = os.getenv("ERROR_QUEUE", "tool.deps.error")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LOGGER_SERVER = os.getenv("LOGGER_SERVER", "ws://logger:8765")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing! Check your .env file.")


def main(message):
    data = message.get("body")
    task_id = data.get("task_id")
    code = data.get("code")
    testcases = data.get("testcases")
    iterations = data.get("iterations", 0)
    timestamp = str(datetime.now(timezone.utc))

    if not code or not testcases:
        logger.error(f"code or testcases is missing for task_id: {task_id}")
        asyncio.run(send_log("code_dependencies", f"code or testcases is missing for task_id: {task_id}", LOGGER_SERVER))
        return {
            "data": {
                "header": {"from": "code_test", "timestamp": timestamp},
                "body": {"task_id": task_id, "error": "Missing code or testcases"}
            },
            "queue": ERROR_QUEUE
        }

    try:
        logger.info(f"Task {task_id} started processing.")
        asyncio.run(send_log("code_dependencies", f"Task {task_id} started processing.", LOGGER_SERVER))

        llm = GeminiLLM(api_key=GEMINI_API_KEY)
        generator = CodeGenerator(llm=llm)

        decoded_code = decode_base64(code)
        decoded_testcases = decode_base64(testcases)

        dependencies = generator.extract_dependencies(decoded_code)
        logger.info(f"Extracted third-party libraries in {task_id}: {dependencies}")
        asyncio.run(send_log("code_dependencies", f"Extracted third-party libraries in {task_id}: {dependencies}", LOGGER_SERVER))

        configs = generator.identify_secrets(decoded_code, decoded_testcases)
        has_configs = configs.get("has")

        use_depend_queue = (
            (isinstance(has_configs, bool) and has_configs) or
            (isinstance(has_configs, str) and has_configs.upper() == "TRUE")
        )

        if use_depend_queue:
            logger.info(f"Extracted configurations in {task_id}: {configs}")
            asyncio.run(send_log("code_dependencies", f"Extracted configurations in {task_id}: {configs}", LOGGER_SERVER))

        return {
            "data": {
                "header": {"from": "code_test", "timestamp": timestamp},
                "body": {
                    "task_id": task_id,
                    "code": code,
                    "testcases": testcases,
                    "dependencies": dependencies or [],
                    "configs": configs,
                    "iterations": iterations,
                    **data
                }
            },
            "queue": DEPEND_QUEUE if use_depend_queue else OUTPUT_QUEUE
        }

    except Exception as e:
        logger.error(f"Error processing task {task_id}: {e}")
        asyncio.run(send_log("code_dependencies", f"Error processing task {task_id}: {e}", LOGGER_SERVER))
        return {
            "data": {
                "header": {"from": "code_test", "timestamp": timestamp},
                "body": {"task_id": task_id, "error": str(e)}
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
