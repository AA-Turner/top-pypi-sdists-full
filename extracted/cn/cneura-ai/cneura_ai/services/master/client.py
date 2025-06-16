import requests

BASE_URL = "http://localhost:8000" 


def get_health_status():
    return requests.get(f"{BASE_URL}/health").json()


def bulk_add_or_update_config(data: list):
    return requests.post(f"{BASE_URL}/config/bulk", json=data).json()


def get_config():
    return requests.get(f"{BASE_URL}/config/").json()


def create_agent(agent_data: dict):
    return requests.post(f"{BASE_URL}/agent-registry/register", json=agent_data).json()


def get_agent(agent_id: str):
    return requests.get(f"{BASE_URL}/agent-registry/agent/{agent_id}").json()


def update_agent(agent_id: str, update_data: dict):
    return requests.put(f"{BASE_URL}/agent-registry/agent/{agent_id}", json=update_data).json()


def list_agents(agent_name=None, personality=None, skip=0, limit=10):
    params = {
        "agent_name": agent_name,
        "personality": personality,
        "skip": skip,
        "limit": limit
    }
    return requests.get(f"{BASE_URL}/agent-registry/", params=params).json()


def register_credential(credential_data: dict):
    return requests.post(f"{BASE_URL}/credentials/register", json=credential_data).json()


def bulk_register_credentials(credentials_data: dict):
    return requests.post(f"{BASE_URL}/credentials/register/bulk", json=credentials_data).json()


def get_credential(credential_id: str):
    return requests.get(f"{BASE_URL}/credentials/credential/{credential_id}").json()


def delete_credential(credential_id: str):
    return requests.delete(f"{BASE_URL}/credentials/credential/{credential_id}").json()

def store_short_term_memory(data: dict):
    return requests.post(f"{BASE_URL}/memory/store/short", json=data).json()

def store_long_term_memory(data: dict):
    return requests.post(f"{BASE_URL}/memory/store/long", json=data).json()

def store_knowledge(data: dict):
    return requests.post(f"{BASE_URL}/memory/store/knowledge", json=data).json()

def store_abilities(data: dict):
    return requests.post(f"{BASE_URL}/memory/store/abilities", json=data).json()

def store_auto_classified_memory(data: dict):
    return requests.post(f"{BASE_URL}/memory/store/auto", json=data).json()

def retrieve_memory(data: dict):
    return requests.post(f"{BASE_URL}/memory/retrieve", json=data).json()

def retrieve_relevant_context(data: dict):
    return requests.post(f"{BASE_URL}/memory/context", json=data).json()

def get_combined_context(data: dict):
    return requests.post(f"{BASE_URL}/memory/context/combined", json=data).json()

def cleanup_short_term_memory(namespace: str):
    return requests.delete(f"{BASE_URL}/memory/cleanup/{namespace}").json()

def delete_namespace(namespace: str):
    return requests.delete(f"{BASE_URL}/memory/namespace/{namespace}").json()

def search_research(data: dict):
    return requests.post(f"{BASE_URL}/research/search", json=data).json()

def create_session(data):
    return requests.post(f"{BASE_URL}/shell/session/create", json=data).json()

def stop_session(data):
    return requests.post(f"{BASE_URL}/shell/session/stop", json=data).json()

def run_command(data):
    return requests.post(f"{BASE_URL}/shell/command/run", json=data).json()

def get_file(data):
    return requests.post(f"{BASE_URL}/shell/file/get", json=data).json()

def get_folder(data):
    return requests.post(f"{BASE_URL}/shell/folder/get", json=data).json()

def download_folder(local_path):
    return requests.get(f"{BASE_URL}/shell/folder/download", params={"local_path": local_path}).json()

def create_tool(data):
    return requests.post(f"{BASE_URL}/tool-registry/register", json=data).json()

def get_tool(tool_id):
    return requests.get(f"{BASE_URL}/tool-registry/tool/{tool_id}").json()

def update_tool(tool_id, data):
    return requests.put(f"{BASE_URL}/tool-registry/tool/{tool_id}", json=data).json()

def list_tools(name=None, tool_class=None, skip=0, limit=10):
    params = {"skip": skip, "limit": limit}
    if name:
        params["name"] = name
    if tool_class:
        params["tool_class"] = tool_class
    return requests.get(f"{BASE_URL}/tool-registry/", params=params).json()

def register_user(username: str, password: str):
    url = f"{BASE_URL}/auth/register"
    data = {"username": username, "password": password}
    response = requests.post(url, json=data)
    return response.json()

def login_user(username: str, password: str):
    url = f"{BASE_URL}/auth/login"
    data = {"username": username, "password": password}
    response = requests.post(url, data=data)
    return response.json()

def get_current_user(token: str):
    url = f"{BASE_URL}/auth/me"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def get_log_history(task_id: str, start_time=None, end_time=None, skip=0, limit=100):
    url = f"{BASE_URL}/log/history"
    params = {
        "task_id": task_id,
        "start_time": start_time,
        "end_time": end_time,
        "skip": skip,
        "limit": limit
    }
    response = requests.get(url, params=params)
    return response.json()

def get_log_dashboard():
    url = f"{BASE_URL}/log/dashboard"
    response = requests.get(url)
    return response.text 

def list_queues():
    url = f"{BASE_URL}/queue/"
    response = requests.get(url)
    return response.json()

def get_queue_message(queue_name: str):
    url = f"{BASE_URL}/queue/recieve/{queue_name}/messages"
    response = requests.get(url)
    return response.json()


