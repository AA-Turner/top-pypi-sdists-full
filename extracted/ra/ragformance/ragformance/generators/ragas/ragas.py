# Removed imports for get_generator_instance, get_querydistribution_instance

try:
    from langchain_community.document_loaders import (
        DirectoryLoader,
        TextLoader,
    )  # Added TextLoader
    from ragas.testset.generator import TestsetGenerator  # Corrected import path
    from ragas.testset.graph import NodeType
    from ragas.testset.distribution import QueryDistribution  # For type hinting

    _RAGAS_AVAILABLE = True
except ImportError:
    _RAGAS_AVAILABLE = False
    DirectoryLoader = None
    TextLoader = None
    TestsetGenerator = None
    NodeType = None
    QueryDistribution = None

import os
import json
import uuid
import sys
from pathlib import Path  # For path operations
from typing import List, Tuple, Dict, Optional  # For type hinting


def _validate_input_files(datapath_str: str) -> bool:
    datapath_obj = Path(datapath_str)
    if not datapath_obj.exists():
        print(f"Error: The path '{datapath_str}' does not exist.")
        sys.exit(1)  # Or raise error

    valid_files_to_process = []
    if datapath_obj.is_dir():
        files_in_dir = os.listdir(datapath_str)
        valid_files_in_dir = [
            f for f in files_in_dir if f.lower().endswith((".txt", ".md"))
        ]
        if not valid_files_in_dir:
            print(f"Error: No .txt or .md files found in directory '{datapath_str}'.")
            sys.exit(1)  # Or raise error
        valid_files_to_process = valid_files_in_dir
    elif datapath_obj.is_file():
        if not datapath_str.lower().endswith((".txt", ".md")):
            print(f"Error: File '{datapath_str}' is not a .txt or .md file.")
            sys.exit(1)  # Or raise error
        valid_files_to_process = [datapath_obj.name]
    else:
        print(f"Error: Path '{datapath_str}' is not a valid file or directory.")
        sys.exit(1)  # Or raise error

    print("Files to be processed:")
    for f_name in valid_files_to_process:
        print(f" - {f_name}")
    return True


def _relationship_condition(rel):
    # Define your condition as a lambda
    return rel.type == "child"


def _extract_corpus_items(kg):
    corpus_items = []

    # The corpus will be formed only by the chunks of the RAGAS knowledge graph
    corpus_id_set = set()  # To avoid duplicate corpus entries

    if kg is None:
        print("Warning: Knowledge graph is None. Cannot extract corpus items.")
        return []

    relationship_condition = _relationship_condition
    result = kg.find_two_nodes_single_rel(relationship_condition)

    for node_a, rel, node_b in result:
        current_corpus_id = None
        current_corpus_text = None
        current_corpus_title = None  # Initialize title

        # Prioritize CHUNK nodes for text and ID
        for node in [node_a, node_b]:  # Check both nodes
            if getattr(node, "type", None) == NodeType.CHUNK:
                current_corpus_text = getattr(node, "properties", {}).get(
                    "page_content", ""
                )
                current_corpus_id = str(node.id)
                # Try to get title from the document this chunk belongs to
                # This assumes a DOCUMENT node is related to this CHUNK node, which might not always be direct in find_two_nodes_single_rel
                # A more robust way would be to traverse from chunk to its parent document if KG structure allows.
                # For now, we'll try to find a DOCUMENT node in the pair.
                doc_node_for_title = (
                    node_a
                    if getattr(node_b, "type", None) == NodeType.DOCUMENT
                    else (
                        node_b
                        if getattr(node_a, "type", None) == NodeType.DOCUMENT
                        else None
                    )
                )
                if (
                    not doc_node_for_title
                ):  # If CHUNK is paired with another CHUNK, search for related DOCUMENT
                    try:
                        # This is a conceptual search; actual KG traversal might differ
                        related_docs = [
                            n
                            for n_id in kg.G.neighbors(node.id)
                            for n in [kg.G.nodes[n_id]["data"]]
                            if getattr(n, "type", None) == NodeType.DOCUMENT
                        ]
                        if related_docs:
                            doc_node_for_title = related_docs[0]
                    except Exception:
                        pass  # KG structure might not support this easily

                if doc_node_for_title:
                    current_corpus_title = (
                        getattr(doc_node_for_title, "properties", {})
                        .get("document_metadata", {})
                        .get("source", "")
                    )
                break  # Found a CHUNK, prioritize its ID and text

        # If no CHUNK node gave an ID, try a DOCUMENT node from the pair (less ideal for corpus)
        if current_corpus_id is None:
            for node in [node_a, node_b]:
                if getattr(node, "type", None) == NodeType.DOCUMENT:
                    current_corpus_id = str(node.id)
                    if current_corpus_text is None:  # If CHUNK text wasn't found
                        current_corpus_text = getattr(node, "properties", {}).get(
                            "page_content", ""
                        )  # Some docs might have raw text
                    if current_corpus_title is None:
                        current_corpus_title = (
                            getattr(node, "properties", {})
                            .get("document_metadata", {})
                            .get("source", "")
                        )
                    break

        if current_corpus_id and current_corpus_id not in corpus_id_set:
            corpus_items.append(
                {
                    "_id": current_corpus_id,
                    "title": current_corpus_title
                    if current_corpus_title
                    else "Unknown Title",
                    "text": current_corpus_text if current_corpus_text else "",
                }
            )
            corpus_id_set.add(current_corpus_id)
        elif not current_corpus_id:
            print(
                "Warning: Could not determine a corpus ID for a node pair in KG during corpus extraction."
            )

    if not corpus_items:
        print(
            "Warning: No corpus items extracted from the knowledge graph. This might happen if the graph is empty or only contains DOCUMENT nodes without extractable CHUNK information via selected relationships."
        )

    return corpus_items


