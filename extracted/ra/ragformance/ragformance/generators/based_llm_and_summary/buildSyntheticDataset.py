#!/usr/bin/env python3
"""
Build the two-file dataset required by BEIR-style benchmarks:

corpus.jsonl  :
    {"_id": str, "title": str, "text": str}

queries.jsonl :
    {"_id": str,
     "text": str,
     "references": [{"corpus_id": str, "score": float}],
     "ref_answer": str,
     "metadata": {...}}
"""

# ────────────────────────────── Imports ────────────────────────────────────
import os
import re
import yaml
import logging
from datetime import datetime
import litellm


# ────────────────────────  Logging setup  ──────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)


# ──────────────────────  Network / Proxy setup  ────────────────────────────
def set_proxy_environment(config_model) -> None:
    """Set proxy, no_proxy, and CA bundle env vars from the config_model object."""
    proxy = config_model.proxy_url or ""
    no_proxy = config_model.no_proxy_list or ""
    ca_bundle = config_model.ca_bundle_path

    if proxy:
        for key in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"):
            os.environ[key] = proxy
    if no_proxy:
        os.environ["NO_PROXY"] = no_proxy
        os.environ["no_proxy"] = no_proxy

    if ca_bundle:
        os.environ["CURL_CA_BUNDLE"] = ca_bundle
        os.environ["REQUESTS_CA_BUNDLE"] = ca_bundle
        os.environ["SSL_CERT_FILE"] = ca_bundle
    os.environ["OPENAI_LOG"] = "info"


# ─────────────────────────── External libs ─────────────────────────────────
try:
    from unstructured.partition.auto import partition
except ImportError as err:
    logger.error(
        "'unstructured[md]' module is not installed. "
        "Please install ragformance with the [generators-llm-summary] option:\n"
        "    pip install ragformance[generators-llm-summary]"
    )
    raise err


# ───────────────────────────  Helpers ──────────────────────────────────────
def extract_contents(file_path: str) -> str:
    """Extract raw text from an arbitrary file with unstructured."""
    try:
        elements = partition(file_path)
        return "\n".join(e.text for e in elements if getattr(e, "text", ""))
    except Exception as exc:
        logger.error("Failed to extract from %s : %s", file_path, exc)
        return ""


def create_summary(text: str, config_model) -> str:
    """Ask the LLM for a concise markdown summary."""
    try:
        response = litellm.completion(
            model="openai/" + config_model.llm_summary_model_name,
            messages=[
                {
                    "role": "user",
                    "content": "Write a concise markdown summary:\n\n" + text,
                }
            ],
            temperature=0.3,
            top_p=0.9,
            api_key=config_model.llm_api_key,
            base_url=config_model.llm_base_url,
        )
        return response.choices[0].message.content.strip()
    except Exception as err:  # General exception for litellm errors
        logger.error("Summary generation error: %s", err)
        return ""


SYSTEM_PROMPT = """
You will receive a short text (summary of a document).
1. Produce 10 diverse question-answer pairs about that text.
2. Ensure that the questions are relevant to the summary provided and vary in difficulty.
3. Return ONLY valid YAML that follows this exact schema:

questions:
- question: "<string>"
  answer: "<string>"
"""


def generate_questions_yaml(context: str, config_model, n_questions: int = 10) -> str:
    """Ask the LLM to create QA pairs in YAML."""
    try:
        response = litellm.completion(
            model="openai/" + config_model.llm_qa_model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Create {n_questions} questions and answers "
                    f"about:\n\n{context}",
                },
            ],
            temperature=0.3,
            top_p=0.9,
            api_key=config_model.llm_api_key,
            base_url=config_model.llm_base_url,
        )
        return response.choices[0].message.content.strip()
    except Exception as err:  # General exception for litellm errors
        logger.error("Q/A generation error: %s", err)
        return ""


def parse_questions_yaml(raw: str) -> list[dict]:
    """
    Convert the LLM output to Python list of dicts.
    Extremely defensive:  1) remove ``` fences  2) try YAML loader
                          3) fallback to regex extraction
    """

    txt = raw.strip()
    if txt.startswith("```"):
        txt = txt.split("\n", 1)[1]
    if txt.endswith("```"):
        txt = txt.rsplit("```", 1)[0]

    # Try normal YAML parsing first
    try:
        data = yaml.safe_load(txt)
        if isinstance(data, dict) and "questions" in data:
            return data["questions"]
    except yaml.YAMLError:
        pass

    # Fallback regex: - question: "...", answer: "..."
    qa_pairs = re.findall(
        r'question:\s*["“](.*?)["”]\s*.*?answer:\s*["“](.*?)["”]', txt, flags=re.S
    )
    return [{"question": q.strip(), "answer": a.strip()} for q, a in qa_pairs]


# ───────────────────────  Dataset builder  ─────────────────────────────────
def build_dataset(
    src_dir: str, include_ext: list[str] | tuple[str], config_model
) -> tuple[list[dict], list[dict]]:
    """
    Walk over src_dir, create corpus & query lists ready to save as jsonl.
    """
    corpus, queries = [], []
    corpus_id = 0
    query_id = 0
    timestamp = datetime.utcnow().isoformat()

    for root, _, files in os.walk(src_dir):
        for fname in files:
            if "_" not in include_ext and not any(
                fname.lower().endswith(ext) for ext in include_ext
            ):
                continue

            path = os.path.join(root, fname)
            text = extract_contents(path)
            if not text:
                continue

            # ---------------- corpus entry ----------------
            cid = str(corpus_id)
            corpus_id += 1
            corpus.append({"_id": cid, "title": fname, "text": text})

            # --------------- questions --------------------
            summary = (
                create_summary(text, config_model) or text[:2000]
            )  # fallback to raw text
            qa_yaml = generate_questions_yaml(summary, config_model)
            questions = parse_questions_yaml(qa_yaml)

            if not questions:
                logger.error("No Q/A pairs parsed for %s", fname)
                continue

            for qa in questions:
                queries.append(
                    {
                        "_id": str(query_id),
                        "text": qa["question"],
                        "references": [{"corpus_id": cid, "score": 1.0}],
                        "ref_answer": qa["answer"],
                        "metadata": {"source_file": fname, "generated_at": timestamp},
                    }
                )
                query_id += 1

    return corpus, queries
