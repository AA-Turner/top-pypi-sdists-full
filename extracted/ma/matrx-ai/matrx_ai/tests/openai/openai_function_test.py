from openai import OpenAI
import json
from dotenv import load_dotenv
from matrx_utils import vcprint, clear_terminal

load_dotenv()

clear_terminal()

client = OpenAI()

# 1. Define a list of callable tools for the model
tools = [
    {
        "type": "function",
        "name": "get_horoscope",
        "description": "Get today's horoscope for an astrological sign.",
        "parameters": {
            "type": "object",
            "properties": {
                "sign": {
                    "type": "string",
                    "description": "An astrological sign like Taurus or Aquarius",
                },
            },
            "required": ["sign"],
        },
    },
]

def get_horoscope(sign):
    return f"{sign}: Next Tuesday you will befriend a baby otter."

# Create a running input list we will add to over time
input_list = [
    {"role": "user", "content": "What is my horoscope? I am an Aquarius."}
]

# 2. Prompt the model with tools defined
response = client.responses.create(
    model="gpt-5-mini",
    reasoning={
        "effort": "high",
        "summary": "detailed"
    },
    tools=tools,
    include=["reasoning.encrypted_content"],
    input=input_list,
)

# Save function call outputs for subsequent requests
input_list += response.output


vcprint(input_list, "Updated Input List", color="green")

for item in response.output:
    if item.type == "function_call":
        if item.name == "get_horoscope":
            # 3. Execute the function logic for get_horoscope
            horoscope = get_horoscope(json.loads(item.arguments))
            
            # 4. Provide function call results to the model
            input_list.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps({
                  "horoscope": horoscope
                })
            })

print("Final input:")
vcprint(input_list, "Final Input List", color="cyan")

response = client.responses.create(
    model="gpt-5-mini",
    instructions="Give the user a short but thought-provoking response.",
    reasoning={
        "effort": "high",
        "summary": "detailed"
    },
    tools=tools,
    input=input_list,
    include=["reasoning.encrypted_content"],
)

input_list += response.output

# 5. The model should be able to give a response!
print("Final output:")
print(response.model_dump_json(indent=2))
print("\n" + response.output_text)


vcprint(input_list, "Updated Input List", color="green")
