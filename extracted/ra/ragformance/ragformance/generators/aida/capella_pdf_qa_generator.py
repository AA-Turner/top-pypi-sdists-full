"""
capella_pdf_qa_generator.py

AIDA Architecture Processing Pipeline.

This module provides an end-to-end pipeline to:

1. Build a directed graph of Capella model elements from an XML file.
2. Extract and resolve entities mentioned in user queries.
3. Retrieve and rank relevant XML snippets and PDF chunks.
4. Generate BEIR-style `corpus.jsonl` (PDF text chunks) and `queries.jsonl`
   (ten generated Q-A pairs per seed question) using LLMs.

Usage:
    from ragformance.data_generation.generators.capella_pdf_qa_generator import run

    run(
        seed_questions_path=Path("questions.json"),
        data_dir=Path("./pdfs"),
        output_dir=Path("results"),
        openrouter_key=os.getenv("OPENROUTER_API_KEY"),
        openrouter_base_url=os.getenv("OPENROUTER_BASE_URL"),
        hf_embed_model="ibm-granite/granite-embedding-30m-english",
        capella_path=Path("./model.capella"),
        entity_model_name="google/gemini-2.0-flash-001",
        qa_model_name="google/gemini-2.5-pro-preview",
    )


"""

import re
import uuid
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import networkx as nx
from lxml import etree
from rapidfuzz import process, fuzz
from pydantic import BaseModel, Field
import litellm

try:
    import instructor
except ImportError:
    instructor = None  # TODO put structured output in common
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# Constants & Data Models

XMI_NS_URI = "http://www.omg.org/XMI"
ID_ATTRS = [f"{{{XMI_NS_URI}}}id", "id"]
TAG_RE = re.compile(r"\[S[a-f0-9]{6}\]", re.I)


class EntityList(BaseModel):
    """Schema for a list of extracted Capella entity names."""

    entities: List[str] = Field(
        ..., description="exact names as they appear in Capella"
    )


class QA(BaseModel):
    """Schema for a single Q-A pair."""

    question: str
    answer: str
    sources: List[str]


class QASet(BaseModel):
    """Schema for a full set of ten categorized Q-A pairs."""

    simple_fact: QA
    simple_conditional: QA
    comparison: QA
    interpretative: QA
    multi_answer: QA
    aggregation: QA
    multi_hop: QA
    heavy_post: QA
    erroneous: QA
    summary: QA


# XML / Graph Utilities


def iter_capella_elements(xml_path: Path):
    print(f"[iter_capella_elements] Parsing XML file: {xml_path}")
    for _, elem in etree.iterparse(str(xml_path), events=("end",)):
        yield elem
        elem.clear()
        parent = elem.getparent()
        if parent is not None:
            while elem.getprevious() is not None:
                del parent[0]
    print(f"[iter_capella_elements] Completed parsing {xml_path}")


def get_node_id(elem: etree._Element) -> str:
    for attr in ID_ATTRS:
        nid = elem.get(attr)
        if nid:
            return nid
    return None


def build_network(xml_path: Path) -> nx.DiGraph:
    print(f"[build_network] Building Capella graph from {xml_path}")
    G = nx.DiGraph()
    for elem in iter_capella_elements(xml_path):
        nid = get_node_id(elem)
        if not nid:
            continue
        G.add_node(
            nid,
            tag=etree.QName(elem.tag).localname,
            name=elem.get("name", ""),
            file=str(xml_path.resolve()),
            line=elem.sourceline,
            description=elem.get("description", ""),
        )
        parent = elem.getparent()
        pid = get_node_id(parent) if parent is not None else None
        if pid:
            G.add_edge(pid, nid, type="contains")
    print(
        f"[build_network] Completed graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges"
    )
    return G


# Entity Extraction Setup


