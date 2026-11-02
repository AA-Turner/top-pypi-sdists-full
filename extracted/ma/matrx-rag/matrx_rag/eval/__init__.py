"""RAG evaluation harness.

Provides a tiny, reproducible test rig for the retrieval pipeline so we
can answer questions like:

  * Did contextual retrieval actually help on our corpus?
  * Is multi-query worth the latency?
  * Which embedding model gives best recall@10?
  * After we change the chunker, did anything regress?

Usage::

    uv run python -m aidream.services.rag.eval.runner \
        --golden aidream/services/rag/eval/golden_starter.json \
        --user-id <uuid> \
        --report-out /tmp/rag_eval.json

A "golden item" is a JSON object::

    {
      "query": "find the retry helper",
      "expected_source_ids": ["<code_files.id>"],         # any-match
      "expected_chunk_ids":  [],                          # optional, exact-match
      "source_kinds":        ["code_file"],               # restrict scope
      "answer":              "...optional draft answer...",
                                                          # if present, faithfulness ran
      "tags":                ["code", "python"]
    }

A "golden set" is a JSON document with::

    {
      "name": "starter_v1",
      "items": [ <golden_item>, ... ]
    }

The runner outputs::

    {
      "name": ...,
      "ran_at": ...,
      "config":  { embedding_models, multi_query, use_hyde, use_mmr, rerank },
      "items":   [ {item, retrieved_chunk_ids, retrieved_source_ids, hits@k, mrr, faithfulness?}, ... ],
      "summary": { recall@1/3/5/10, mrr, mean_faithfulness, n_items, n_with_answer }
    }
"""
