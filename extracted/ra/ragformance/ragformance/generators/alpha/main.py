import logging


try:
    from forcolate import convert_folders_to_markdown
except ImportError:

    def convert_folders_to_markdown(*args, **kwargs):
        raise ImportError(
            "'forcolate' module is not installed. "
            "Please install ragformance with the [all] option:\n"
            "    pip install ragformance[all]"
        )


from ragformance.generators.alpha.prompts import (
    QUESTION_GENERATION_SYSTEM_PROMPT,
    QUESTION_GENERATION_USER_PROMPT,
    SUMMARIZATION_USER_PROMPT,
)
import pandas as pd
import os
import litellm
import re
import json
from typing import List, Dict, Any, Tuple
from ragformance.models.corpus import DocModel
from ragformance.models.answer import AnnotatedQueryModel
from pydantic import TypeAdapter

logger = logging.getLogger(__name__)


def _extract_tag_content(text: str, tag: str) -> str:
    """Extract text enclosed in <tag>...</tag> from the given string. Returns an empty string if the tag is not found."""
    if not text:
        return ""
    try:
        pattern = rf"<{tag}\s*>([\s\S]*?)</{tag}>"
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    except Exception as e:
        logger.error(f"Error extracting tag content for '{tag}': {e}")
    return ""


def _attempt_json_parse(json_str: str) -> Any:
    """Attempt to parse a JSON string. Return parsed object if success, or None if parsing fails."""
    try:
        return json.loads(json_str)
    except Exception:
        return None


def _maybe_strip_triple_backticks(text_in: str) -> str:
    """Removes triple backticks (``` or ```json) from the beginning and end of a string, if present."""
    if not text_in or not isinstance(text_in, str):
        return ""
    try:
        pattern = r"^\s*```(?:json)?\s*([\s\S]*?)\s*```$"
        match = re.match(pattern, text_in)
        if match:
            return match.group(1)
    except Exception as e:
        logger.error(f"Error stripping backticks: {e}")
    return text_in


def _best_effort_json_extract(full_text: str) -> list[str]:
    """Collect bracket-delimited substrings that might be valid JSON. Returns a list of candidates (which may be empty)."""
    if not full_text or not isinstance(full_text, str):
        return []
    candidates = []
    try:
        pattern = r"([\[{].*?[\]}])"
        matches = re.findall(pattern, full_text, flags=re.DOTALL)
        for match_text in matches:
            if (match_text.startswith("[") and match_text.endswith("]")) or (
                match_text.startswith("{") and match_text.endswith("}")
            ):
                candidates.append(match_text.strip())
    except Exception as e:
        logger.error(f"Error in best-effort JSON extraction: {e}")
    return candidates


def parse_qa_pairs_from_response(raw_response: str) -> list[dict[str, Any]]:
    """Attempt to parse question-answer pairs from a raw LLM response. Priority: <output_json>, ```json, best-effort bracket."""
    if not raw_response or not isinstance(raw_response, str):
        return []
    extracted_json_str = _extract_tag_content(raw_response, "output_json")
    if extracted_json_str.strip():
        possible_parsed = _attempt_json_parse(
            _maybe_strip_triple_backticks(extracted_json_str)
        )
        if isinstance(possible_parsed, list):
            return possible_parsed
    fence_pattern = r"```json\s*([\s\S]*?)\s*```"
    fence_match = re.search(fence_pattern, raw_response)
    if fence_match:
        possible_parsed = _attempt_json_parse(fence_match.group(1).strip())
        if isinstance(possible_parsed, list):
            return possible_parsed
    qa_pairs = []
    pair_blocks = re.findall(r"<qa_pair>(.*?)</qa_pair>", raw_response, re.DOTALL)
    for block in pair_blocks:
        question = _extract_tag_content(block, "question")
        answer = _extract_tag_content(block, "answer")
        if question and answer:
            qa_pairs.append({"question": question, "answer": answer})
    if qa_pairs:
        return qa_pairs
    questions = re.findall(r"<question>(.*?)</question>", raw_response, re.DOTALL)
    answers = re.findall(r"<answer>(.*?)</answer>", raw_response, re.DOTALL)
    if questions and answers:
        for q_text, a_text in zip(questions, answers):
            qa_pairs.append({"question": q_text.strip(), "answer": a_text.strip()})
        return qa_pairs
    return []


