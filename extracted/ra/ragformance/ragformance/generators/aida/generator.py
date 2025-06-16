import json
from pathlib import Path
from typing import List, Tuple, Dict

from ragformance.generators.data_generator_interface import (
    RAGformanceGeneratorInterface,
)
from ragformance.generators.aida.config import AidaGeneratorConfig
from ragformance.models.corpus import DocModel
from ragformance.models.answer import AnnotatedQueryModel


# TODO assess if we need langchain, if yes put it in optionnal
from langchain_community.document_loaders import PyPDFium2Loader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


from .capella_pdf_qa_generator import (
    build_network,
    build_name_index,
    setup_entity_extractor,
    setup_qa_llm,
    generate_qa_set,
)


class AidaGenerator(RAGformanceGeneratorInterface):
    def run(self, config: Dict) -> Tuple[List[DocModel], List[AnnotatedQueryModel]]:
        """
        Generates corpus and queries using the AIDA Capella PDF QA generation method.

        Args:
            config: A dictionary containing configuration parameters:
                - seed_questions_path (str): Path to seed questions JSON file.
                - data_dir (str): Directory containing PDF files.
                - output_dir (str): Directory for output files.
                - llm_api_key (str): API key for the LLM (e.g., OpenRouter).
                - llm_base_url (str): Base URL for the LLM API.
                - hf_embed_model (str): HuggingFace embedding model ID.
                - capella_xml_path (str): Path to the Capella XML file.
                - entity_model_name (str): LLM model for entity extraction.
                - qa_model_name (str): LLM model for QA pair generation.
                - chunk_size (int, optional): Max chars per text chunk. Defaults to 750.
                - chunk_overlap (int, optional): Overlap between chunks. Defaults to 100.
                - persist_dir (str, optional): Directory for Chroma index. Defaults to "chroma_index".
                - k_pdf (int, optional): Top PDF chunks to retrieve. Defaults to 5.
                - k_capella (int, optional): Top Capella snippets. Defaults to 8.
        """
        config_model = AidaGeneratorConfig(**config)

        seed_questions_path = Path(config_model.seed_questions_path)
        data_dir = Path(config_model.data_dir)
        output_dir = Path(config_model.output_dir)
        openrouter_key = config_model.llm_api_key
        openrouter_base_url = config_model.llm_base_url
        hf_embed_model_name = config_model.hf_embed_model
        capella_path = Path(config_model.capella_xml_path)
        entity_model_name = config_model.entity_model_name
        qa_model_name = config_model.qa_model_name

        chunk_size = config_model.chunk_size
        chunk_overlap = config_model.chunk_overlap
        persist_dir = Path(config_model.persist_dir)
        k_pdf = config_model.k_pdf
        k_capella = config_model.k_capella

        # --- This is the adapted logic from the original run function ---
        print("[AidaGenerator.run] Starting AIDA BEIR-style pipeline run")

        output_dir.mkdir(parents=True, exist_ok=True)

        # 1) Build Capella graph
        G = build_network(capella_path)

        # 2) Name index & choices
        name_index = build_name_index(G)
        choices = {nid: attrs["name"] for nid, attrs in G.nodes(data=True)}

        # 3) Load & chunk PDFs
        pages = []
        for pdf_file_path in sorted(data_dir.glob("*.pdf")):
            loaded = PyPDFium2Loader(str(pdf_file_path)).load()
            for p in loaded:
                p.metadata["source"] = Path(pdf_file_path).name
            pages.extend(loaded)
            print(
                f"[AidaGenerator.run]   Loaded {len(loaded)} pages from {pdf_file_path.name}"
            )

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        raw_chunks = splitter.split_documents(pages)

        corpus_docs_intermediate = []
        for idx, chunk_doc in enumerate(raw_chunks):
            meta = dict(chunk_doc.metadata)
            corpus_id = f"doc{idx}"
            meta["corpus_id"] = corpus_id
            meta["title"] = meta.get("source", "")
            corpus_docs_intermediate.append(
                type(chunk_doc)(page_content=chunk_doc.page_content, metadata=meta)
            )

        print(
            f"[AidaGenerator.run]   Split into {len(corpus_docs_intermediate)} chunks"
        )

        # 4) Build & persist Chroma index
        emb_model_service = HuggingFaceEmbeddings(
            model_name=hf_embed_model_name
        )  # Changed variable name
        vectordb = Chroma.from_documents(
            corpus_docs_intermediate,
            embedding=emb_model_service,
            persist_directory=str(persist_dir),
        )
        vectordb.persist()
        print(f"[AidaGenerator.run]   Chroma index persisted at {persist_dir}")

        # 5) Setup LLMs & parsers
        (
            extract_prompt_template,
            extract_response_model,
            entity_model_name_out,
            entity_api_key_out,
            entity_api_base_out,
        ) = setup_entity_extractor(
            entity_model_name, openrouter_key, openrouter_base_url
        )
        # setup_qa_llm returns: response_model (QASet), model_name, api_key, api_base
        (
            qa_response_pydantic_model,
            qa_model_name_out,
            qa_api_key_out,
            qa_api_base_out,
        ) = setup_qa_llm(qa_model_name, openrouter_key, openrouter_base_url)

        final_corpus: List[DocModel] = []
        for chunk_doc_obj in corpus_docs_intermediate:
            final_corpus.append(
                DocModel(
                    _id=chunk_doc_obj.metadata["corpus_id"],
                    text=chunk_doc_obj.page_content,
                    title=chunk_doc_obj.metadata["title"],
                )
            )

        corpus_jsonl_path = output_dir / "corpus.jsonl"
        with corpus_jsonl_path.open("w", encoding="utf-8") as cf:
            for doc_model_instance in final_corpus:
                cf.write(doc_model_instance.model_dump_json() + "\n")
        print(f"[AidaGenerator.run] Wrote corpus to {corpus_jsonl_path}")

        with seed_questions_path.open("r", encoding="utf-8") as f:
            seeds = json.load(f)

        final_queries: List[AnnotatedQueryModel] = []
        queries_jsonl_path = output_dir / "queries.jsonl"

        with queries_jsonl_path.open("w", encoding="utf-8") as qf:
            for qi, seed_query_text in enumerate(seeds):
                qa_set_as_dict, src_map = (
                    generate_qa_set(  # generate_qa_set returns a dict and src_map
                        user_query=seed_query_text,
                        G=G,
                        vectordb=vectordb,
                        embed_model=hf_embed_model_name,  # Pass the model name string
                        extract_prompt_template=extract_prompt_template,
                        extract_response_model=extract_response_model,  # This is EntityList
                        entity_model_name=entity_model_name_out,
                        entity_api_key=entity_api_key_out,
                        entity_api_base=entity_api_base_out,
                        qa_response_model=qa_response_pydantic_model,  # This is QASet
                        qa_model_name=qa_model_name_out,
                        qa_api_key=qa_api_key_out,
                        qa_api_base=qa_api_base_out,
                        name_index=name_index,
                        choices=choices,
                        k_pdf=k_pdf,
                        k_capella=k_capella,
                    )
                )
                if qa_set_as_dict:  # This is already a dictionary
                    for category, qa_item_model_fields in qa_set_as_dict.items():
                        query_id = f"q{qi}_{category}"

                        # The 'sources' from qa_item_model_fields are [Sxxxxx] tags.
                        # These need to be resolved to corpus document IDs for 'relevant_document_ids'.
                        # This is a complex step. For now, storing original sources in metadata.
                        # Placeholder for resolved relevant_document_ids
                        relevant_docs_list = []

                        # Attempt to resolve sources if src_map is available and sources are present
                        original_sources = qa_item_model_fields.get("sources", [])
                        resolved_sources_info = []
                        if src_map and original_sources:
                            for src_tag_raw in original_sources:
                                # src_tag_raw could be like "[S123456]" or just "S123456"
                                # Assuming src_map keys are "S123456" (without brackets)
                                src_tag_cleaned = src_tag_raw.strip("[]")
                                if src_tag_cleaned in src_map:
                                    mapped_info = src_map[src_tag_cleaned]
                                    resolved_sources_info.append(mapped_info)
                                    # If mapped_info['kind'] == 'pdf', its 'snippet' is page content
                                    # and it should have a 'corpus_id' if we added it during chunking.
                                    # This part requires that `src_map` items for PDFs get a `corpus_id`.
                                    # The current `generate_qa_set` `src_map` for PDFs is:
                                    # src_map[sid] = {"kind":"pdf","page":ch.metadata.get("page","?"),"snippet":ch.page_content}
                                    # It's missing corpus_id. This needs to be added when pdf_blocks are created in generate_qa_set
                                    # For now, this resolution will be partial.
                                    if (
                                        mapped_info.get("kind") == "pdf_chunk_id"
                                    ):  # Assuming we can add 'pdf_chunk_id' to src_map
                                        relevant_docs_list.append(
                                            {
                                                "corpus_id": mapped_info[
                                                    "pdf_chunk_id"
                                                ],
                                                "score": 1,
                                            }
                                        )

                        aqm = AnnotatedQueryModel(
                            _id=query_id,
                            query_text=qa_item_model_fields["question"],
                            relevant_document_ids=relevant_docs_list,
                            ref_answer=qa_item_model_fields["answer"],
                            metadata={
                                "seed_index": qi,
                                "category": category,
                                "original_sources": original_sources,
                                "resolved_sources_info": resolved_sources_info,  # Store more detailed info
                            },
                        )
                        final_queries.append(aqm)
                        qf.write(aqm.model_dump_json() + "\n")

            print("[AidaGenerator.run] AIDA generator pipeline complete.")
            return final_corpus, final_queries
