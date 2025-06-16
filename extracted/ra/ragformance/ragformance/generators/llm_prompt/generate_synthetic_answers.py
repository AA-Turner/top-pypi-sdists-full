import os
import json
from pathlib import Path
from typing import List, Dict, Optional
from ragformance.models.corpus import DocModel  # For type hinting if context is needed


# TODO Placeholder for actual LLM call logic
def _call_llm_for_answer(
    question_text: str,
    document_text: str,
    model_name: str,
    api_key: str,
    base_url: str,
    prompt_template: Optional[str],
) -> str:
    """
    Placeholder function to simulate LLM call for answer generation.
    In a real implementation, this would use litellm or a similar library.
    """
    print(
        f"[Placeholder] Generating answer for question '{question_text[:50]}...' using document segment '{document_text[:50]}...' with model {model_name} at {base_url} using key {api_key}."
    )
    if prompt_template:
        print(f"[Placeholder] Using prompt template: {prompt_template}")

    return f"Placeholder answer for: {question_text[:50]}..."


def generate_answers_for_queries(
    queries: List[
        Dict[str, str]
    ],  # Expects list of dicts with "query_id", "question", "doc_id"
    corpus: List[DocModel],
    model_name: str,
    api_key: str,
    base_url: str,
    output_file_path: Path,
    prompt_template_path: Optional[str] = None,
) -> List[Dict[str, str]]:
    """
    Generates synthetic answers for each query using the relevant document from the corpus.
    Updates the query dictionaries with an 'answer' field.
    Writes the updated queries to output_file_path (JSONL format).
    Returns the list of query dictionaries with answers.
    """

    prompt_template_content = None
    if prompt_template_path and os.path.exists(prompt_template_path):
        with open(prompt_template_path, encoding="utf-8") as f:
            prompt_template_content = f.read()
        print(f"Loaded answer generation prompt template from: {prompt_template_path}")

    # Create a quick lookup for documents by their ID
    corpus_map = {doc.id: doc for doc in corpus}

    updated_queries_with_answers = []

    for query_dict in queries:
        doc_id = query_dict.get("doc_id")
        document = corpus_map.get(doc_id)

        if not document:
            print(
                f"Warning: Document with ID '{doc_id}' not found for query '{query_dict['query_id']}'. Skipping answer generation for this query."
            )
            query_dict["answer"] = "Error: Source document not found."
            updated_queries_with_answers.append(query_dict)
            continue

        # In a real scenario, might need more sophisticated context retrieval than just full doc text
        answer_text = _call_llm_for_answer(
            question_text=query_dict["question"],
            document_text=document.text,
            model_name=model_name,
            api_key=api_key,
            base_url=base_url,
            prompt_template=prompt_template_content,
        )

        query_dict["answer"] = answer_text  # Add the answer to the dictionary
        updated_queries_with_answers.append(query_dict)

    # Write to output file
    output_dir = output_file_path.parent
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_file_path, "w", encoding="utf-8") as fout:
        for query_entry in updated_queries_with_answers:
            fout.write(json.dumps(query_entry, ensure_ascii=False) + "\n")

    print(
        f"Saved {len(updated_queries_with_answers)} queries with answers to {output_file_path}"
    )

    return updated_queries_with_answers
