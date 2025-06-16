import requests
import json
import ast
import tiktoken
import numpy as np
import re


def estimate_tokens(text: str) -> int:
    """Estimate the number of tokens in a text using tiktoken."""
    tokenizer = tiktoken.get_encoding("cl100k_base")
    return len(tokenizer.encode(text))


def split_document(
    document: str, max_tokens: int = 160000, overlap_chars: int = 4000
) -> list:
    """Split a document into chunks based on max token count and overlap."""
    avg_token_length = 4
    max_chars = max_tokens * avg_token_length
    chunks = []
    start, end = 0, 0
    while end < len(document):
        end = min(start + max_chars, len(document))
        chunk = document[start:end]
        chunks.append(chunk)
        start = end - overlap_chars
    return chunks


def find_pages(
    keyword: str,
    document: str,
    max_token_context: int = 64000,
    API_KEY: str = None,
    API_URL: str = "https://openrouter.ai/api/v1/chat/completions",
    API_MODEL: str = "qwen/qwen3-32b:free",
) -> list:
    """Find pages in a document that mention a keyword using an LLM API."""
    if not API_KEY:
        raise ValueError("Please set the API_KEY environment variable.")
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    estimated_tokens = estimate_tokens(document)
    print("estimated_tokens", estimated_tokens)
    if estimated_tokens > max_token_context:
        print("Document too large, splitting into chunks...")
        chunks = split_document(document, max_tokens=max_token_context - 4000)
    else:
        chunks = [document]
    all_pages = []
    models = [API_MODEL]
    for i, chunk in enumerate(chunks):
        payload = {
            "models": models,
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "The following is the content of a Markdown file:\n\n"
                        f"{chunk}\n\n"
                        f"Please analyze this content and identify the pages that talk about {keyword}. "
                        "Return only the page numbers as a Python list (e.g., [35,36,37]). if you don't find any pages (which often happens), just return []."
                    ),
                }
            ],
        }
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            response_json = response.json()
            try:
                message = response_json["choices"][0]["message"]["content"]
                match = re.search(r"\[.*?\]", message).group()
                page_numbers = ast.literal_eval(match)
                if isinstance(page_numbers, list) and all(
                    isinstance(num, int) for num in page_numbers
                ):
                    all_pages.extend(page_numbers)
                else:
                    print(f"Response from chunk {i} is not a valid list of integers.")
            except Exception as e:
                print(f"Error parsing response from chunk {i}: {e}")
        else:
            print(f"Error during the request for chunk {i}: {response.status_code}")
            print(response.text)
    return list(np.unique(all_pages)) if all_pages else None


def merge_pages(page_numbers: list, path: str, prefix_id: str, title: str) -> tuple:
    """Merge selected pages into a single text and build a corpus list."""
    selected_pages = []
    corpus = []
    for page in page_numbers:
        with open(path + f"/page_{page}.md", encoding="utf-8") as file:
            selected_pages += f"\n\n --- PAGE n°{page} --- \n\n"
            text = file.read()
            selected_pages += text
            corpus.append(
                {"_id": f"DOC_{prefix_id}_p{page}", "title": title, "text": text}
            )
    return selected_pages, corpus


def extract_keywords(
    keyword: str,
    document: str,
    API_KEY: str = None,
    API_URL: str = "https://openrouter.ai/api/v1/chat/completions",
    API_MODEL: str = "qwen/qwen3-32b:free",
) -> dict:
    """Extract keywords and their context from a document using an LLM API."""
    if not API_KEY:
        raise ValueError("Please set the API_KEY environment variable.")
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    models = [API_MODEL]
    payload = {
        "models": models,
        "messages": [
            {
                "role": "user",
                "content": (
                    "You are a text analysis assistant.\n"
                    f"Given the following text, identify all {keyword} present. For each error code, extract the exact sentence or paragraph in which it appears, ensuring the text remains unaltered. Don't forget to add the page where the sentence has been extracted. Return the results in a JSON format where each key is an error code, and its value is the corresponding text segment, and it's associate page number."
                    f"Even if you're not sure but it seems to be a {keyword}, don't hesitate to put it in doubt."
                    "Example output format:\n"
                    """{
                    "ERROR_CODE_1": ["Exact text containing ERROR_CODE_1", X1 (corresponding to the page number of the extract text)],
                    "ERROR_CODE_2": ["Exact text containing ERROR_CODE_2.", X2 (corresponding to the page number of the extract text)],
                    ...
                    }"""
                    f"Text to analyse: {document}"
                ),
            }
        ],
    }
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        response_json = response.json()
        message = response_json["choices"][0]["message"]["content"]
        print("Raw response from the model:")
        message = json.loads(message)
    else:
        print(f"Error during the request: {response.status_code}")
        print(response.text)
    return message if message else None
