import os
import numpy as np
import uuid
from typing import Any, Optional
import json
from .parser import Manual, Page  # Corrected import


def format_query(
    text: str,
    references: list[dict],
    ref_answer: str,
    id: Optional[str] = None,
    metadata: Optional[dict] = None,
):
    return {
        "_id": str(uuid.uuid4()) if id is None else id,
        "text": text,
        "references": references,
        "ref_answer": ref_answer,
        "metadata": {} if metadata is None else metadata,
    }


def get_section_size_questions(manual: Manual) -> list[dict[str, Any]]:
    section_length_question_template = (
        "How many pages does the section titled {section_title} takes?"
    )
    section_length_questions = [
        format_query(
            text=section_length_question_template.format(section_title=section.title),
            references=[
                {"corpus_id": manual.pages[page_number - 1]._id, "score": 1}
                for page_number in section.pages_number
            ],
            ref_answer=str(len(section.pages_number)),
        )
        for section in manual.sections
    ]
    return section_length_questions


def get_section_size_size_comparison_questions(manual: Manual) -> list[dict[str, Any]]:
    sections_length = [len(section.pages_number) for section in manual.sections]
    id_longest_section = np.argmax(sections_length)
    longest_section_question = (
        "What is the title of the section with the longest number of pages?"
    )
    longest_section_qa = format_query(
        text=longest_section_question,
        references=[
            {"corpus_id": manual.pages[page_number - 1]._id, "score": 1}
            for page_number in manual.sections[id_longest_section].pages_number
        ],
        ref_answer=manual.sections[id_longest_section].title.strip("#"),
    )
    number_sections_with_same_nb_docs_template = (
        "how many question have {n} number of pages?"
    )
    set_sections_with_same_nb_docs_template = (
        "List the titles of the sections with {n} number of pages."
    )
    number_sections_qa_pairs = []
    set_sections_qa_pairs = []
    for i in range(len(manual.sections[id_longest_section].pages_number)):
        id_sections_length_i = list(np.where(np.array(sections_length) == i)[0])
        query_nb = format_query(
            text=number_sections_with_same_nb_docs_template.format(n=i),
            references=[
                {"corpus_id": manual.pages[page_number - 1]._id, "score": 1}
                for id_section in id_sections_length_i
                for page_number in manual.sections[id_section].pages_number
            ],
            ref_answer=str(len(id_sections_length_i)),
        )
        number_sections_qa_pairs.append(query_nb)
        query_set = format_query(
            text=set_sections_with_same_nb_docs_template.format(n=i),
            references=[
                {"corpus_id": manual.pages[page_number - 1]._id, "score": 1}
                for id_section in id_sections_length_i
                for page_number in manual.sections[id_section].pages_number
            ],
            ref_answer="\n".join(
                [
                    "-" + section.title
                    for section in np.array(manual.sections)[id_sections_length_i]
                ]
            ),
        )
        set_sections_qa_pairs.append(query_set)
    return [longest_section_qa] + number_sections_qa_pairs + set_sections_qa_pairs


def get_corpus(pages: list[Page], manual_name: str) -> list[str, str]:
    corpus = [
        {
            "_id": page._id,
            "title": f"Page {page.page_number} of {manual_name}",
            "text": page.content,
        }
        for page in pages
    ]
    return corpus


def run(folder_path: str, file_name: str = None, output_path: str = "output") -> None:
    """Generate the dataset composed of questions about the structure of the document.
    Args:
        folder_path (str): Path to the folder containing the data in markdown format.
        file_name (str): Name of the file to generate questions on. If set, only this file will be processed.
        output_path (str): Path to save the converted markdown files.
    """
    queries = []
    corpus = []
    if file_name is not None:
        manual = Manual.from_file(folder_path, file_name)
        corpus += get_corpus(manual.pages, manual.name)
        queries += get_section_size_questions(manual)
        queries += get_section_size_size_comparison_questions(manual)
    else:
        # iterate over all files in the folder
        for file in os.listdir(folder_path):
            manual = Manual.from_file(folder_path, file)
            corpus += get_corpus(manual.pages, manual.name)
            queries += get_section_size_questions(manual)
            queries += get_section_size_size_comparison_questions(manual)

    os.makedirs(output_path, exist_ok=True)
    corpus_path = os.path.join(output_path, "corpus.jsonl")
    queries_path = os.path.join(output_path, "queries.jsonl")

    with open(corpus_path, "w") as f:
        for line in corpus:
            f.write(json.dumps(line) + "\n")

    with open(queries_path, "w") as f:
        for line in queries:
            f.write(json.dumps(line) + "\n")
    return corpus, queries
