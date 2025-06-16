import os
import json
from pathlib import Path
from typing import List, Dict, Optional
from ragformance.models.corpus import DocModel


# TODO Placeholder for actual LLM call logic
def _call_llm_for_queries(
    document_text: str,
    model_name: str,
    api_key: str,
    base_url: str,
    prompt_template: Optional[str],
    max_questions: int,
) -> List[str]:
    """
    Placeholder function to simulate LLM call for query generation.
    In a real implementation, this would use litellm or a similar library.
    """
    print(
        f"[Placeholder] Generating {max_questions} queries for document segment with model {model_name} at {base_url} using key {api_key}."
    )
    if prompt_template:
        print(f"[Placeholder] Using prompt template: {prompt_template}")

    # Simulate generating N questions
    generated_qs = []
    for i in range(max_questions):
        generated_qs.append(
            f"Placeholder question {i+1} for document starting with: {document_text[:50]}..."
        )
    return generated_qs


def generate_queries_from_corpus(
    corpus: List[DocModel],
    model_name: str,
    api_key: str,
    base_url: str,
    output_file_path: Path,
    prompt_template_path: Optional[str] = None,
    max_questions_per_doc: int = 5,
) -> List[Dict[str, str]]:
    """
    Generates synthetic queries for each document in the corpus.
    Writes the generated queries to output_file_path (JSONL format).
    Returns a list of dictionaries, where each dictionary represents a query.
    """
    raw_queries_list = []
    query_counter = 0

    prompt_template_content = None
    if prompt_template_path and os.path.exists(prompt_template_path):
        with open(prompt_template_path, encoding="utf-8") as f:
            prompt_template_content = f.read()
        print(f"Loaded query generation prompt template from: {prompt_template_path}")

    for doc in corpus:
        # In a real scenario, might chunk doc.text if too long for LLM context window
        # For now, using full text.
        generated_questions_for_doc = _call_llm_for_queries(
            document_text=doc.text,
            model_name=model_name,
            api_key=api_key,
            base_url=base_url,
            prompt_template=prompt_template_content,
            max_questions=max_questions_per_doc,
        )

        for q_text in generated_questions_for_doc:
            query_id = f"query_{doc.id}_{query_counter}"
            query_dict = {
                "query_id": query_id,
                "question": q_text,
                "doc_id": doc.id,  # doc_id links back to the source DocModel
            }
            raw_queries_list.append(query_dict)
            query_counter += 1

    # Write to output file
    output_dir = output_file_path.parent
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_file_path, "w", encoding="utf-8") as fout:
        for query_entry in raw_queries_list:
            fout.write(json.dumps(query_entry, ensure_ascii=False) + "\n")

    print(f"Saved {len(raw_queries_list)} generated queries to {output_file_path}")

    return raw_queries_list
