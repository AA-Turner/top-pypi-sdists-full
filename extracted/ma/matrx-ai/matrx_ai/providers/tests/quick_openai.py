import sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()





message = "What are the top 3 things taught in AP Precalculus?"









response = client.responses.create(
    model="gpt-4.1-mini",
    input=message,
)







print("--------------------------------")
print()
print(response.output_text)
print("--------------------------------")