def setup_entity_extractor(
    model_name: str, api_key: str, api_base: str
) -> Tuple[ChatPromptTemplate, type[BaseModel], str, str, str]:
    # Patch litellm to use Pydantic models if not already patched
    if not hasattr(litellm, "_patched_with_instructor"):
        instructor.patch(litellm)
        litellm._patched_with_instructor = True

    inst = PydanticOutputParser(pydantic_object=EntityList).get_format_instructions()
    inst = inst.replace("{", "{{").replace("}", "}}")  # Keep for prompt construction
    system = SystemMessagePromptTemplate.from_template(
        "You are an assistant that extracts Capella element names "
        "from user queries and returns them **only** as JSON matching this schema:\n\n"
        + inst
    )
    print(f"[setup_entity_extractor] Configuring extractor for LLM: {model_name}")
    user = HumanMessagePromptTemplate.from_template("{user_query}")
    prompt = ChatPromptTemplate.from_messages([system, user])
    print("[setup_entity_extractor] Extractor prompt and response model configured")
    return prompt, EntityList, model_name, api_key, api_base


# Name Index & Fuzzy Matching


def build_name_index(G: nx.DiGraph) -> Dict[str, List[str]]:
    print("[build_name_index] Building name index from graph nodes")
    idx: Dict[str, List[str]] = {}
    for nid, attrs in G.nodes(data=True):
        key = attrs["name"].lower()
        idx.setdefault(key, []).append(nid)
    print(f"[build_name_index] Name index size: {len(idx)}")
    return idx


def fuzzy_candidates(
    query: str, choices: Dict[str, str], top_k: int = 5, score_cutoff: int = 80
):
    return (
        (nid, score)
        for nid, score, _ in process.extract(
            query, choices, scorer=fuzz.token_set_ratio, limit=top_k
        )
        if score >= score_cutoff
    )


def resolve_entity(
    entity: str,
    name_index: Dict[str, List[str]],
    choices: Dict[str, str],
    *,
    fuzzy: bool = True,
) -> List[str]:
    key = entity.lower()
    if key in name_index:
        print(f"[resolve_entity] Exact match for '{entity}': {name_index[key]}")
        return name_index[key]
    if fuzzy:
        cands = [nid for nid, _ in fuzzy_candidates(entity, choices)]
        print(f"[resolve_entity] Fuzzy candidates for '{entity}': {cands}")
        return cands
    print(f"[resolve_entity] No match for '{entity}'")
    return []


# XML Slicing & Tag Utilities


def slice_xml(node_attrs: dict, *, context_lines: int = 0) -> str:
    path = Path(node_attrs["file"])
    start = max(node_attrs["line"] - 1 - context_lines, 0)
    lines = path.read_text(encoding="utf-8").splitlines()
    open_t, close_t = f"<{node_attrs['tag']}", f"</{node_attrs['tag']}>"
    depth, end = 0, None
    for i, ln in enumerate(lines[node_attrs["line"] - 1 :], start=node_attrs["line"]):
        if open_t in ln:
            depth += ln.count(open_t)
        if close_t in ln:
            depth -= ln.count(close_t)
        if depth <= 0 and end is None:
            end = i
    end = end if end is not None else len(lines) - 1
    return "\n".join(lines[start : end + context_lines + 1])


def extract_tags(text: str) -> List[str]:
    seen, out = set(), []
    for m in TAG_RE.findall(text):
        t = m.strip("[]")
        if t not in seen:
            out.append(t)
            seen.add(t)
    return out


def slice_relevant_xml(nid: str, G: nx.DiGraph) -> str:
    raw = slice_xml(G.nodes[nid])
    if any(x in raw for x in ("ownedDiagrams", "layoutData", "filters")):
        return ""
    clean = re.sub(r"\s+", " ", raw).strip()
    return clean[:600] + ("…" if len(clean) > 600 else "")


