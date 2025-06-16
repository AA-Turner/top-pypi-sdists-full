import os
import re
import uuid
import fitz
import io
import json
from tqdm import tqdm
from openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from PIL import Image
import base64
from typing import List, Generator, Optional

# from ragformance.data_generation.generators.alpha.prompts import (
#     EXTRACT_TXT_PROMPT,
#     GENERATE_QUESTIONS_PROMPT,
#     GENERATE_ANSWERS_PROMPT,
#     FIND_CHUNKS_PROMPT,
#     CATEGORIZE_SECTIONS_PROMPT
# )
from .prompts import (
    EXTRACT_TXT_PROMPT,
    GENERATE_QUESTIONS_PROMPT,
    GENERATE_ANSWERS_PROMPT,
    FIND_CHUNKS_PROMPT,
    CATEGORIZE_SECTIONS_PROMPT,
)
# Global constants for API are removed. They will be passed via args.
# MODEL_NAME = "gpt-4.1-mini" # Default can be handled in generator or main function

DEFAULT_MODEL_NAME = "gpt-4.1-mini"  # A default if not provided

# %%


def pdf_to_images(pdf_path: str) -> Generator[Image.Image, None, None]:
    doc = fitz.open(pdf_path)
    try:
        for page in doc:
            pix = page.get_pixmap()
            yield Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    finally:
        doc.close()


def image_to_bytes(image: Image.Image) -> bytes:
    with io.BytesIO() as buffer:
        image.save(buffer, format="PNG", optimize=True)
        return buffer.getvalue()


def extract_raw_text(image_b64: str, openai_client, model: str = "MODEL_NAME") -> str:
    response = openai_client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": EXTRACT_TXT_PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{image_b64}"},
                    },
                ],
            }
        ],
        temperature=0,
    )
    return response.choices[0].message.content


def read_pdf_file_multimodal(
    file_path: str,
    api_key: str,
    base_url: str,
    model_name: str,
    max_pages: Optional[int] = None,
) -> str:
    openai_client = OpenAI(api_key=api_key, base_url=base_url)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found")

    extracted_texts = []
    doc = fitz.open(file_path)
    total_pages = len(doc)
    pages_to_process = total_pages
    if max_pages is not None and max_pages > 0:
        pages_to_process = min(total_pages, max_pages)

    print(
        f"Converting PDF with {pages_to_process}/{total_pages} pages to images for OCR..."
    )

    for page_num, image in enumerate(pdf_to_images(file_path), start=1):
        if page_num > pages_to_process:
            break
        print(f"Processing page {page_num}/{pages_to_process}...")
        try:
            img_bytes = image_to_bytes(image)
            img_b64 = base64.b64encode(img_bytes).decode("utf-8")
            # Pass model_name to extract_raw_text if it's not using the global one.
            # extract_raw_text already takes model as an argument.
            page_text = extract_raw_text(
                img_b64, openai_client=openai_client, model=model_name
            )
            extracted_texts.append(page_text)
        except Exception as e:
            error_msg = f"\nError processing page {page_num}: {str(e)}\n"
            extracted_texts.append(
                error_msg
            )  # Add error to list to indicate failure for this page
            print(error_msg)
    doc.close()
    print(f"OCR processing complete for {file_path}")
    return "\n\n".join(extracted_texts)


# %%


def remove_page_numbers(text: str) -> str:
    lines = text.split("\n")
    filtered_lines = [
        line for line in lines if not re.fullmatch(r"^\s*p\s*a\s*g\s*e\s+\d+\s*$", line)
    ]
    return "\n".join(filtered_lines)


# %%


def split_into_sections(raw_text: str) -> List[str]:
    section_pattern = re.compile(r"\n\s*\d+\.\s+", re.IGNORECASE)
    sections = section_pattern.split(raw_text)
    chunks = []
    for i in range(1, len(sections)):
        delimiter = section_pattern.findall(raw_text)[i - 1].strip()
        chunk = f"{delimiter}{sections[i]}".strip()
        chunks.append(chunk)
    return chunks