def call_backend_agent(
    system_prompt: str,
    user_prompt: str,
    api_key: str = "YOUR_KEY",
    base_url: str = "http://your.url/v1",
    model_name: str = "YOUR_MODEL",
    temperature: float = 0.7,
    max_tokens_to_sample: int = 2000,
    stop_sequences: List[str] = ["Observation:"],
):
    """Call a backend LLM agent and return the answer."""
    messages = []
    if system_prompt and system_prompt.strip():
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})
    try:
        logger.info(
            f"[call_backend_agent] Calling litellm with model {model_name} at {base_url}"
        )
        response = litellm.completion(
            model="openai/" + model_name,
            messages=messages,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature,
            max_tokens=max_tokens_to_sample,
            stop=stop_sequences,
        )
        if (
            response
            and response.choices
            and response.choices[0].message
            and response.choices[0].message.content
        ):
            answer = response.choices[0].message.content
            return answer
        else:
            logger.error(
                f"Error: Could not extract answer from litellm response: {response}"
            )
            return None
    except Exception as e:
        logger.error(f"Error calling litellm: {e}")
        return None


def summarize(
    document,
    API_KEY="YOUR_KEY",
    API_BASE_URL="http://your.url/v1",
    API_MODEL="YOUR_MODEL",
):
    """Summarize a document using the backend agent."""
    message = SUMMARIZATION_USER_PROMPT.format(document=document)
    answer = call_backend_agent(
        system_prompt="",
        user_prompt=message,
        api_key=API_KEY,
        base_url=API_BASE_URL,
        model_name=API_MODEL,
    )
    final_summary = _extract_tag_content(answer, "final_summary") if answer else ""
    return final_summary


def _split_into_sentences(text: str) -> list[str]:
    """Splits the input text into sentences using a simple rule-based approach that looks for punctuation delimiters ('.', '!', '?')."""
    normalized_text = text.replace("\n", " ").strip()
    if normalized_text is None or normalized_text == "":
        return []
    segments = re.split(r"([.!?])", normalized_text)
    sentences: list[str] = []
    for i in range(0, len(segments), 2):
        if i + 1 < len(segments):
            candidate = (segments[i] + segments[i + 1]).strip()
        else:
            candidate = segments[i].strip()
        if candidate:
            sentences.append(candidate)
    return sentences


# TODO uniformize chunking across generators
def _chunk_document_fast(
    sentences: list[str],
    l_max_tokens: int,
    doc_id: str,
) -> List[Tuple[str, str]]:
    """Creates chunks based purely on a maximum token length."""
    chunks: List[Tuple[str, str]] = []
    current_chunk: list[str] = []
    current_len: int = 0
    chunk_index: int = 0
    for sentence in sentences:
        sentence_token_count = len(sentence.split())
        if current_len + sentence_token_count > l_max_tokens:
            if current_chunk:
                chunk_str = " ".join(current_chunk)
                chunks.append((f"{doc_id}_{chunk_index}", chunk_str))
                chunk_index += 1
            current_chunk = [sentence]
            current_len = sentence_token_count
        else:
            current_chunk.append(sentence)
            current_len += sentence_token_count
    if current_chunk:
        chunk_str = " ".join(current_chunk)
        chunks.append((f"{doc_id}_{chunk_index}", chunk_str))
    return chunks