def resolve_tag(tag: str, src_map: dict, G: nx.DiGraph) -> dict:
    e = src_map.get(tag)
    if not e:
        print(f"[resolve_tag] Tag {tag} not found")
        return {"tag": tag, "error": "not_found"}
    if e["kind"] == "pdf":
        print(f"[resolve_tag] Resolved PDF tag {tag} → page {e['page']}")
        return {"tag": tag, "kind": "pdf", "page": e["page"], "snippet": e["snippet"]}
    attrs = G.nodes[e["id"]]
    snippet = slice_relevant_xml(e["id"], G)
    print(f"[resolve_tag] Resolved Capella tag {tag} → node {e['id']}")
    return {"tag": tag, "kind": "capella", **attrs, "snippet": snippet}


# QA Pipeline Setup


def setup_qa_llm(
    model_name: str, api_key: str, api_base: str
) -> Tuple[type[BaseModel], str, str, str]:
    # Patch litellm to use Pydantic models if not already patched
    if not hasattr(litellm, "_patched_with_instructor"):
        instructor.patch(litellm)
        litellm._patched_with_instructor = True

    print(f"[setup_qa_llm] Configuring QA for LLM: {model_name}")
    # Pydantic model QASet is the "parser" or response model
    print("[setup_qa_llm] QA response model configured")
    return QASet, model_name, api_key, api_base


