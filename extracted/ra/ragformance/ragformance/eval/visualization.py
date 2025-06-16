import numpy as np
import plotly.graph_objects as go
from plotly.offline import plot
from typing import List, Union
from collections import defaultdict

from ragformance.models.answer import AnswerModel
from ragformance.models.corpus import DocModel
from IPython.display import HTML, display


try:
    from sentence_transformers import SentenceTransformer
except ImportError:

    def SentenceTransformer(*args, **kwargs):
        raise ImportError(
            "'sentence-transformers' module is not installed. "
            "Please install ragformance with the [all] option:\n"
            "    pip install ragformance[all]"
        )


DEFAULT_EMBEDDING_CONFIG = {
    "name": "default_openai_embedding",
    "provider": "openai",
    "model": "text-embedding-ada-002",
    "api_key_env": "OPENAI_API_KEY",
    "params": {},
}

embedding_model = None  #  TODO : connect with config system


def find_in_corpus(corpus: List[DocModel], doc_id):
    for doc in corpus:
        if doc.id == doc_id:
            return doc
    return None


def visualize_semantic_F1(
    corpus: List[DocModel],
    answers: list[AnswerModel],
    output_file="visualization.html",
    f1_threshold=0.5,
    semantic_threshold=0.5,
    embedding_config=None,  # Permet de passer une config custom
):
    def cosine_sim(a, b):
        return (a @ b) / (np.linalg.norm(a) * np.linalg.norm(b))

    grouped_data = defaultdict(list)
    model_quadrants = defaultdict(
        lambda: {
            "Difficult and missed": 0,
            "Difficult and success": 0,
            "Simple but missed": 0,
            "Simple and success": 0,
        }
    )

    embedding_model = SentenceTransformer(
        embedding_config["model"]
    )  # TODO alternative litellm

    for a in answers:
        query_id = a.query.id
        relevant_docs = {doc.corpus_id for doc in a.query.relevant_document_ids}
        retrieved_docs = set(a.retrieved_documents_ids)

        precision = (
            len(relevant_docs & retrieved_docs) / len(retrieved_docs)
            if retrieved_docs
            else 0
        )
        recall = (
            len(relevant_docs & retrieved_docs) / len(relevant_docs)
            if relevant_docs
            else 0
        )
        f1 = (
            2 * (precision * recall) / (precision + recall)
            if (precision + recall)
            else 0
        )

        query_text = a.query.query_text

        query_embedding = embedding_model.encode([query_text], show_progress_bar=False)[
            0
        ]

        document_texts = [
            find_in_corpus(corpus, doc_id).text
            for doc_id in relevant_docs
            if find_in_corpus(corpus, doc_id)
        ]
        if not document_texts:
            continue

        doc_embeddings = embedding_model.encode(document_texts, show_progress_bar=False)
        semantic_score = np.mean(
            [
                max(
                    0,
                    min(
                        1,
                        cosine_sim(np.array(query_embedding), np.array(doc_embedding)),
                    ),
                )
                for doc_embedding in doc_embeddings
            ]
        )

        model_key = f"{a.embedding_model_name} + {a.llm_model_name}"

        # Quadrant classification
        is_simple = semantic_score > semantic_threshold
        is_success = f1 > f1_threshold

        if not is_simple and not is_success:
            quadrant = "Difficult and missed"
        elif not is_simple and is_success:
            quadrant = "Difficult and success"
        elif is_simple and not is_success:
            quadrant = "Simple but missed"
        else:
            quadrant = "Simple and success"

        model_quadrants[model_key][quadrant] += 1

        grouped_data[model_key].append(
            {
                "query": query_id,
                "f1_score": f1,
                "semantic_score": semantic_score,
                "stats": f"{len(relevant_docs)} expected / {len(relevant_docs & retrieved_docs)} found <br>{len(relevant_docs - retrieved_docs)} not found / {len(retrieved_docs - relevant_docs)} found but not relevant",
                "retrieved": len(retrieved_docs),
            }
        )

    is_single_model = len(grouped_data) == 1
    display_data = (
        grouped_data
        if not is_single_model
        else {"Overall": list(grouped_data.values())[0]}
    )
    display_quadrants = (
        model_quadrants
        if not is_single_model
        else {"Overall": list(model_quadrants.values())[0]}
    )

    div_blocks = []
    for model_key, points in display_data.items():
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=[p["f1_score"] for p in points],
                y=[p["semantic_score"] for p in points],
                mode="markers",
                marker=dict(
                    size=10,
                    color=[p["retrieved"] for p in points],
                    colorscale="Viridis",
                    showscale=True,
                ),
                text=[
                    f"Query ID: {p['query']}<br>F1: {p['f1_score']:.2f}<br>Semantic: {p['semantic_score']:.2f}<br>{p['stats']}"
                    for p in points
                ],
                hoverinfo="text",
            )
        )

        fig.update_layout(
            title=f"Semantic Similarity of queries, number of documents retrieved as color – {model_key}"
            if not is_single_model
            else "Semantic Similarity of queries, number of documents retrieved as color",
            xaxis_title="F1 Score (Right is better)",
            yaxis_title="Semantic Similarity Score <br>(Axis Reversed : Difficult queries are on the top)",
            xaxis=dict(range=[0, 1]),
            yaxis=dict(range=[0, 1]),
            shapes=[
                dict(
                    type="line",
                    x0=f1_threshold,
                    x1=f1_threshold,
                    y0=0,
                    y1=1,
                    line=dict(dash="dot", color="grey"),
                ),
                dict(
                    type="line",
                    x0=0,
                    x1=1,
                    y0=semantic_threshold,
                    y1=semantic_threshold,
                    line=dict(dash="dot", color="grey"),
                ),
            ],
            height=800,
        )
        fig.update_yaxes(autorange="reversed")

        title = f"<h2>{model_key}</h2>" if not is_single_model else ""
        div_html = plot(fig, include_plotlyjs=False, output_type="div")
        div_blocks.append(f"{title}\n{div_html}")

    full_html = f"""
    <html>
    <head>
        <title>Semantic F1 Visualizations</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        {"" if is_single_model else "<h1>Semantic Similarity by Model</h1>"}
        {'<hr>'.join(div_blocks)}
    </body>
    </html>
    """

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_html)
    display(
        HTML(
            f""" <iframe sandbox='allow-scripts allow-forms' style='display:block; margin:0px;' width="1000" height="1000" frameborder='0' srcdoc='{full_html}' />"""
        )
    )

    return display_quadrants


