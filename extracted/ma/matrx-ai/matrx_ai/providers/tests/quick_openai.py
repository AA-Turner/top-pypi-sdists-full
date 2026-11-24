"""Manual smoke script: one live OpenAI Responses call. Run it directly; importing it does nothing.

Provider discovery imports every module under ``matrx_ai.providers``; a module-level client made that
import call the OpenAI API (and fail without OPENAI_API_KEY in CI).
"""

from dotenv import load_dotenv
from openai import OpenAI


def main() -> None:
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


if __name__ == "__main__":
    main()
