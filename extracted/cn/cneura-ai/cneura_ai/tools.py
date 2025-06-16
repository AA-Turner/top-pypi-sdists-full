import os
import uuid
import asyncio
import requests
from cneura_ai.memory import MemoryManager  
from cneura_ai.llm import GeminiLLM

# Configurations
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", 8888))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
RESEARCH_API_URL = os.getenv("RESEARCH_API_URL", "http://host.docker.internal:8500/search")
SHELL_EXEC_API_URL = os.getenv("SHELL_EXEC_API_URL", "http://host.docker.internal:8600/command/run")
TOOL_API_URL = os.getenv("TOOL_API_URL", "http://host.docker.internal:8800/tools/query")
AGENT_ID = os.getenv("AGENT_ID", "agent")

# Core modules
llm = GeminiLLM(api_key=GEMINI_API_KEY)
memory_manager = MemoryManager(host=CHROMA_HOST, port=CHROMA_PORT, llm=llm)

# Tool creation
def create_tool(description: str) -> dict:
    return {"tool_description": description, "queue": "tool.code.synth"}

def get_tool(query: str):
    try:
        response = requests.post(TOOL_API_URL, json={"top_k": 1, "query": query})
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and data:
            return data[0]
        return {"error": "No tool found."}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def run_tool(url: str, args: dict = {}) -> dict:
    try:
        response = requests.post(url, json=args)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def research(query: str) -> dict:
    try:
        response = requests.post(RESEARCH_API_URL, json={"query": query})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Memory functions
def set_short_term_memory(memory: str):
    try:
        uid = str(uuid.uuid4())
        asyncio.run(memory_manager.store_to_short_term(AGENT_ID, uid, memory))
    except Exception as e:
        return {"error": str(e)}

def get_short_term_memory(query: str):
    try:
        return asyncio.run(memory_manager.retrieve_from_namespace(AGENT_ID, "short_term_memory", query))
    except Exception as e:
        return {"error": str(e)}

def set_long_term_memory(memory: str):
    try:
        uid = str(uuid.uuid4())
        asyncio.run(memory_manager.store_to_long_term(AGENT_ID, uid, memory))
    except Exception as e:
        return {"error": str(e)}

def get_long_term_memory(query: str):
    try:
        return asyncio.run(memory_manager.retrieve_from_namespace(AGENT_ID, "long_term_memory", query))
    except Exception as e:
        return {"error": str(e)}

def get_knowledge_base_memory(query: str):
    try:
        return asyncio.run(memory_manager.retrieve_from_namespace(AGENT_ID, "knowledge_base", query))
    except Exception as e:
        return {"error": str(e)}

def shell(command: str) -> dict:
    try:
        response = requests.post(SHELL_EXEC_API_URL, json={"agent_id": AGENT_ID, "command": [command]})
        response.raise_for_status()
        print(response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print(e)
        return {"error": str(e)}


# tool = create_tool("A tool that summarizes long documents.")
# print(tool)

# tool = get_tool("get time")
# print(tool)


# response = run_tool("http://localhost:36235/run", {"input_list": [54,87,98,54]})
# print(response)


# set_short_term_memory("The user asked about AI advancements.")

# result = get_short_term_memory("What did the user ask previously?")
# print(result)

# set_long_term_memory("AI alignment is a key concern for safe deployment.")


# result = get_long_term_memory("What is AI alignment?")
# print(result)

# kb = get_knowledge_base_memory("What is the capital of France?")
# print(kb)

# shell_output = shell("ls")
# print(shell_output)