def display_semantic_quadrants(
    quadrants: Union[dict[str, dict[str, int]], dict[str, int]],
    output_file="semantic_quadrants.html",
):
    if all(isinstance(v, int) for v in quadrants.values()):
        quadrants = {"Overall": quadrants}

    is_single_model = len(quadrants) == 1 and "Overall" in quadrants

    labels = [
        ["Difficult and missed", "Difficult and success"],
        ["Simple but missed", "Simple and success"],
    ]

    custom_colors = {
        "Difficult and missed": "#ffd6a5",
        "Difficult and success": "#caffbf",
        "Simple but missed": "#ffadad",
        "Simple and success": "#9bf6ff",
    }

    div_blocks = []

    for model_name, quad in quadrants.items():
        z = [
            [quad["Difficult and missed"], quad["Difficult and success"]],
            [quad["Simple but missed"], quad["Simple and success"]],
        ]

        shapes = []
        annotations = []
        total = sum([sum(row) for row in z])
        for i in range(2):
            for j in range(2):
                label = labels[i][j]
                count = z[i][j]
                percent = count / total * 100 if total > 0 else 0
                x0, x1 = j, j + 1
                y0, y1 = 1 - i, 2 - i
                shapes.append(
                    dict(
                        type="rect",
                        x0=x0,
                        x1=x1,
                        y0=y0,
                        y1=y1,
                        fillcolor=custom_colors[label],
                        line=dict(width=2),
                    )
                )
                annotations.append(
                    dict(
                        x=(x0 + x1) / 2,
                        y=(y0 + y1) / 2,
                        text=f"<b>{count} ({percent:.1f}%)</b><br>{label}",
                        showarrow=False,
                        font=dict(color="black", size=16),
                    )
                )

        fig = go.Figure()
        fig.update_layout(
            title=f"Semantic Quadrant – {model_name}" if not is_single_model else "",
            shapes=shapes,
            annotations=annotations,
            xaxis=dict(showgrid=False, zeroline=False, tickvals=[], range=[0, 2]),
            yaxis=dict(showgrid=False, zeroline=False, tickvals=[], range=[0, 2]),
            width=800,
            height=800,
        )

        fig.update_xaxes(
            showticklabels=True, showline=False, showgrid=False, zeroline=False
        )
        fig.update_yaxes(
            showticklabels=True, showline=False, showgrid=False, zeroline=False
        )

        title = f"<h2>{model_name}</h2>" if not is_single_model else ""
        div_html = plot(fig, include_plotlyjs=False, output_type="div")
        div_blocks.append(f"{title}\n{div_html}")

    full_html = f"""
    <html>
    <head>
        <title>Semantic Quadrants</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        {"" if is_single_model else "<h1>Semantic Quadrants</h1>"}
        {'<hr>'.join(div_blocks)}
    </body>
    </html>
    """

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_html)

    return HTML(f""" <iframe sandbox='allow-scripts allow-forms' style='display:block; margin:0px;' width="1000" height="1000" frameborder='0' srcdoc='{full_html}' />
    """)
