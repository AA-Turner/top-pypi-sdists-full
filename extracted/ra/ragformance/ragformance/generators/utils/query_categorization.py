import requests
import json

import logging
from tqdm.autonotebook import tqdm


logger = logging.getLogger(__name__)


def categorize_queries(queries, configpath="config.json"):
    new_queries = []

    with open(configpath) as f:
        config = json.load(f)

        url = config.get("LLMurl", "https://localhost:8000/v1/chat/completions")
        key = config.get("LLMkey", None)
        model = config.get("LLMmodel", None)

    question_categories = [
        "Simple (Factual/ Simple with conditions)",
        "Analytic (Comparison/ evaluation )",
        "Superlative Questions",
        "Interpretatives",
        "Set (multiple answers)",
        "Summarization",
        "False Premise",
        "Unanswerable",
        "Aggregation",
        "Multi-Hop",
        "Post-processing Heavy",
        "Information Integration",
        "Numerical Comparison",
        "Temporal Sequence",
    ]

    for q in tqdm(queries, desc="Queries categorizations"):
        query = q["text"]

        prompt_and_query = (
            "Tell me if this question belongs to one of the following category. Answer with just the categories as a comma separated list."
            + query
            + str(question_categories)
        )

        response = requests.post(
            url=url,
            headers={
                "Authorization": "Bearer " + key,
            },
            data=json.dumps(
                {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt_and_query}],
                }
            ),
        )
        response_json = response.json()["choices"][0]["message"]["content"]
        categories = response_json.split(",")
        if "metadata" not in q:
            q["metadata"] = {}
        q["metadata"]["categories"] = categories
        new_queries.append(q)

        # save classes to a csv file
        with open("query_classes.csv", "w") as f:
            f.write(f"{query},{categories}\n")
        logger.info(f"{query}, {str(categories)}")

    return new_queries