def _extract_chunk_id(chunk_str: str, kg) -> Optional[str]:
    if kg is None:
        print(
            f"Warning: Knowledge graph is None. Cannot extract chunk ID for: {chunk_str[:50]}..."
        )
        return None

    relationship_condition = _relationship_condition
    # find_two_nodes_single_rel might not be the most efficient if we just need to find a chunk by content
    # A direct node lookup or search by property would be better if available.
    # Assuming we must use this for now:
    result = kg.find_two_nodes_single_rel(relationship_condition)

    # Using a smaller, more distinctive part of the string might be better
    # Also, handle potential leading/trailing whitespace differences.
    search_str_key = chunk_str.strip()[:50]  # Use a key portion for matching

    for node_a, rel, node_b in result:
        for node in [node_a, node_b]:
            if getattr(node, "type", None) == NodeType.CHUNK:
                page_content = getattr(node, "properties", {}).get("page_content", "")
                if page_content.strip()[:50] == search_str_key:  # Compare key portions
                    return str(node.id)

    print(
        f"Warning: Could not find chunk_id for content starting with: {search_str_key}"
    )
    return None


def run_ragas_core(  # Renamed from run
    datapath: str,
    output_path: str,
    ragas_testset_generator: TestsetGenerator,
    n_questions: int,
    query_distribution: Optional[QueryDistribution] = None,
    save_ragas_kg: bool = True,
    # **kwargs removed as TestsetGenerator.generate_with_langchain_docs specific args are handled
) -> Tuple[List[Dict], List[Dict]]:
    if not _RAGAS_AVAILABLE:
        raise ImportError(
            "'ragas' module is not installed. "
            "Please install ragformance with the [generators-ragas] option:\n"
            "    pip install ragformance[generators-ragas]"
        )

    _validate_input_files(datapath)

    datapath_obj = Path(datapath)
    if datapath_obj.is_dir():
        loader = DirectoryLoader(
            datapath,
            glob="**/[!.]*",
            show_progress=True,
            use_multithreading=False,
            silent_errors=True,
        )  # Process all files except hidden
    elif datapath_obj.is_file():
        loader = TextLoader(datapath)
    else:
        raise ValueError(
            f"Path {datapath} is not a valid directory or file."
        )  # Should be caught by _validate

    docs = loader.load()
    if not docs:
        print(f"No documents loaded from {datapath}. Exiting.")
        return [], []

    generation_args = {"test_size": n_questions}
    if query_distribution:
        generation_args["distributions"] = query_distribution

    print(
        f"Generating RAGAS testset with TestsetGenerator.generate_with_langchain_docs and args: {generation_args}"
    )
    dataset = ragas_testset_generator.generate_with_langchain_docs(
        docs, **generation_args
    )

    kg_to_use = None
    if (
        hasattr(ragas_testset_generator, "knowledge_graph")
        and ragas_testset_generator.knowledge_graph
    ):
        kg_to_use = ragas_testset_generator.knowledge_graph
        if save_ragas_kg:
            kg_path = os.path.join(output_path, "knowledge_graph_ragas.json")
            os.makedirs(os.path.dirname(kg_path), exist_ok=True)  # Ensure dir exists
            try:
                kg_to_use.save(kg_path)
                print(f"Saved RAGAS knowledge graph to {kg_path}")
            except Exception as e:
                print(f"Failed to save RAGAS knowledge graph: {e}")
    else:
        print("Knowledge graph not found or not populated in TestsetGenerator.")

    query_items = []
    # RAGAS 0.1.x dataset format
    for data_item in dataset.to_list():
        question = data_item.get("question", "")
        ground_truth = data_item.get(
            "ground_truth", ""
        )  # RAGAS 0.1.x uses "ground_truth"
        contexts = data_item.get("contexts", [])  # RAGAS 0.1.x uses "contexts"
        evolution_type = data_item.get("evolution_type", "")  # RAGAS 0.1.x

        query_item = {
            "_id": str(uuid.uuid4()),
            "text": question,
            "ref_answer": ground_truth,
            "references": [
                {
                    "corpus_id": _extract_chunk_id(chunk_str=context, kg=kg_to_use),
                    "score": 1.0,  # Default score
                }
                for context in contexts
            ],
            "metadata": {"evolution_type": evolution_type},
        }
        # Filter out references where corpus_id could not be found
        query_item["references"] = [
            ref for ref in query_item["references"] if ref["corpus_id"] is not None
        ]
        query_items.append(query_item)

    corpus_items = _extract_corpus_items(kg=kg_to_use)

    corpus_path = os.path.join(output_path, "corpus.jsonl")
    queries_path = os.path.join(output_path, "queries.jsonl")

    # save corpus and queries to json lines files

    # Ensure the folder exists
    os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
    with open(corpus_path, "w") as f:
        for line in corpus_items:
            f.write(json.dumps(line) + "\n")

    # Ensure the folder exists
    os.makedirs(os.path.dirname(queries_path), exist_ok=True)
    with open(queries_path, "w") as f:
        for line in query_items:
            f.write(json.dumps(line) + "\n")

    return corpus_items, query_items
