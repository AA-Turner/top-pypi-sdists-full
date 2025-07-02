import re
import json
import requests
from pydantic import BaseModel
from maisaedu_utilities_prefect import get_dsn

from maisaedu_utilities_prefect.database.postgres import (
    connect,
    select,
    execute,
    insert_batch,
    detect_sql_injection
)


OPEN_ROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def is_valid_schema(schema):
    return re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", schema) is not None

class LLMService(BaseModel):
    open_router_api_key: str
    flow_name: str
    configs: list = []
    default_schema: str = 'meta'

    def __init__(self, **data):
        conn = connect(get_dsn())
        configs = []

        if data.get("default_schema") is None:
            data["default_schema"] = 'meta'
        else:
            if not is_valid_schema(data.get("default_schema")):
                raise ValueError("Invalid schema name")
            
        query = f"""
            select
                id,
                flow_name,	
                is_active,	
                model,	
                system_prompt,	
                response_format::text,	
                temperature,
                max_tokens
            from {data.get("default_schema")}.llm_flows_configs where flow_name = %s
            and is_active = true
        """

        results = select(
            conn,
            query,
            (data.get("flow_name"),)
        )
        
        if not results:
            raise ValueError(f"No configuration found for flow_name: {data.get('flow_name')}")
        else:
            for config in results:
                config_dict = {
                    "id": config[0],
                    "flow_name": config[1],
                    "is_active": config[2],
                    "model": config[3],
                    "system_prompt": config[4],
                    "response_format": json.loads(config[5]) if config[5] else None,
                    "temperature": config[6],
                    "max_tokens": config[7]
                }
                configs.append(config_dict)
            data['configs'] = configs

        conn.close()
        
        super().__init__(**data)

    def __validate_messages(self, messages):
        if not isinstance(messages, list) or not all(
            isinstance(m, dict) and 'role' in m and 'content' in m and isinstance(m['content'], str)
            for m in messages
        ):
            raise ValueError("messages must be a list of dicts with 'role' and 'content' (str)")

    def __save_history(self, config_id, request, response):
        conn = connect(get_dsn())
        model = request.get("model", "")
        request_json = json.dumps(request).replace("\\u0000", "")
        response_json = json.dumps(response.json()).replace("\\u0000", "")
    
        insert_sql = f"""
            INSERT INTO {self.default_schema}.llm_flows_runs_history (llm_flow_config_id, model, request, response)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """
        
        with conn.cursor() as cur:
            cur.execute(insert_sql, (config_id , model, request_json, response_json))
            inserted_id = cur.fetchone()[0]
            conn.commit()

        conn.close()
        return inserted_id

    def call_llm_api(self, messages):
        self.__validate_messages(messages)

        results = []

        for config in self.configs:
            result_return = {}
            result_return["model"] = config['model']
        
            messages = [
                {"role": "system", "content": config['system_prompt']},
                *messages
            ]

            if config['response_format'] is not None and config['response_format'] != "":
                request = {
                        "model": config['model'],
                        "messages": messages,
                        "temperature": config['temperature'],
                        "max_tokens": config['max_tokens'],
                        "response_format": {
                            "type": "json_schema",
                            "json_schema": config['response_format'],
                        },
                    }    
            else:
                request = {
                        "model": config['model'],
                        "temperature": config['temperature'],
                        "max_tokens": config['max_tokens'],
                        "messages": messages,
                    }

            try:
                response = requests.post(
                    OPEN_ROUTER_API_URL,
                    headers={
                        "Authorization": "Bearer " + self.open_router_api_key.replace("Bearer ", ""),
                        "Content-Type": "application/json",
                    },
                    json=request,
                )

                llm_flow_run_history_id = self.__save_history(config['id'], request, response)
                result_return["llm_flow_run_history_id"] = llm_flow_run_history_id
                
                if response.status_code == 200:
                    result = response.json()
                    if "error" in result and "message" in result['error']:
                        result_return['error'] = result['error']['message']
                    if "usage" in result:
                        try:
                            result_return["usage"] = result["usage"]
                        except Exception as e:
                            result_return["usage"] = f"Exception: {str(e)}"
                    if "choices" in result and len(result["choices"]) > 0:
                        content = result["choices"][0]["message"]["content"]
                        if isinstance(content, str):
                            try:
                                result_return["content"] = json.loads(content)
                            except Exception as e:
                                result_return["error"] = f"Exception: {str(e)}"
                        else:
                            result_return["content"] = content
                else:
                    result_return["error"] = f"Error in API request: {response.status_code}"
            except Exception as e:
                result_return["error"] = f"Exception: {str(e)}"
            
            results.append(result_return)

        return results

