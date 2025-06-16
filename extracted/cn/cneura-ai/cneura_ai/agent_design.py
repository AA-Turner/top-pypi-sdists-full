from datetime import datetime, timezone
import json
import pika
import pymongo
import uuid
from typing import Any


class AgentDesign:
    schema = {
        "type": "object",
        "properties": {
            "agent_name": {"type": "string"},
            "agent_description": {"type": "string"},
            "instructions": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of instructions to guide the agent."
            },
            "tools": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "tool_name": {"type": "string"},
                        "tool_description": {
                            "type": "string",
                            "description": "A detailed description of what the tool does. Must be sufficient to implement the tool."
                        },
                        "status": {
                            "type": "string",
                            "description": "Tool generation status",
                            "enum": ["pending", "generated", "failed"]
                        }
                    },
                    "required": ["tool_name", "tool_description"]
                }
            }
        },
        "required": ["agent_name", "agent_description", "instructions", "tools"]
    }

    system_prompt = (
        "You are an expert AI agent system designer.\n"
        "Based on the user query, generate a JSON object that defines the agent structure.\n"
        "Follow this schema:\n"
        "1. agent_name: A descriptive name for the agent.\n"
        "2. agent_description: A short summary of what the agent does.\n"
        "3. instructions: A list of steps the agent should follow.\n"
        "4. tools: A list of tools, each with:\n"
        "   - tool_name: A short name.\n"
        "   - tool_description: A strong technical description of the tool, enough to implement it in code.\n\n"
        "Output ONLY a valid JSON object matching the schema. Do not include comments or extra text."
    )

    def __init__(self, llm, mongo_uri: str, mq=True, host: str = 'localhost', username: str = None, password: str = None, tool_queue:str ="tool.code.synth"):
        self.llm = llm
        self.mongo_client = pymongo.MongoClient(mongo_uri)
        self.db = self.mongo_client["agent_db"]
        self.collection = self.db["agent_designs"]

        self.host = host
        self.tool_queue = tool_queue
        self.timestamp = str(datetime.now(timezone.utc))
        if mq:
            credentials = pika.PlainCredentials(username, password) if username and password else None
            connection_params = pika.ConnectionParameters(host=self.host, credentials=credentials) if credentials else pika.ConnectionParameters(host=self.host)
            self.mq_connection = pika.BlockingConnection(connection_params)
            self.channel = self.mq_connection.channel()
            self.channel.queue_declare(queue=tool_queue)

    def generate_and_store_agent_design(self, query: str) -> dict:
        result = self.llm.query(query=query, schema=self.schema, system_prompt=self.system_prompt)

        if not result.get("success", False):
            return {"error": "LLM failed to generate agent design", "details": result}

        design = result.get("data")
        design_id = str(uuid.uuid4())
        design["design_id"] = design_id

        for tool in design.get("tools", []):
            tool["status"] = "pending"

        self.collection.insert_one(design)

        for tool in design["tools"]:
            mq_payload = {
                "header":{"from": "agent_design", "timestamp":self.timestamp},"body":
               { "design_id": design_id,
                "tool_name": tool["tool_name"],
                "task_id": str(uuid.uuid4()),
                "task_description": tool["tool_description"]}
            }
            self.channel.basic_publish(
                exchange="",
                routing_key=self.tool_queue,
                body=json.dumps(mq_payload)
            )

        return design

    def update_tool_by_design_id(self, design_id: str, tool_name: str, updates: dict) -> dict:
        allowed_status = {"pending", "generated", "failed"}
        allowed_fields = {"status", "run", "doc", "parameters"}

        invalid_fields = set(updates) - allowed_fields
        if invalid_fields:
            return {"error": f"Invalid fields in update: {invalid_fields}"}

        if "status" in updates and updates["status"] not in allowed_status:
            return {"error": f"Invalid status value. Must be one of {allowed_status}"}

        update_query = {f"tools.$.{field}": value for field, value in updates.items()}

        result = self.collection.update_one(
            {"design_id": design_id, "tools.tool_name": tool_name},
            {"$set": update_query}
        )

        if result.matched_count == 0:
            return {"success": False, "error": "No matching design or tool found."}
        return {"success": True, "message": f"Tool '{tool_name}' updated successfully."}
