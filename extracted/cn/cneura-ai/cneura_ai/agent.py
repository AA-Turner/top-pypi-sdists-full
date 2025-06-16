import asyncio
import json
import re
from typing import List
from cneura_ai.llm import LLMInterface
from cneura_ai.logger import logger
from cneura_ai.memory import PersistentWorkingMemory, MemoryManager
import ast
import time
import random
import uuid
import inspect


class Agent:
    def __init__(
        self, 
        llm: LLMInterface, 
        personality: dict, 
        memory_manager: MemoryManager = None, 
        namespace: str = "default", 
        working_memory: PersistentWorkingMemory = None, 
        memory_state_id: str = None):
        """
        Initializes the Agent with required dependencies, personality, memory, and namespace.
        """
        self.llm = llm
        self.memory_manager = memory_manager
        self.namespace = namespace
        self.tools_doc = []
        self.tools = {}
        self.personality = personality
        self.system_prompt = ""
        self.schema = self._get_schema()

        self.working_memory = working_memory
        self.collection = self.working_memory.collection if self.working_memory else None
        self.memory_state_id = memory_state_id
        self.memory_slots = self._load_memory()

        self.messages = self._load_conversation()

    def _get_schema(self):
        """
        Returns the schema used to validate actions, thoughts, observations, and answers.
        """
        return {
            "type": "object",
            "properties": {
                "type": {
                "type": "string",
                "description": "THOUGHT | ACTION | OBSERVATION | ANSWER"
                },
                "thought": {
                "type": "string",
                "description": "Thought content if the message type is THOUGHT."
                },
                "pause": {
                "type": "boolean",
                "description": "True if ACTION type requires a pause."
                },
                "tool": {
                "type": "string",
                "description": "Tool name if ACTION type."
                },
                "args": {
                "type": "string",
                "description": "Arguments for the tool in ACTION."
                },
                "observation": {
                "type": "string",
                "description": "Observation content if the message type is OBSERVATION."
                },
                "answer": {
                "type": "string",
                "description": "Final answer if the message type is ANSWER."
                }
            }
            }


    def _load_memory(self):
        """
        Loads the memory from the working memory, if available, based on the memory state ID.
        """
        if self.working_memory and self.memory_state_id:
            return self.working_memory.load_memory_by_state_id(self.memory_state_id) or []
        return []

    def _load_conversation(self):
        """
        Loads the conversation history from memory if the memory state ID is provided.
        """
        return self.working_memory.load_conversation_by_state_id(self.memory_state_id) if self.memory_state_id else []

    def set_tools_and_docs(self, tools: dict, tools_doc: list):
        """
        Sets available tools and their documentation for the agent.
        """
        self.tools = tools
        self.tools_doc = tools_doc

        tools_doc_str = json.dumps(self.tools_doc, indent=2)
        self.system_prompt = f"""
            You are: {self.personality.get("name")}
            Personality Description: {self.personality.get("description")}
            Instructions: {self.personality.get("instructions")}
            You operate in a reasoning loop: Thought → Action → Observation, and then provide a final Answer.

            - Use **THOUGHT** to describe what you're thinking.
            - Use **ACTION** to call one of the available tools.
            - Return **PAUSE** after an ACTION to wait for an observation.
            - Use **OBSERVATION** to process results from the tool call.
            - Finally, use **ANSWER** to provide the result when ready.

            Your available actions are:

            {tools_doc_str}

            Here is a generic example:

            Question: <QUESTION>

            step 01 - {{ "type": "THOUGHT", "thought": "I need to understand the question and decide next step", "pause": false, "tool": "", "args": "", "observation": "", "answer": "" }}

            step 02 - {{ "type": "ACTION", "tool": "<TOOL_NAME>", "args": ["<ARGUMENT_1>", "<ARGUMENT_2>"], "pause": true, "thought": "",  "observation": "", "answer": "" }}

            You will be called again with this:

            step 03 - {{ "type": "OBSERVATION", "observation": "<RESULT_FROM_TOOL>" }}

            step 04 - {{ "type": "THOUGHT", "thought": "Now I can reason further or call another tool if needed", "pause": false, "tool": "", "args": "", "observation": "", "answer": "" }}

            step 05 - {{ "type": "ACTION", "tool": "<ANOTHER_TOOL>", "args": ["<ARGUMENT>"], "pause": true, "thought": "",  "observation": "", "answer": "" }}

            You will be called again with this:

            step 06 - {{ "type": "OBSERVATION", "observation": "<ANOTHER_RESULT>" }}

            step 07 - {{ "type": "ANSWER", "answer": "<FINAL_ANSWER>", "tool": "", "args": "", "observation": "", "thought": "",  }}

            **Guidelines**
            - One step at a time.
            - Always follow the Thought → Action → Observation cycle.
            - Only give the final response as an ANSWER when ready.
            - the all fields are required. If the field has not value give empty string.

            Now it's your turn:
        """.strip()

        self.messages = [ ("system", self.system_prompt)]

    async def __call__(self, query: str = None):
        """
        Starts the agent's execution cycle. Processes thoughts, actions, and observations.
        Handles retry logic for failed LLM queries.
        """
        next_prompt = query if query else self.messages[-1][1]
        max_iterations = 10
        retries = 3  
        retry_delay = 2  
        attempt = 0

        while attempt < retries:
            attempt += 1
            i = 0
            while i < max_iterations:
                i += 1
                try:
                    result = await self.execute(next_prompt)

                    if result is None:
                        logger.error("Received None as the result. Exiting the loop.")
                        break

                    logger.info(f"Result: {result}")

                    if result.get("type") == "THOUGHT":
                        next_prompt = result
                        continue

                    if result.get("type") == "ACTION" and "pause" in result and "tool" in result:
                        chosen_tool = result.get("tool", "")
                        args = self._parse_args(result.get("args"))

                        if chosen_tool in self.tools:
                            tool_func = self.tools[chosen_tool]
                            expected_args = inspect.signature(tool_func).parameters
                            if len(args) != len(expected_args):
                                logger.error(f"Incorrect number of args for tool {chosen_tool}")
                                next_prompt = {"type": "OBSERVATION", "observation": "Incorrect number of arguments for the tool."}
                                continue

                            is_instant = any(doc for doc in self.tools_doc if doc["name"] == chosen_tool and doc.get("instant", True))

                            result_tool = await tool_func(*args) if asyncio.iscoroutinefunction(tool_func) else tool_func(*args)
                            next_prompt = {"type": "OBSERVATION", "observation": result_tool}
                            logger.info(f"Executed tool {chosen_tool} with args {args}")

                            if is_instant:
                                continue
                            else:
                                logger.info("tool goes external")
                                return {"is_tool": True, "data": result_tool, "tool": chosen_tool, "args": args}

                        else:
                            next_prompt = {"type": "OBSERVATION", "observation": "Tool not found"}
                            logger.error(f"Tool '{chosen_tool}' not found")
                        continue

                    if result.get("type") == "ANSWER":
                        logger.info(f"Final Answer: {result['answer']}")
                        return result['answer']
                    break

                except Exception as e:
                    logger.error(f"Attempt {attempt} failed: {e}. Retrying in {retry_delay} seconds...")
                    await asyncio.sleep(retry_delay + random.uniform(0, 1))  
                    continue

            if i >= max_iterations:
                logger.error("Maximum iterations reached without success.")
                break

        logger.error(f"All attempts failed after {retries} retries.")
        return None
    

    def _extract_and_parse_json(self, response: str):
        """Extract JSON content from LLM response."""
        try:
            # Case 1: Look for fenced JSON block (```json ... ```)
            match = re.search(r"```json\s*\n(\{.*?\})\s*```", response, re.DOTALL)
            if match:
                json_str = match.group(1).strip()
                return json.loads(json_str)

            # Case 2: Fallback to first JSON object-like string
            json_match = re.search(r"(\{.*\})", response, re.DOTALL)
            if json_match:
                json_str = json_match.group(1).strip()
                return json.loads(json_str)

            # Case 3: Try to parse whole response
            return json.loads(response.strip())

        except json.JSONDecodeError as e:
            logger.error(f"[JSONDecodeError] Could not parse JSON. Error: {e}")
            logger.error("Raw response:\n", response)
            return None  # or response if you want to fallback to raw
        
    def parse_result(self, result):
        """
        Parse the result of a query based on its type, with error handling for missing fields.
        """
        if isinstance(result, str):
            parsed_result =self. _extract_and_parse_json(result)
            logger.info(f"The llm response is a type of string. {type(parsed_result)} {parsed_result}")

        if isinstance(result, dict):
            if "type" not in result:
                logger.error(f"Missing 'type' in the result: {result}")
                return None

            match result["type"]:
                case "THOUGHT":
                    return {"type": "THOUGHT", "thought": result.get("thought", "")}

                case "ACTION":
                    raw_args = result.get("args", [])
                    parsed_args = self._parse_args(raw_args)
                    return {"type": "ACTION", "tool": result["tool"], "args": parsed_args, "pause": result.get("pause", False)}

                case "OBSERVATION":
                    return {"type": "OBSERVATION", "observation": result.get("observation", "")}

                case "ANSWER":
                    return {"type": "ANSWER", "answer": result.get("answer", "")}

                case _:
                    logger.error(f"Unknown 'type' value: {result['type']}")
                    return None
        else:
            # logger.error(f"Result is not a dictionary: {result}")
            return None

    def _parse_args(self, raw_args):
        """
        Safely parses the 'args' field, handling both stringified lists and simple strings.
        Returns a list of arguments.
        """
        if isinstance(raw_args, str):
            trimmed = raw_args.strip()
            if trimmed.startswith(("(", "[", "{")) and trimmed.endswith((")", "]", "}")):
                try:
                    parsed = ast.literal_eval(trimmed)
                    if isinstance(parsed, (list, tuple)):
                        return list(parsed)
                    return [parsed]
                except Exception as e:
                    logger.error(f"Failed to parse args: {raw_args} | Error: {e}")
                    return [raw_args]
            else:
                # Plain string, treat as single argument
                return [raw_args]
        elif isinstance(raw_args, (list, tuple)):
            return list(raw_args)
        else:
            return [raw_args]

    async def execute(self, message):
        """
        Executes the agent's reasoning process based on the current message, with retry logic.
        """
        if message:
            self.messages.append(("user", message))

        retries = 3 
        max_retry_delay = 10  
        attempt = 0

        while attempt < retries:
            attempt += 1
            try:
                result = self.llm.query(self.messages, self.schema)
                if not result.get("success", False):
                    raise ValueError(result.get("error", "LLM ERROR"))
                
                result_data = result.get("data", None)
                if not result_data:
                    raise ValueError("The data key not found on llm response")

                parsed_result = self.parse_result(result_data)
                
                self.messages.append(("ai", parsed_result))
                return parsed_result

            except Exception as e:
                logger.error(f"Attempt {attempt} failed: {e}. Retrying...")
                
                delay = min(2 ** attempt, max_retry_delay) 
                await asyncio.sleep(delay)  
                
                continue  

        logger.error(f"All {retries} attempts to execute the message failed.")
        return None


    def save_current_memory(self):
        """
        Saves the current conversation state to memory.
        """
        if self.working_memory:
            if self.memory_state_id:
                self.working_memory.update_memory(self.memory_state_id, self.messages)
            else:
                self.memory_state_id = self.working_memory.save_memory(self.messages)

            return self.memory_state_id
