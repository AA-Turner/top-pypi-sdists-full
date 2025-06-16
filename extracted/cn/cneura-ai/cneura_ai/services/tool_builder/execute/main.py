import os
import asyncio
import redis
from dotenv import load_dotenv  # type: ignore
from datetime import datetime, timezone
from cneura_ai.logger import logger
from cneura_ai.messaging import MessageWorker
from cneura_ai.executor import CodeExecutor
from cneura_ai.code import CodeGenerator
from cneura_ai.llm import GeminiLLM
from cneura_ai.utils import decode_base64, send_log
from cneura_ai.credential import CredentialManager, SecureCredential

load_dotenv()


RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
REMOTE_URL = os.getenv("REMOTE_URL") 
INPUT_QUEUE = os.getenv("INPUT_QUEUE", "tool.code.exec")
OUTPUT_QUEUE = os.getenv("OUTPUT_QUEUE", "tool.code.debug")
OUT_QUEUE = os.getenv("OUTPUT_QUEUE", "tool.code.deploy")
ERROR_QUEUE = os.getenv("ERROR_QUEUE", "tool.exec.error")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LOGGER_SERVER = os.getenv("LOGGER_SERVER", "ws://logger:8765")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
SECRET_KEY = os.getenv("SECRET_KEY", "my_secret")

redis_client = redis.Redis.from_url(f"redis://{REDIS_HOST}:6379")

MAX_ITERATIONS = 9

def store_attempt(task_id, iteration, code, testcases, output, pass_rate):
    redis_client.zadd(f"task:{task_id}:codes", {code: pass_rate})
    attempt_key = f"task:{task_id}:attempts:{iteration}"
    redis_client.hset(attempt_key, mapping={
        "code": code,
        "testcases": testcases,
        "output": output,
        "pass_rate": pass_rate,
        "iteration": iteration
    })
    redis_client.rpush(f"task:{task_id}:attempts", attempt_key)

def get_best_code(task_id):
    best = redis_client.zrevrange(f"task:{task_id}:codes", 0, 0, withscores=True)
    if best:
        code, score = best[0]
        return code.decode()
    return None

def clear_task_cache(task_id):
    keys = redis_client.lrange(f"task:{task_id}:attempts", 0, -1)
    for key in keys:
        redis_client.delete(key)
    redis_client.delete(f"task:{task_id}:attempts")
    redis_client.delete(f"task:{task_id}:codes")

def main(message):
    data = message.get("body")
    task_id = data.get("task_id")
    iterations = data.get("iterations", 0)
    credential_id = data.get("credential_id", None)
    timestamp = str(datetime.now(timezone.utc))


    try:
        code = decode_base64(data.get("code", ""))
        testcases = decode_base64(data.get("testcases", ""))
        if not code or not testcases:
            raise ValueError("The code or testcases decode failed.")
    except Exception as e:
        logger.error(f"Task {task_id} failed: Invalid Base64 encoding - {e}")
        asyncio.run(send_log("code_execute", f"Task {task_id} failed: Invalid Base64 encoding - {e}", LOGGER_SERVER))
        return {"data": {"header":{"from": "code_exec", "timestamp":timestamp},"body":{"task_id": task_id, "status": "error", "detail": str(e)}}, "queue": ERROR_QUEUE}

    language = data.get("language", "python")
    memory_limit = data.get("memory_limit", 256)
    dependencies = data.get("dependencies", [])

    if iterations >= MAX_ITERATIONS:
        logger.info(f"Max iteration limit exceeded for task {task_id}.")
        asyncio.run(send_log("code_execute", f"Max iteration limit exceeded for task {task_id}.", LOGGER_SERVER))

        best_code = get_best_code(task_id)
        clear_task_cache(task_id)

        return {"data":{"header":{"from": "code_exec", "timestamp":timestamp},"body": {
                        "task_id": task_id,
                        "status": "completed",
                        "code": best_code,
                        **data
                    }}, "queue": OUT_QUEUE}

    logger.info(f"Received task {task_id}: Executing {language} code...")
    asyncio.run(send_log("code_execute", f"Received task {task_id}: {iterations} Executing {language} code...", LOGGER_SERVER))

    try:
        manager = CredentialManager(secret_key=SECRET_KEY, mongo_uri=MONGO_URI)
        executor = CodeExecutor(image="python:3.12-slim", remote_url=REMOTE_URL, memory_limit_mb=memory_limit)
        if credential_id is not None:
            with SecureCredential(manager.get_credentials(credential_id)) as creds:
                error, output = executor.execute(code, testcases, dependencies or [], creds)
        else:
            error, output = executor.execute(code, testcases, dependencies or [], {})

        if error:
            logger.error(f"Task {task_id} failed: {error}")
            asyncio.run(send_log("code_execute", f"Task {task_id} failed: {error}", LOGGER_SERVER))
            return {"data": {"header":{"from": "code_exec", "timestamp":timestamp},"body":{"task_id": task_id, "status": "error", "detail": str(error),
                                 "code": data.get("code", ""), "testcases": data.get("testcases", "")}},
                        "queue": ERROR_QUEUE}

        logger.info(f"Task {task_id} completed successfully\nOutput:\n{output}")
        asyncio.run(send_log("code_execute", f"Task {task_id} completed successfully\nOutput:\n{output}", LOGGER_SERVER))

        llm = GeminiLLM(api_key=GEMINI_API_KEY)
        generator = CodeGenerator(llm)

        result_data = generator.execution_result_processor(output)
        logger.info(f"Procceded result : {result_data}")
        total = int(result_data.get("total_testcases", 1))
        passed = total - int(result_data.get("fail_testcases", 0))
        pass_rate = passed / total if total > 0 else 0

        logger.info(f"Pass Rate : {pass_rate * 100:.2f}% ✅")
        asyncio.run(send_log("code_execute", f"Pass Rate : {pass_rate * 100:.2f}% ✅", LOGGER_SERVER))

        store_attempt(task_id, iterations, data.get("code", ""), data.get("testcases", ""), output, pass_rate)

        if pass_rate < 0.9:
            data.pop("iterations")
            logger.info(f"Low pass rate.")
            return {"data": {"header":{"from": "code_exec", "timestamp":timestamp},"body":{
                    "task_id": task_id,
                    "status": "completed",
                    "testcases": data.get("testcases", ""),
                    "iterations": iterations + 1, 
                    "code": data.get("code", ""),
                    "detail":output,
                    **data
                }}, "queue": OUTPUT_QUEUE}
        else:
            logger.info(f"High pass rate.")
            clear_task_cache(task_id)
            return {"data": {"header":{"from": "code_exec", "timestamp":timestamp},"body":{
                    "task_id": task_id,
                    "status": "completed",
                    "code": data.get("code", ""),
                    **data
                }}, "queue": OUT_QUEUE}


    except Exception as e:
        logger.error(f"Task {task_id} failed: {e}")
        asyncio.run(send_log("code_execute", f"Task {task_id} failed: {e}", LOGGER_SERVER))
        return {"data": {"header":{"from": "code_exec", "timestamp":timestamp},"body":{"task_id": task_id, "status": "error", "detail": str(e)}}, "queue": ERROR_QUEUE}


if __name__ == "__main__":
    worker = MessageWorker(
        input_queue=INPUT_QUEUE,
        process_message=main,
        host=RABBITMQ_HOST,
        username=RABBITMQ_USER,
        password=RABBITMQ_PASS
    )
    worker.start()