def generate_questions(
    chunks: List[Tuple[str, str]],
    file_name_md: str,
    doc_summary: str,
    output_path_parquet: str = "questions",
    API_KEY="YOUR_KEY",
    API_BASE_URL="http://your.url/v1",
    API_MODEL="YOUR_MODEL",
):
    """Generate questions and answers for document chunks using an LLM."""
    data = []
    if not os.path.exists(output_path_parquet):
        os.makedirs(output_path_parquet)
    doc_name_no_ext = file_name_md.replace(".md", "")
    for chunk_id_str, chunk_text in chunks:
        message = QUESTION_GENERATION_USER_PROMPT.format(
            title=doc_name_no_ext,
            document_summary=doc_summary,
            text_chunk=chunk_text,
            additional_instructions="",
        )
        raw_response_content = call_backend_agent(
            system_prompt=QUESTION_GENERATION_SYSTEM_PROMPT,
            user_prompt=message,
            api_key=API_KEY,
            base_url=API_BASE_URL,
            model_name=API_MODEL,
        )
        if not raw_response_content:
            logger.warning(
                f"No response from LLM for chunk {chunk_id_str} in file {file_name_md}"
            )
            continue
        parsed_qa_list = parse_qa_pairs_from_response(raw_response_content)
        if not parsed_qa_list:
            logger.warning(
                f"No QA pairs parsed for chunk {chunk_id_str} in file {file_name_md}"
            )
            continue
        for qa_pair in parsed_qa_list:
            question = qa_pair.get("question")
            answer = qa_pair.get("answer")
            if not question or not answer:
                continue
            data.append(
                {
                    "document_name": doc_name_no_ext,
                    "summary": doc_summary,
                    "chunk_id": chunk_id_str,
                    "chunk_text": chunk_text,
                    "question": question,
                    "answer": answer,
                }
            )
    if not data:
        logger.warning(f"No questions generated for file {file_name_md}")
        return
    df = pd.DataFrame(data)
    parquet_file_path = os.path.join(output_path_parquet, f"{doc_name_no_ext}.parquet")
    df.to_parquet(parquet_file_path, index=False)


def parquet_to_jsonl(
    parquet_folder_path: str,
) -> Tuple[List[DocModel], List[AnnotatedQueryModel]]:
    """Convert a folder of parquet files to JSONL corpus and queries."""
    ta_doc = TypeAdapter(List[DocModel])
    ta_query = TypeAdapter(List[AnnotatedQueryModel])
    corpus_list: List[Dict[str, Any]] = []
    queries_list: List[Dict[str, Any]] = []
    query_id_counter = 0
    for file_name in os.listdir(parquet_folder_path):
        if file_name.endswith(".parquet"):
            logger.info(f"Processing parquet file: {file_name}")
            df = pd.read_parquet(os.path.join(parquet_folder_path, file_name))
            for row in df.itertuples(index=False):
                doc_name = getattr(row, "document_name", "")
                chunk_id = str(getattr(row, "chunk_id", ""))
                chunk_text = getattr(row, "chunk_text", "")
                question_text = getattr(row, "question", "")
                answer_text = getattr(row, "answer", "")
                if not chunk_id or not chunk_text:
                    logger.warning(
                        f"Skipping row due to missing chunk_id or chunk_text in {file_name}"
                    )
                    continue
                queries_list.append(
                    {
                        "_id": str(query_id_counter),
                        "query_text": question_text,
                        "relevant_document_ids": [{"corpus_id": chunk_id, "score": 1}],
                        "ref_answer": answer_text,
                    }
                )
                corpus_list.append(
                    {
                        "_id": chunk_id,
                        "title": doc_name,
                        "text": chunk_text,
                    }
                )
                query_id_counter += 1
    if corpus_list:
        seen_ids = set()
        deduplicated_corpus = []
        for item in corpus_list:
            item_id = item.get("_id")
            if item_id not in seen_ids:
                seen_ids.add(item_id)
                deduplicated_corpus.append(item)
        corpus_list = deduplicated_corpus
    corpus_jsonl_path = os.path.join(parquet_folder_path, "corpus.jsonl")
    queries_jsonl_path = os.path.join(parquet_folder_path, "queries.jsonl")
    with open(corpus_jsonl_path, "w", encoding="utf-8") as f:
        for item in corpus_list:
            f.write(json.dumps(item) + "\n")
    with open(queries_jsonl_path, "w", encoding="utf-8") as f:
        for item in queries_list:
            f.write(json.dumps(item) + "\n")
    validated_corpus = ta_doc.validate_python(corpus_list)
    validated_queries = ta_query.validate_python(queries_list)
    return validated_corpus, validated_queries
