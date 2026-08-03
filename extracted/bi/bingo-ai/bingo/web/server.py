"""
Bingo Web UI Server - Cursor/OpenCode 스타일
FastAPI + WebSocket 실시간 인터페이스
"""
import os
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from datetime import datetime

from bingo import __version__
from bingo.core.workspace import WorkspaceManager

app = FastAPI(title="Bingo Web UI", version=__version__)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 전역 상태
workspace_manager = WorkspaceManager()
active_connections: List[WebSocket] = []
current_mode = "pentest"  # pentest or coding

# 정적 파일 서빙
static_dir = Path(__file__).parent / "static"
templates_dir = Path(__file__).parent / "templates"

if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


# ==================== Models ====================
class FileContent(BaseModel):
    path: str
    content: str


class ChatMessage(BaseModel):
    message: str
    mode: Optional[str] = None


# ==================== WebSocket ====================
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global current_mode

    await websocket.accept()
    active_connections.append(websocket)

    try:
        await websocket.send_json({
            "type": "system",
            "message": f"🎨 Bingo {__version__} 연결됨",
            "mode": current_mode,
            "timestamp": datetime.now().isoformat()
        })

        while True:
            data = await websocket.receive_json()
            message_type = data.get("type")

            if message_type == "chat":
                user_message = data.get("message", "")
                mode = data.get("mode", current_mode)

                await broadcast({
                    "type": "user_message",
                    "message": user_message,
                    "timestamp": datetime.now().isoformat()
                })

                await broadcast({
                    "type": "agent_thinking",
                    "message": "🤔 처리 중...",
                    "timestamp": datetime.now().isoformat()
                })

                # TODO: 실제 agent 호출
                response = f"[{mode} 모드] {user_message}에 대한 응답"

                await broadcast({
                    "type": "agent_response",
                    "message": response,
                    "timestamp": datetime.now().isoformat()
                })

            elif message_type == "mode_switch":
                new_mode = data.get("mode", "pentest")
                current_mode = new_mode

                await broadcast({
                    "type": "mode_changed",
                    "mode": new_mode,
                    "timestamp": datetime.now().isoformat()
                })

    except WebSocketDisconnect:
        active_connections.remove(websocket)
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        })


async def broadcast(message: Dict[str, Any]):
    """모든 연결된 클라이언트에게 메시지 브로드캐스트"""
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except:
            pass


# ==================== REST API ====================
@app.get("/")
async def root():
    """메인 페이지"""
    index_path = templates_dir / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return HTMLResponse("""
    <html>
        <head>
            <title>Bingo Web UI</title>
        </head>
        <body>
            <h1>🎨 Bingo Web UI</h1>
            <p>Template not found. Creating...</p>
        </body>
    </html>
    """)


@app.get("/api/workspace/tree")
async def get_workspace_tree():
    """작업 공간 파일 트리"""
    try:
        tree = workspace_manager.get_file_tree()
        return {"success": True, "tree": tree}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/file/read")
async def read_file(data: dict):
    """파일 읽기"""
    try:
        path = data.get("path")
        if not path:
            raise HTTPException(status_code=400, detail="path required")

        content = workspace_manager.read_file(path)
        return {
            "success": True,
            "path": path,
            "content": content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/file/write")
async def write_file(data: FileContent):
    """파일 쓰기/수정"""
    try:
        workspace_manager.write_file(data.path, data.content)

        await broadcast({
            "type": "file_updated",
            "path": data.path,
            "timestamp": datetime.now().isoformat()
        })

        return {"success": True, "path": data.path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/file/create")
async def create_file(data: dict):
    """파일 생성"""
    try:
        path = data.get("path")
        file_type = data.get("type", "file")

        if file_type == "directory":
            workspace_manager.create_directory(path)
        else:
            workspace_manager.create_file(path)

        await broadcast({
            "type": "file_created",
            "path": path,
            "file_type": file_type,
            "timestamp": datetime.now().isoformat()
        })

        return {"success": True, "path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/file/delete")
async def delete_file(data: dict):
    """파일 삭제"""
    try:
        path = data.get("path")
        workspace_manager.delete_file(path)

        await broadcast({
            "type": "file_deleted",
            "path": path,
            "timestamp": datetime.now().isoformat()
        })

        return {"success": True, "path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/file/rename")
async def rename_file(data: dict):
    """파일 이름 변경"""
    try:
        old_path = data.get("old_path")
        new_path = data.get("new_path")

        workspace_manager.rename_file(old_path, new_path)

        await broadcast({
            "type": "file_renamed",
            "old_path": old_path,
            "new_path": new_path,
            "timestamp": datetime.now().isoformat()
        })

        return {"success": True, "old_path": old_path, "new_path": new_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/status")
async def get_status():
    """현재 상태"""
    return {
        "version": __version__,
        "mode": current_mode,
        "workspace": workspace_manager.get_current_workspace(),
        "connected_clients": len(active_connections)
    }


@app.post("/api/mode")
async def switch_mode(data: dict):
    """모드 전환"""
    global current_mode
    new_mode = data.get("mode", "pentest")

    if new_mode not in ["pentest", "coding"]:
        raise HTTPException(status_code=400, detail="Invalid mode")

    current_mode = new_mode

    await broadcast({
        "type": "mode_changed",
        "mode": new_mode,
        "timestamp": datetime.now().isoformat()
    })

    return {"success": True, "mode": new_mode}


def _is_wsl2() -> bool:
    """WSL2 환경 감지"""
    try:
        with open("/proc/version", "r") as f:
            return "microsoft" in f.read().lower()
    except:
        return False


def start_web_server(event_bus=None, port: int = 8080) -> int:
    """
    백그라운드에서 웹 서버 시작
    Returns: 실제 사용된 포트 번호
    """
    import uvicorn
    import threading
    import socket

    # 포트 사용 가능 여부 확인
    def is_port_available(port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return True
            except OSError:
                return False

    # 사용 가능한 포트 찾기
    original_port = port
    while not is_port_available(port):
        port += 1
        if port > original_port + 100:  # 최대 100개 포트 시도
            raise RuntimeError("No available port found")

    def _run():
        uvicorn.run(app, host="127.0.0.1", port=port, log_level="error")

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()

    return port


def run_server(host: str = "127.0.0.1", port: int = 8080):
    """서버 실행 (직접 실행용)"""
    import uvicorn
    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║  🎨 Bingo Web UI v{__version__}
║  📡 Server: http://{host}:{port}
║  🔧 Mode: {current_mode}
╚══════════════════════════════════════════════════════════════════╝
    """)
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    run_server()