# %%


def convert_numbered_list_str_to_list(s: str) -> List[str]:
    pattern = re.compile(r"^\d+\.\s*")
    values = []
    for line in s.split("\n"):
        val = pattern.sub("", line).strip()
        if val:
            values.append(val)
    return values


def generate_questions(raw_text: str, llm) -> List[str]:
    prompt = GENERATE_QUESTIONS_PROMPT.format(raw_text=raw_text)
    answer = llm.invoke([HumanMessage(content=prompt)]).content.strip()
    print(answer)
    questions = convert_numbered_list_str_to_list(answer)
    return questions


def generate_answers(context: str, query: str, llm) -> List[str]:
    prompt = GENERATE_ANSWERS_PROMPT.format(context=context, query=query)
    answer = llm.invoke([HumanMessage(content=prompt)])
    return answer.content.strip()


def find_chunks(context: str, query: str, llm) -> List[str]:
    prompt = FIND_CHUNKS_PROMPT.format(context=context, query=query)
    chunks = llm.invoke([HumanMessage(content=prompt)])
    chunks = convert_numbered_list_str_to_list(chunks.content.strip())
    return chunks


def categorize_question(query: str, context: str, llm) -> str:
    prompt = CATEGORIZE_SECTIONS_PROMPT.format(context=context, query=query)
    answer = llm.invoke([HumanMessage(content=prompt)])
    return answer.content.strip()


def extract_category(content: str):
    category_line = next(
        line for line in content.split("\n") if line.startswith("Category: ")
    )
    match = re.search(r"Category:\s*\d+\.\s*(.*)", category_line)
    if match:
        category = match.group(1).strip()
        return category.lower()
    else:
        return "unknown"


# %%


def save_list_to_file(lf: List[str], file_path: str) -> None:
    with open(file_path, "w") as f:
        for s in lf:
            f.write(f"{s}\n")


def load_list_from_file(file_path: str) -> List[str]:
    with open(file_path) as f:
        return [line.rstrip("\n") for line in f]


# %%


if __name__ == "__main__":
    # read_pdf_file_multimodal(file_path="AIDA Architecture synthesis V4.5.pdf")
    # with open("AIDA Architecture synthesis V4.5_image_description.txt", "r") as file:
    #     content = file.read()
    # content=remove_page_numbers(text=content)
    # with open("raw.txt", "w", encoding="utf-8") as f:
    #     f.write(content)

    # plug from config
    try:
        llm = ChatOpenAI(
            model_name="MODEL_NAME",
            temperature=0.0,
            openai_api_base="OPENAI_BASE_URL",
            openai_api_key="OPENAI_API_KEY",
        )
        print("LLM initialized successfully.")
    except Exception as e:
        llm = None
        print(f"Failed to initialize LLM: {e}")

    with open("raw.txt") as file:
        raw_text = file.read()
    sections = split_into_sections(raw_text=raw_text)
    print("Number of sections: ", len(sections))
    questions = generate_questions(raw_text=sections[4], llm=llm)
    print(questions)


