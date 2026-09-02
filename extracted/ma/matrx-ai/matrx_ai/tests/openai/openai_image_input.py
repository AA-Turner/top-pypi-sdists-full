import os

from openai import OpenAI
from matrx_utils import vcprint, clear_terminal
from dotenv import load_dotenv

load_dotenv()
clear_terminal()

test_user_id = os.environ.get("TEST_USER_ID", "")

client = OpenAI()

response = client.responses.create(
    model="gpt-4.1-mini",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "what is in this image?"},
                {
                    "type": "input_image",
                    "image_url": f"https://cdn.matrxserver.com/test-assets/user-{test_user_id}/mcp-logo.png",
                },
            ],
        }
    ],
)

vcprint(response, "Response", color="green")

text_content = response.output[0].content[0].text
print("\n")
print(text_content)
print("\n")
