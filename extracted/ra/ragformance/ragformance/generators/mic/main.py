import math
import uuid
import numpy as np
import os
import json
from bs4 import BeautifulSoup
from markdown import markdown
from typing import Any
from .parser import ManualSplitter  # Corrected import
from .model import LLM  # Corrected import

DEFAULT_GENERATION_PROMPT = """
You goal is to find the concise question the following extract from a washing machine manual guide is answering.
You do not have access to the question but you must guess it.
The question is not general but focused on a specific aspect.
The extract is:
<extract>
{text}
</extract>
You MUST use the following template to answer (without any additional formatting or comments):
Reasoning:
Here give your short and concise reasoning (max 30 words) about what might be the missing question.
Question:
Here give the question the extract is the answer to.
If you do not use this manual your answer will not be taken into account.
If you do not know leave the question field empty.
Remember to first give your reasoning.
"""


def parse_outputs(outputs: list[str]) -> dict[str, str]:
    queries = []
    id_sections = []
    for id_query, out in enumerate(outputs):
        html = markdown(out)
        text = "".join(BeautifulSoup(html).findAll(text=True))
        splitted_text = text.split("Question:")
        if len(splitted_text) == 2:
            queries.append(splitted_text[-1])
            id_sections.append(id_query)
    return queries, id_sections


def format_query(query: str) -> dict[str, Any]:
    return {
        "_id": str(uuid.uuid4()),
        "query_text": query,
        "relevant_document_ids": [],
        "ref_answer": "This question can not be answered based on the available data",
        "metadata": {},
    }


def format_doc(
    section: str,
):
    print(section)
    splitted_section = section.strip().split("\n", maxsplit=1)
    return {
        "_id": str(uuid.uuid4()),
        "title": splitted_section[0],
        "text": splitted_section[-1],
    }


def generate_queries_and_corpus(
    splitter, llm, file_path, prompt_template, batch_size, num_queries
):
    splitted_manual = splitter.split_manual(file_path)
    llm.set_system_prompt(
        "You are an expert at guessing the concise question that a text answers."
    )
    prompts = [prompt_template.format(text=section) for section in splitted_manual]
    num_batch = math.ceil(len(prompts) / batch_size)
    outputs = []
    for id_batch in range(num_batch):
        end_batch = -1 if id_batch == (num_batch - 1) else (id_batch + 1) * batch_size
        outputs += llm.generate(prompts[id_batch * batch_size : end_batch])
    queries, id_sections = parse_outputs(outputs)
    id_sampled_queries = np.random.choice(
        len(queries), size=min(len(queries), num_queries), replace=False
    )
    sampled_queries = np.array(queries)[id_sampled_queries]
    id_sections_to_remove = np.array(id_sections)[id_sampled_queries]
    manual_to_keep = [
        section
        for idx, section in enumerate(splitted_manual)
        if idx in id_sections_to_remove
    ]
    formatted_queries = [format_query(query) for query in sampled_queries]
    formatted_corpus = [format_doc(section) for section in manual_to_keep]
    return formatted_queries, formatted_corpus


def run(
    file_path: str,
    output_path: str,
    model_name: str = "Qwen/Qwen2.5-1.5B-Instruct",
    prompt_template: str = DEFAULT_GENERATION_PROMPT,
    batch_size: int = 16,
    num_queries: int = 20,
) -> tuple[dict, dict]:
    # TODO replace with litellm or common LLM interface
    llm = LLM(model_name)
    splitter = ManualSplitter(llm.tokenizer, 500)

    # if path is a dir
    queries = []
    corpus = []
    if os.path.isdir(file_path):
        # iterate over all files in the directory
        for file in os.listdir(file_path):
            if file.endswith(".md") or file.endswith(".txt"):
                full_path = os.path.join(file_path, file)
                formatted_queries, formatted_corpus = generate_queries_and_corpus(
                    splitter, llm, full_path, prompt_template, batch_size, num_queries
                )
                queries.extend(formatted_queries)
                corpus.extend(formatted_corpus)

    else:
        queries, corpus = generate_queries_and_corpus(
            splitter, llm, file_path, prompt_template, batch_size, num_queries
        )

    corpus_path = os.path.join(output_path, "corpus.jsonl")
    queries_path = os.path.join(output_path, "queries.jsonl")
    with open(corpus_path, "w") as f:
        for line in corpus:
            f.write(json.dumps(line) + "\n")

    with open(queries_path, "w") as f:
        for line in queries:
            f.write(json.dumps(line) + "\n")

    return queries, corpus