# Placeholder for the refactored main logic
def main(args: dict) -> None:
    pdf_path = args["pdf_path"]
    output_dir = args["output_dir"]
    # model_path = args.get(
    #    "model_path"
    # )  # For local GPT-2, if used for Q&A generation directly
    max_pages = args.get("max_pages")

    # API details for OpenAI calls (OCR, and potentially Q&A if not using local GPT-2 for that)
    api_key = args["api_key"]
    base_url = args["base_url"]
    # model_name for OpenAI calls (e.g., for OCR, or if ChatOpenAI is used for Q&A)
    openai_model_name = args.get("model_name", DEFAULT_MODEL_NAME)

    print(f"Starting TokenBurner GPT-2 processing for {pdf_path}")
    print(f"Output will be saved to: {output_dir}")

    # 1. Perform OCR and get raw text
    # The read_pdf_file_multimodal now takes API params and returns text
    raw_extracted_text = read_pdf_file_multimodal(
        file_path=pdf_path,
        api_key=api_key,
        base_url=base_url,
        model_name=openai_model_name,  # Model for OCR
        max_pages=max_pages,
    )

    # 2. Preprocess text (remove page numbers, split into sections)
    processed_text = remove_page_numbers(text=raw_extracted_text)
    sections = split_into_sections(raw_text=processed_text)

    if not sections:
        print("No sections found after text processing. Exiting.")
        # Create empty files to satisfy generator expectations
        open(os.path.join(output_dir, "corpus.jsonl"), "w").close()
        open(os.path.join(output_dir, "queries.jsonl"), "w").close()
        return

    # 3. Initialize LLM for Q&A generation
    try:
        llm_qa = ChatOpenAI(
            model_name=openai_model_name,  # Using the same model for Q&A for now
            temperature=0.0,
            openai_api_base=base_url,
            openai_api_key=api_key,
        )
        print(f"LLM for Q&A ({openai_model_name}) initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize LLM for Q&A: {e}. Aborting.")
        # Create empty files
        open(os.path.join(output_dir, "corpus.jsonl"), "w").close()
        open(os.path.join(output_dir, "queries.jsonl"), "w").close()
        return

    # 4. Generate Corpus
    corpus_items = []
    for i, section_text in enumerate(sections):
        # Simple title for now, could be improved if sections have titles
        title = f"Section {i+1} of {os.path.basename(pdf_path)}"
        doc_id = f"doc_{os.path.basename(pdf_path)}_{i+1}"
        corpus_items.append(
            {"_id": doc_id, "title": title, "text": section_text.strip()}
        )

    corpus_file_path = os.path.join(output_dir, "corpus.jsonl")
    with open(corpus_file_path, "w", encoding="utf-8") as f_corp:
        for doc_item in corpus_items:
            f_corp.write(json.dumps(doc_item) + "\n")
    print(f"Corpus saved to {corpus_file_path}")

    # 5. Generate Queries and Answers
    query_items = []

    for doc_item in tqdm(corpus_items, desc="Generating Q&A for sections"):
        section_context = doc_item["text"]
        corpus_doc_id = doc_item["_id"]

        try:
            generated_qs = generate_questions(raw_text=section_context, llm=llm_qa)
            for q_text in generated_qs:
                if not q_text.strip():
                    continue

                answer_text = generate_answers(
                    context=section_context, query=q_text, llm=llm_qa
                )
                # find_chunks_list = find_chunks(context=section_context, query=q_text, llm=llm_qa) # Optional
                # category_text = categorize_question(query=q_text, context=section_context, llm=llm_qa) # Optional
                # category = extract_category(category_text) # Optional

                query_items.append(
                    {
                        "_id": str(uuid.uuid4()),
                        "question": q_text,  # Changed from "query_text" to match generator loading
                        "answer": answer_text,  # Changed from "ref_answer"
                        "relevant_document_ids": [
                            {"corpus_id": corpus_doc_id, "score": 1.0}
                        ],
                        "metadata": {
                            # "category": category, # Optional
                            # "chunks_found": find_chunks_list # Optional
                        },
                    }
                )
        except Exception as e:
            print(f"Error generating Q&A for section {corpus_doc_id}: {e}")
            # Add a placeholder query if generation fails for a section
            query_items.append(
                {
                    "_id": str(uuid.uuid4()),
                    "question": f"Error generating question for {corpus_doc_id}",
                    "answer": str(e),
                    "relevant_document_ids": [
                        {"corpus_id": corpus_doc_id, "score": 1.0}
                    ],
                    "metadata": {"error": True},
                }
            )

    queries_file_path = os.path.join(output_dir, "queries.jsonl")
    with open(queries_file_path, "w", encoding="utf-8") as f_queries:
        for query_item in query_items:
            f_queries.write(json.dumps(query_item) + "\n")
    print(f"Queries saved to {queries_file_path}")

    print("TokenBurner GPT-2 processing finished.")