def generate_qa_set(
    user_query: str,
    G: nx.DiGraph,
    vectordb: Chroma,
    embed_model: str,
    # Parameters from setup_entity_extractor
    extract_prompt_template: ChatPromptTemplate,
    extract_response_model: type[BaseModel],
    entity_model_name: str,
    entity_api_key: str,
    entity_api_base: str,
    # Parameters from setup_qa_llm
    qa_response_model: type[BaseModel],
    qa_model_name: str,
    qa_api_key: str,
    qa_api_base: str,
    name_index: Dict[str, List[str]],
    choices: Dict[str, str],
    k_pdf: int = 5,
    k_capella: int = 8,
) -> Tuple[dict, dict]:
    print(f"[generate_qa_set] Generating QA for query: '{user_query}'")

    # 1) Entity extraction
    prompt_messages_lc = extract_prompt_template.format_prompt(
        user_query=user_query
    ).to_messages()
    messages = []
    for msg in prompt_messages_lc:
        role = msg.type
        if role == "human":
            role = "user"
        elif role == "ai":
            role = "assistant"
        messages.append({"role": role, "content": msg.content})

    print(
        f"[generate_qa_set] Calling litellm for entity extraction with model {entity_model_name}"
    )
    extracted_data = litellm.completion(
        model="openai/" + entity_model_name,
        messages=messages,
        api_key=entity_api_key,
        base_url=entity_api_base,
        response_model=extract_response_model,
    )
    entities = extracted_data.entities if extracted_data else []
    print(f"[generate_qa_set] Extracted entities: {entities}")

    resolved = {e: resolve_entity(e, name_index, choices) for e in entities}
    print(f"[generate_qa_set] Resolved entities to IDs: {resolved}")

    raw_ids = [nid for ids in resolved.values() for nid in ids]
    missing = [nid for nid in raw_ids if nid not in G.nodes]
    if missing:
        print(
            f"[generate_qa_set] Warning: these IDs not in graph and will be skipped: {missing}"
        )
    flat_ids = [nid for nid in raw_ids if nid in G.nodes]

    # 2) Capella snippet ranking (skip if none)
    capella_blocks, src_map = [], {}
    if flat_ids:
        print("[generate_qa_set] Embedding query and descriptions")
        rank_emb = HuggingFaceEmbeddings(model_name=embed_model)
        q_vec = rank_emb.embed_query(user_query)
        descs = [G.nodes[n].get("description") or G.nodes[n]["name"] for n in flat_ids]
        doc_vecs = rank_emb.embed_documents(descs)
        scores = np.dot(doc_vecs, q_vec)
        top_nids = [flat_ids[i] for i in np.argsort(scores)[-k_capella:][::-1]]
        print(f"[generate_qa_set] Top Capella node IDs: {top_nids}")
        for nid in top_nids:
            xml = slice_relevant_xml(nid, G)
            if not xml:
                continue
            sid = f"S{uuid.uuid4().hex[:6]}"
            node = G.nodes[nid]
            src_map[sid] = {
                "kind": "capella",
                "id": nid,
                "tag": node["tag"],
                "name": node["name"],
                "snippet": xml,
            }
            capella_blocks.append(f"[{sid}] ({node['tag']})\n```xml\n{xml}\n```")
        print(f"[generate_qa_set] Built {len(capella_blocks)} Capella snippet blocks")
    else:
        print("[generate_qa_set] No Capella IDs to rank; skipping.")

    # 3) PDF retrieval
    pdf_blocks = []
    for ch in vectordb.similarity_search(user_query, k=k_pdf):
        sid = f"S{uuid.uuid4().hex[:6]}"
        # Ensure ch.metadata contains "corpus_id" which was added before Chroma ingestion
        src_map[sid] = {
            "kind": "pdf",
            "corpus_id": ch.metadata.get("corpus_id"),  # Added corpus_id
            "page": ch.metadata.get("page", "?"),
            "snippet": ch.page_content,
        }
        pdf_blocks.append(f"[{sid}] (page {src_map[sid]['page']})\n{ch.page_content}")
    print(f"[generate_qa_set] Retrieved {len(pdf_blocks)} PDF blocks")

    # 4) Assemble & invoke QA prompt
    cat_desc = """
    1. simple_fact          : a single factual answer.
    2. simple_conditional    : answer depends on an 'if' condition.
    3. comparison            : compare / evaluate two items.
    4. interpretative        : requires interpretation of intent / rationale.
    5. multi_answer          : expects a set/list of items.
    6. aggregation           : numeric or textual aggregation.
    7. multi_hop             : needs reasoning over ≥2 facts.
    8. heavy_post            : answer needs transformation (e.g., unit conversion).
    9. erroneous             : user premise wrong; correct it politely.
    10. summary              : produce a concise summary.
    """
    # schema = qa_ps.get_format_instructions().replace("{","{{").replace("}", "}}") # This line is removed, qa_ps is not defined here.
    # sys_msg below is not used, sys_msg_for_prompt is used.

    # qa_ps (PydanticOutputParser for QASet) is replaced by qa_response_model (QASet itself)
    # The schema for the prompt is still obtained from PydanticOutputParser(pydantic_object=qa_response_model)
    temp_parser_for_schema = PydanticOutputParser(pydantic_object=qa_response_model)
    schema_instructions = (
        temp_parser_for_schema.get_format_instructions()
        .replace("{", "{{")
        .replace("}", "}}")
    )

    sys_msg_for_prompt = (
        "You are an aerospace-domain assistant. Prefer PDF snippets for facts; "
        "use Capella XML only as supplementary context and do NOT leak XML.\n\n"
        "Generate TEN Q-A pairs matching schema below, citing at least one [Sxxxxx] token per answer.\n\n"
        "Categories:\n" + cat_desc + "\n\nSchema:\n" + schema_instructions
    )

    qa_prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", sys_msg_for_prompt),
            (
                "human",
                "## Documents\n"
                + "\n\n".join(pdf_blocks)
                + "\n\n## Capella\n"
                + "\n\n".join(capella_blocks)
                + "\n\n## Question\n"
                + user_query,
            ),
        ]
    )

    prompt_messages_lc_qa = qa_prompt_template.format_prompt().to_messages()
    messages_qa = []
    for msg in prompt_messages_lc_qa:
        role = msg.type
        if role == "human":
            role = "user"
        elif role == "ai":
            role = "assistant"
        messages_qa.append({"role": role, "content": msg.content})

    print(
        f"[generate_qa_set] Assembled QA prompt, calling litellm with model {qa_model_name}"
    )
    qa_set_response = litellm.completion(
        model="openai/" + qa_model_name,
        messages=messages_qa,
        api_key=qa_api_key,
        base_url=qa_api_base,
        response_model=qa_response_model,
    )
    print("[generate_qa_set] QA set generation complete")

    return qa_set_response.dict() if qa_set_response else {}, src_map
