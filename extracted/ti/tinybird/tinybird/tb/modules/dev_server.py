import glob
import http.server
import json
import time
from pathlib import Path
from typing import Callable, Optional

import click

from tinybird.tb.client import TinyB
from tinybird.tb.modules.common import sys_exit
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.local_common import TB_LOCAL_PORT
from tinybird.tb.modules.project import Project


class BuildStatus:
    def __init__(self):
        self.last_build_time = 0
        self.building = False
        self.error: Optional[str] = None
        self.result: Optional[str] = None


class DevServer(http.server.HTTPServer):
    project: Project
    tb_client: TinyB
    process: Callable

    def __init__(
        self,
        process: Callable,
        project: Project,
        build_status: BuildStatus,
        tb_client: TinyB,
    ):
        port = 49161
        self.project = project
        self.tb_client = tb_client
        self.process = process
        self.build_status = build_status
        self.port = port

        try:
            super().__init__(("", port), DevHandler)
            click.echo(FeedbackManager.success(message=f"✓ Dev server running on http://localhost:{port}"))
            click.echo(
                FeedbackManager.info(
                    message=f"* Access your project at https://cloud.tinybird.co/local/{TB_LOCAL_PORT}/{project.workspace_name}/project"
                )
            )
        except OSError as e:
            if e.errno == 48:  # Address already in use
                click.echo(FeedbackManager.error(message=f"Port {port} is already in use. Try a different port."))
                sys_exit("port_in_use", f"Port {port} is already in use")
            else:
                click.echo(FeedbackManager.error_exception(error=e))
                sys_exit("server_error", str(e))


class DevHandler(http.server.SimpleHTTPRequestHandler):
    server: DevServer

    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        try:
            project: Project = self.server.project

            if self.path == "/":
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.send_cors_headers()
                self.end_headers()

                html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Tinybird Dev Server</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                        h1 {{ color: #333; }}
                        ul {{ list-style-type: none; padding: 0; }}
                        li {{ margin-bottom: 10px; }}
                        a {{ color: #0066cc; text-decoration: none; }}
                        a:hover {{ text-decoration: underline; }}
                    </style>
                </head>
                <body>
                    <h1>Tinybird Dev Server</h1>
                    <p>Server running for project: {project.path}</p>
                    <p>Access your local environment at <a href="https://cloud.tinybird.co/local/{TB_LOCAL_PORT}/{project.workspace_name}/project">https://cloud.tinybird.co/local/{TB_LOCAL_PORT}/{project.workspace_name}/project</a> and edit your project.</p>
                    <h2>API Endpoints:</h2>
                    <ul>
                        <li><a href="/files">/files</a> - List all project files</li>
                    </ul>
                </body>
                </html>
                """
                self.wfile.write(html.encode())
                return

            elif "/files/" in self.path:
                file_path = self.path.split("/files/")[1].split("?")[0]
                project_files = project.get_project_files()
                project_file = next((Path(f) for f in project_files if f.endswith(file_path)), None)
                if not project_file:
                    self.send_response(404)
                    self.send_header("Content-Type", "application/json")
                    self.send_cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "error", "error": "Resource not found"}).encode())
                    return

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"path": str(project_file), "content": project_file.read_text()}).encode())
                return

            elif "/files" in self.path:
                project_files = project.get_project_files()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(
                    json.dumps(
                        {
                            "files": [f.replace(f"{project.folder}/", "") for f in project_files],
                            "root": project.folder,
                            "workspace_name": project.workspace_name,
                        }
                    ).encode()
                )
                return

            # Handle all other paths
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": "Not found"}).encode())

        except Exception as e:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())

    def do_POST(self):
        try:
            # Parse the request body
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            data = json.loads(body)

            # Get the file path from the request body
            file_path = data.get("path")
            if not file_path:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "No file path provided"}).encode())
                return

            exists = glob.glob(f"{self.server.project.folder}/**/{file_path}", recursive=True)
            if not exists:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "File does not exist"}).encode())
                return

            # Get the content from the request body
            content = data.get("content")
            if not content:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "No content provided"}).encode())
                return

            # Write the content to the file
            file_path = exists[0]
            with open(file_path, "w") as f:
                f.write(content)
            # sleep for 0.2 seconds to ensure the file is written
            time.sleep(0.2)

            def check_build_status(attempts: int = 0):
                if attempts > 10:
                    return "Build timeout. Check the console for more details."
                if self.server.build_status.building:
                    time.sleep(0.5)
                    return check_build_status(attempts + 1)
                else:
                    return self.server.build_status.error

            build_error = check_build_status()
            if build_error:
                raise Exception(build_error)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "message": "File written successfully"}).encode())

        except Exception as e:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "error": str(e)}).encode())

    def log_message(self, format, *args):
        pass


def start_server(project: Project, tb_client: TinyB, process: Callable, build_status: BuildStatus):
    """Start a development server for the project.

    Args:
        project: The project instance to serve.
    """

    try:
        click.echo(FeedbackManager.highlight(message="\n» Starting Tinybird dev server...\n"))

        # Create and start the server
        server = DevServer(process, project, build_status, tb_client)
        server.serve_forever()

        # Run the server in the main thread
        click.echo(FeedbackManager.gray(message="\nWatching for changes...\n"))
        click.echo(FeedbackManager.highlight(message="Press Ctrl+C to stop the server\n"))

    except KeyboardInterrupt:
        click.echo(FeedbackManager.highlight(message="\n» Stopping Tinybird dev server...\n"))
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=e))
        sys_exit("server_error", str(e))
