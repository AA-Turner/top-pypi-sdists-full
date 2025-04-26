import aiohttp


class OpenAIClient:
    def __init__(self):
        self.api_key = "96ae909e40534d49a70c5e4bdfe54f62"
        self.endpoint = "https://zinley.openai.azure.com"
        self.deployment_id = "gpt-4o"
        self.headers = {"api-key": self.api_key, "Content-Type": "application/json"}

    async def complete(self, messages, temperature=0, top_p=0.1, max_tokens=4096):

        payload = {
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens,
        }

        url = f"{self.endpoint}/openai/deployments/{self.deployment_id}/chat/completions?api-version=2024-04-01-preview"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=payload) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(
                        f"Error: {response.status} - {await response.text()}"
                    )


async def main():
    print("hello")
    client = OpenAIClient()
    response = await client.complete(
        messages=[
            {
                "role": "user",
                "content": f"Hello, tell me about Vietnam",
            }
        ]
    )
    print(response)
