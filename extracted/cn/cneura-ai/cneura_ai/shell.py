import docker
import tarfile
import io
import time
from docker.errors import NotFound
from pymongo import MongoClient
from bson import ObjectId

class DockerShellSession:
    def __init__(self, agent_id: str,  remote_url: str,image="ubuntu", mongo_uri:str = "mongodb://localhost:27017/", database:str = "docker_sessions", collection:str = "sessions"):
        self.agent_id = agent_id
        self.container_name = f"agent_container_{agent_id}"
        self.image = image
        self.client = docker.DockerClient(base_url=remote_url)
        self.container = None

        self.mongo_client = MongoClient(mongo_uri)  
        self.db = self.mongo_client[database]  
        self.sessions_collection = self.db[collection]  

        self._load_session_data()
        self._ensure_container_running()

    def _load_session_data(self):
        """ Try to load saved session data from MongoDB. """
        session_data = self.sessions_collection.find_one({"agent_id": self.agent_id})
        if session_data:
            container_id = session_data.get("container_id")
            if container_id:
                try:
                    self.container = self.client.containers.get(container_id)
                except NotFound:
                    self.container = None

    def _save_session_data(self):
        """ Save the session data to MongoDB. """
        if self.container:
            session_data = {
                "agent_id": self.agent_id,
                "container_id": self.container.id
            }
            self.sessions_collection.update_one(
                {"agent_id": self.agent_id},
                {"$set": session_data},
                upsert=True  # If no document is found, a new one is created
            )

    def _wait_for_container_ready(self):
        """ Wait for the container to be fully ready before executing commands. """
        retries = 10  # Number of retries to check if the container is ready
        while retries > 0:
            container = self.client.containers.get(self.container_name)
            if container.status == "running":
                print(f"Container {self.container_name} is ready!")
                return
            else:
                print(f"Waiting for container {self.container_name} to be ready...")
                time.sleep(2)  # Wait for 2 seconds before retrying
                retries -= 1

        print(f"Container {self.container_name} did not start in time.")

    def _ensure_container_running(self):
        """ Ensure that the container is running, or start a new one. """
        if not self.container:
            containers = self.client.containers.list(filters={"name": self.container_name})
            if containers:
                self.container = containers[0]
            else:
                self.container = self.client.containers.run(
                    self.image,
                    name=self.container_name,
                    command="bash",
                    tty=True,
                    detach=True,
                    stdin_open=True
                )
            self._save_session_data()
        self._wait_for_container_ready()

    def run(self, command: list):
        try:
            if not is_safe_command(command):
                return {"stdout": "", "stderr": "Unsafe command detected", "returncode": -1}

            container = self.client.containers.get(self.container_name)
            
            if isinstance(command, list):
                command_str = " ".join(command)
            else:
                command_str = command
            
            cmd = ["bash", "-c", command_str]

            exec_result = container.exec_run(cmd=cmd, stdout=True, stderr=True)

            stdout = exec_result.output.decode('utf-8').strip() if exec_result.output else ""
            stderr = ""

            if hasattr(exec_result, 'stderr') and exec_result.stderr:
                stderr = exec_result.stderr.decode('utf-8').strip()

            return {
                "stdout": stdout,
                "stderr": stderr,
                "returncode": exec_result.exit_code
            }

        except docker.errors.APIError as e:
            return {"stdout": "", "stderr": str(e), "returncode": -1}
        except Exception as e:
            return {"stdout": "", "stderr": str(e), "returncode": -1}


    def stop(self):
        """ Stop and remove the container. """
        try:
            container = self.client.containers.get(self.container_name)
            container.stop()
            container.remove()
            self.container = None
            self._save_session_data() 
        except NotFound:
            pass  # Container not found, nothing to stop

    def get_file(self, container_path: str) -> bytes:
        """ Retrieve a file from the container. """
        try:
            tar_stream, _ = self.container.get_archive(container_path)

            file_like_object = io.BytesIO()
            for chunk in tar_stream:
                file_like_object.write(chunk)
            file_like_object.seek(0)

            with tarfile.open(fileobj=file_like_object) as tar:
                member = tar.getmembers()[0]
                file_content = tar.extractfile(member).read()

            return file_content
        except Exception as e:
            print(f"Error getting file: {e}")
            return None
        
    def get_folder(self, folder_path: str, local_path: str):
        """ Get a large folder from the container. """
        try:
            bits, stat = self.container.get_archive(folder_path)
            with open(local_path, 'wb') as f:
                for chunk in bits:
                    f.write(chunk)
            return f"Folder archived successfully at {local_path}"
        except Exception as e:
            return f"Error getting folder: {str(e)}"

class ShellSessionManager:
    def __init__(self, remote_url: str, image="ubuntu", mongo_uri:str = "mongodb://localhost:27017/", database:str = "docker_sessions", collection:str = "sessions"):
        self.sessions = {}
        self.remote_url = remote_url
        self.image = image
        self.mongo_uri = mongo_uri
        self.database = database
        self.collection = collection

    def get_session(self, agent_id: str):
        """ Retrieve or create a DockerShellSession. """
        if agent_id not in self.sessions:
            self.sessions[agent_id] = DockerShellSession(agent_id=agent_id, remote_url=self.remote_url, image=self.image, mongo_uri=self.mongo_uri, database=self.database, collection=self.collection)
        
        session = self.sessions[agent_id]
        if not session.container:
            session._ensure_container_running()
        
        return session

    def run_command(self, agent_id: str, command: list):
        """ Run a command within the session's container. """
        session = self.get_session(agent_id)
        return session.run(command)

    def stop_session(self, agent_id: str):
        """ Stop and remove the session's container. """
        if agent_id in self.sessions:
            self.sessions[agent_id].stop()
            del self.sessions[agent_id]

def is_safe_command(command: list) -> bool:
    """ Validate that the command is not harmful. """
    blacklisted = ['rm ', 'reboot', 'shutdown', 'mkfs', 'dd ', 'eval']
    return not any(bad in " ".join(command) for bad in blacklisted)
