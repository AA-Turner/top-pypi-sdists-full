from cneura_ai.logger import logger
import base64
import asyncio
import websockets
import json


def decode_base64(value:str):
    try:
        return base64.b64decode(value).decode("utf-8")
    except Exception as e:
        logger.error(f"Invalid Base64 encoding - {e}")
        return False
    
def encode_base64(value:str):
    try:
        return base64.b64encode(value.encode("utf-8")).decode("utf-8")
    except Exception as e:
        logger.error(f"Invalid string - {e}")
        return False
    


async def send_log(service, message, websocket_server="ws://localhost:8765", max_retries=5):
    retries = 0

    while retries < max_retries:
        try:
            async with websockets.connect(websocket_server) as websocket:
                logger.info(f"✅ Logger server Connected")

                log_data = {
                    "service": service,
                    "level": "info",
                    "message": message
                }

                await websocket.send(json.dumps(log_data))
                logger.info(f"📤 Sent log: {log_data}")

                return  None

        except Exception as e:
            retries += 1
            logger.error(f"⚠️ Connection failed ({retries}/{max_retries}) - Retrying in 3s...")
            await asyncio.sleep(3)

    logger.error("❌ Could not connect after max retries. Exiting...")