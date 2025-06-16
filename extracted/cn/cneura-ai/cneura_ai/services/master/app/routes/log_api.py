from fastapi import APIRouter, HTTPException, Query, WebSocket, WebSocketDisconnect, Depends, status
from typing import List, Dict, Any, Optional
import json
import uuid
import datetime

from fastapi.responses import HTMLResponse

from app.dependencies import DatabaseHub, get_db_hub  

router = APIRouter(prefix="/log", tags=["Log"])


class Subscriber:
    def __init__(self, websocket: WebSocket, task_id_filter: Optional[str] = None):
        self.websocket = websocket
        self.task_id_filter = task_id_filter


class ConnectionManager:
    def __init__(self):
        self.subscribers: List[Subscriber] = []

    async def connect(self, websocket: WebSocket, task_id_filter: Optional[str]):
        await websocket.accept()
        self.subscribers.append(Subscriber(websocket, task_id_filter))

    def disconnect(self, websocket: WebSocket):
        self.subscribers = [s for s in self.subscribers if s.websocket != websocket]

    async def broadcast(self, message: Dict[str, Any]):
        serialized = json.dumps(message)
        for subscriber in self.subscribers:
            if (
                subscriber.task_id_filter is None
                or subscriber.task_id_filter == message.get("task_id")
            ):
                await subscriber.websocket.send_text(serialized)


manager = ConnectionManager()


@router.websocket("/ws")
async def websocket_log_endpoint(
    websocket: WebSocket,
    task_id: Optional[str] = None,
    db_hub: DatabaseHub = Depends(get_db_hub),
):
    await db_hub.load_config()
    await db_hub.connect_mongodb()

    await manager.connect(websocket, task_id_filter=task_id)

    await db_hub.mongo_client["client_connections"].insert_one({
        "event": "connect",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "task_id": task_id,
        "client": websocket.client.host,
    })

    try:
        while True:
            raw_data = await websocket.receive_text()
            try:
                data = json.loads(raw_data)
                data["timestamp"] = datetime.datetime.utcnow().isoformat()
                data["event_id"] = str(uuid.uuid4())

                print("[LOG EVENT]", data)

                await db_hub.mongo_client["task_logs"].insert_one(data)

                await manager.broadcast(data)

            except json.JSONDecodeError:
                await websocket.send_text(
                    json.dumps({"type": "error", "message": "Invalid JSON"})
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("WebSocket disconnected")
        await db_hub.mongo_client["client_connections"].insert_one({
            "event": "disconnect",
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "task_id": task_id,
            "client": websocket.client.host,
        })


@router.get("/history")
async def get_log_history(
    task_id: str = Query(...),
    start_time: Optional[str] = Query(None),
    end_time: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db_hub: DatabaseHub = Depends(get_db_hub),
):
    try:
        await db_hub.load_config()
        await db_hub.connect_mongodb()

        filters = {"task_id": task_id}
        if start_time or end_time:
            filters["timestamp"] = {}
            if start_time:
                filters["timestamp"]["$gte"] = start_time
            if end_time:
                filters["timestamp"]["$lte"] = end_time

        logs_cursor = db_hub.mongo_client["task_logs"].find(filters).sort("timestamp", 1).skip(skip).limit(limit)
        logs = await logs_cursor.to_list(length=limit)

        for log in logs:
            log["_id"] = str(log["_id"])

        return {
            "task_id": task_id,
            "logs": logs,
            "meta": {
                "skip": skip,
                "limit": limit,
                "count": len(logs),
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/dashboard", response_class=HTMLResponse)
async def serve_log_dashboard():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Task Log Dashboard</title>
        <style>
            body { font-family: sans-serif; margin: 2rem; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
            th { background-color: #eee; }
        </style>
    </head>
    <body>
        <h1>Task Log Dashboard</h1>
        <label for="task_id">Task ID:</label>
        <input type="text" id="task_id" value="my-task-id">
        <button onclick="loadLogs()">Load Logs</button>
        <table id="logTable">
            <thead><tr><th>Timestamp</th><th>Status</th><th>Message</th></tr></thead>
            <tbody></tbody>
        </table>
        <script>
            async function loadLogs() {
                const taskId = document.getElementById('task_id').value;
                const response = await fetch(`/log/history?task_id=${taskId}`);
                const data = await response.json();
                const tbody = document.querySelector("#logTable tbody");
                tbody.innerHTML = "";
                data.logs.forEach(log => {
                    const row = `<tr>
                        <td>${log.timestamp}</td>
                        <td>${log.status}</td>
                        <td>${log.message || ""}</td>
                    </tr>`;
                    tbody.insertAdjacentHTML('beforeend', row);
                });
            }
        </script>
    </body>
    </html>
    """