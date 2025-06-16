from fastapi import APIRouter, Depends, HTTPException
from app.database_hub import DatabaseHub
import aio_pika
import json
import asyncio
from app.dependencies import get_db_hub, DatabaseHub

router = APIRouter(prefix="/queue", tags=["Queues"])

async def get_rabbitmq_connection(db: DatabaseHub):
    if not db.rabbitmq_connection or db.rabbitmq_connection.is_closed:
        await db.connect_rabbitmq()
    return db.rabbitmq_connection


@router.get("/")
async def list_queues(db: DatabaseHub = Depends(get_db_hub)):
    try:
        await db.load_config()
        queues = await db.list_rabbitmq_queues()
        return {"queues": queues}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recieve/{queue_name}/messages")
async def get_queue_message(queue_name: str, db: DatabaseHub = Depends(get_db_hub)):
    """
    Fetch one message from the specified queue for inspection (does not ack, so message is requeued).
    """
    conn = await get_rabbitmq_connection(db)
    try:
        channel = await conn.channel()
        queue = await channel.declare_queue(queue_name, passive=True)

        incoming_message = await queue.get(no_ack=False, timeout=2)
        if incoming_message is None:
            return {"message": None, "info": "Queue is empty"}

        body = incoming_message.body.decode("utf-8")

        await incoming_message.nack(requeue=True)

        try:
            body = json.loads(body)
        except Exception:
            pass

        return {"message": body}
    except aio_pika.exceptions.QueueNotFound:
        raise HTTPException(status_code=404, detail=f"Queue '{queue_name}' not found")
    except asyncio.TimeoutError:
        return {"message": None, "info": "No message received in timeout period"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
