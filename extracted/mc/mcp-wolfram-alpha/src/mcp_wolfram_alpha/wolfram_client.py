import wolframalpha
import os

api_key = os.getenv("WOLFRAM_API_KEY")

if api_key is None:
    raise ValueError("WOLFRAM_API_KEY environment variable not set")

client: wolframalpha.Client = wolframalpha.Client(api_key)

# test case for debugging your api key
if __name__ == "__main__":
    print(next(client.query("1+1").results).text)
