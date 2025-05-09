# pylint: disable=ungrouped-imports

import json
import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Union, Literal
from tenacity import retry, retry_if_exception_type, wait_exponential, stop_after_attempt

import numpy as np
import requests
from tqdm import tqdm

from haystack.environment import (
    HAYSTACK_REMOTE_API_BACKOFF_SEC,
    HAYSTACK_REMOTE_API_MAX_RETRIES,
    HAYSTACK_REMOTE_API_TIMEOUT_SEC,
)
from haystack.errors import AWSConfigurationError, CohereError, CohereUnauthorizedError
from haystack.nodes.retriever._openai_encoder import _OpenAIEmbeddingEncoder
from haystack.schema import Document
from haystack.telemetry import send_event
from haystack.lazy_imports import LazyImport

from ._base_embedding_encoder import _BaseEmbeddingEncoder

if TYPE_CHECKING:
    from haystack.nodes.retriever import EmbeddingRetriever


logger = logging.getLogger(__name__)


with LazyImport(message="Run 'pip install farm-haystack[inference]'") as torch_and_transformers_import:
    import torch
    from sentence_transformers import InputExample, SentenceTransformer
    from torch.utils.data import DataLoader
    from torch.utils.data.sampler import SequentialSampler
    from transformers import AutoModel, AutoTokenizer
    from haystack.modeling.data_handler.dataloader import NamedDataLoader
    from haystack.modeling.data_handler.dataset import convert_features_to_dataset, flatten_rename
    from haystack.modeling.infer import Inferencer
    from haystack.nodes.retriever._losses import _TRAINING_LOSSES

with LazyImport(message="Run 'pip install boto3'") as boto3_import:
    import boto3
    from botocore.exceptions import BotoCoreError

COHERE_TIMEOUT = float(os.environ.get(HAYSTACK_REMOTE_API_TIMEOUT_SEC, 30))
COHERE_BACKOFF = int(os.environ.get(HAYSTACK_REMOTE_API_BACKOFF_SEC, 10))
COHERE_MAX_RETRIES = int(os.environ.get(HAYSTACK_REMOTE_API_MAX_RETRIES, 5))
COHERE_EMBEDDING_MODELS = [
    "small",
    "large",
    "multilingual-22-12",
    "embed-english-v2.0",
    "embed-english-light-v2.0",
    "embed-multilingual-v2.0",
]

BEDROCK_EMBEDDING_MODELS = ["amazon.titan-embed-text-v1", "cohere.embed-english-v3", "cohere.embed-multilingual-v3"]


class _DefaultEmbeddingEncoder(_BaseEmbeddingEncoder):
    def __init__(self, retriever: "EmbeddingRetriever"):
        self.embedding_model = Inferencer.load(
            retriever.embedding_model,
            revision=retriever.model_version,
            task_type="embeddings",
            extraction_strategy=retriever.pooling_strategy,
            extraction_layer=retriever.emb_extraction_layer,
            gpu=retriever.use_gpu,
            batch_size=retriever.batch_size,
            max_seq_len=retriever.max_seq_len,
            num_processes=0,
            use_auth_token=retriever.use_auth_token,
        )
        torch_and_transformers_import.check()
        if retriever.document_store:
            self._check_docstore_similarity_function(
                document_store=retriever.document_store, model_name=retriever.embedding_model
            )

    def embed(self, texts: Union[List[List[str]], List[str], str]) -> np.ndarray:
        # TODO: FARM's `sample_to_features_text` need to fix following warning -
        # tokenization_utils.py:460: FutureWarning: `is_pretokenized` is deprecated and will be removed in a future version, use `is_split_into_words` instead.
        emb = self.embedding_model.inference_from_dicts(dicts=[{"text": t} for t in texts])
        emb = np.stack([r["vec"] for r in emb])
        return emb

    def embed_queries(self, queries: List[str]) -> np.ndarray:
        """
        Create embeddings for a list of queries.

        :param queries: List of queries to embed.
        :return: Embeddings, one per input query, shape: (queries, embedding_dim)
        """
        return self.embed(queries)

    def embed_documents(self, docs: List[Document]) -> np.ndarray:
        """
        Create embeddings for a list of documents.

        :param docs: List of documents to embed.
        :return: Embeddings, one per input document, shape: (documents, embedding_dim)
        """
        passages = [d.content for d in docs]
        return self.embed(passages)

    def train(
        self,
        training_data: List[Dict[str, Any]],
        learning_rate: float = 2e-5,
        n_epochs: int = 1,
        num_warmup_steps: Optional[int] = None,
        batch_size: int = 16,
        train_loss: Literal["mnrl", "margin_mse"] = "mnrl",
        num_workers: int = 0,
        use_amp: bool = False,
        **kwargs,
    ):
        raise NotImplementedError(
            "You can't train this retriever. You can only use the `train` method with sentence-transformers EmbeddingRetrievers."
        )

    def save(self, save_dir: Union[Path, str]):
        raise NotImplementedError(
            "You can't save your record as `save` only works for sentence-transformers EmbeddingRetrievers."
        )


class _SentenceTransformersEmbeddingEncoder(_BaseEmbeddingEncoder):
    def __init__(self, retriever: "EmbeddingRetriever"):
        # pretrained embedding models coming from: https://github.com/UKPLab/sentence-transformers#pretrained-models
        # e.g. 'roberta-base-nli-stsb-mean-tokens'
        torch_and_transformers_import.check()
        self.embedding_model = SentenceTransformer(
            retriever.embedding_model,
            device=str(retriever.devices[0]),
            use_auth_token=retriever.use_auth_token,
            revision=retriever.model_version,
        )
        self.batch_size = retriever.batch_size
        self.embedding_model.max_seq_length = retriever.max_seq_len
        self.show_progress_bar = retriever.progress_bar
        if retriever.document_store:
            self._check_docstore_similarity_function(
                document_store=retriever.document_store, model_name=retriever.embedding_model
            )

    def embed(self, texts: Union[List[str], str]) -> np.ndarray:
        # texts can be a list of strings
        # get back list of numpy embedding vectors
        emb = self.embedding_model.encode(
            texts, batch_size=self.batch_size, show_progress_bar=self.show_progress_bar, convert_to_numpy=True
        )
        return emb

    def embed_queries(self, queries: List[str]) -> np.ndarray:
        """
        Create embeddings for a list of queries.

        :param queries: List of queries to embed.
        :return: Embeddings, one per input query, shape: (queries, embedding_dim)
        """
        return self.embed(queries)

    def embed_documents(self, docs: List[Document]) -> np.ndarray:
        """
        Create embeddings for a list of documents.

        :param docs: List of documents to embed.
        :return: Embeddings, one per input document, shape: (documents, embedding_dim)
        """
        passages = [d.content for d in docs]
        return self.embed(passages)

    def train(
        self,
        training_data: List[Dict[str, Any]],
        learning_rate: float = 2e-5,
        n_epochs: int = 1,
        num_warmup_steps: Optional[int] = None,
        batch_size: Optional[int] = 16,
        train_loss: Literal["mnrl", "margin_mse"] = "mnrl",
        num_workers: int = 0,
        use_amp: bool = False,
        **kwargs,
    ):
        """
        Trains the underlying Sentence Transformer model.

        Each training data example is a dictionary with the following keys:

        * question: The question string.
        * pos_doc: Positive document string (the document containing the answer).
        * neg_doc: Negative document string (the document that doesn't contain the answer).
        * score: The score margin the answer must fall within.

        :param training_data: The training data in a dictionary format.
        :param learning_rate: The learning rate of the optimizer.
        :param n_epochs: The number of iterations on the whole training data set you want to train for.
        :param num_warmup_steps: Behavior depends on the scheduler. For WarmupLinear (default), the learning rate is
            increased from 0 up to the maximal learning rate. After these many training steps, the learning rate is
            decreased linearly back to zero.
        :param batch_size: The batch size to use for the training. The default value is 16.
        :param train_loss: Specify the training loss to use to fit the Sentence-Transformers model. Possible options are
            "mnrl" (Multiple Negatives Ranking Loss) and "margin_mse".
        :param num_workers: The number of subprocesses to use for the Pytorch DataLoader.
        :param use_amp: Use Automatic Mixed Precision (AMP).
        :param kwargs: Additional training keyword arguments to pass to the `SentenceTransformer.fit` function. Please
            reference the Sentence-Transformers [documentation](https://www.sbert.net/docs/training/overview.html#sentence_transformers.SentenceTransformer.fit)
            for a full list of keyword arguments.
        """
        send_event(event_name="Training", event_properties={"class": self.__class__.__name__, "function_name": "train"})

        if train_loss not in _TRAINING_LOSSES:
            raise ValueError(f"Unrecognized train_loss {train_loss}. Should be one of: {_TRAINING_LOSSES.keys()}")

        st_loss = _TRAINING_LOSSES[train_loss]

        train_examples = []
        for train_i in training_data:
            missing_attrs = st_loss.required_attrs.difference(set(train_i.keys()))
            if len(missing_attrs) > 0:
                raise ValueError(
                    f"Some training examples don't contain the fields {missing_attrs} which are necessary when using the '{train_loss}' loss."
                )

            texts = [train_i["question"], train_i["pos_doc"]]
            if "neg_doc" in train_i:
                texts.append(train_i["neg_doc"])

            if "score" in train_i:
                train_examples.append(InputExample(texts=texts, label=train_i["score"]))
            else:
                train_examples.append(InputExample(texts=texts))

        logger.info("Training/adapting %s with %s examples", self.embedding_model, len(train_examples))
        train_dataloader = DataLoader(
            train_examples,  # type: ignore [var-annotated, arg-type]
            batch_size=batch_size,
            drop_last=True,
            shuffle=True,
            num_workers=num_workers,
        )
        train_loss = st_loss.loss(self.embedding_model)

        # Tune the model
        self.embedding_model.fit(
            train_objectives=[(train_dataloader, train_loss)],
            epochs=n_epochs,
            optimizer_params={"lr": learning_rate},
            warmup_steps=int(len(train_dataloader) * 0.1) if num_warmup_steps is None else num_warmup_steps,
            use_amp=use_amp,
            **kwargs,
        )

    def save(self, save_dir: Union[Path, str]):
        self.embedding_model.save(path=str(save_dir))


class _RetribertEmbeddingEncoder(_BaseEmbeddingEncoder):
    def __init__(self, retriever: "EmbeddingRetriever"):
        torch_and_transformers_import.check()

        self.progress_bar = retriever.progress_bar
        self.batch_size = retriever.batch_size
        self.max_length = retriever.max_seq_len
        self.embedding_tokenizer = AutoTokenizer.from_pretrained(
            retriever.embedding_model, use_auth_token=retriever.use_auth_token
        )
        self.embedding_model = AutoModel.from_pretrained(
            retriever.embedding_model, use_auth_token=retriever.use_auth_token
        ).to(str(retriever.devices[0]))

    def embed_queries(self, queries: List[str]) -> np.ndarray:
        """
        Create embeddings for a list of queries.

        :param queries: List of queries to embed.
        :return: Embeddings, one per input query, shape: (queries, embedding_dim)
        """
        query_text = [{"text": q} for q in queries]
        dataloader = self._create_dataloader(query_text)

        embeddings: List[np.ndarray] = []
        disable_tqdm = True if len(dataloader) == 1 else not self.progress_bar

        for batch in tqdm(dataloader, desc="Creating Embeddings", unit=" Batches", disable=disable_tqdm):
            batch = {key: batch[key].to(self.embedding_model.device) for key in batch}
            with torch.inference_mode():
                q_reps = (
                    self.embedding_model.embed_questions(
                        input_ids=batch["input_ids"], attention_mask=batch["padding_mask"]
                    )
                    .cpu()
                    .numpy()
                )
            embeddings.append(q_reps)

        return np.concatenate(embeddings)

    def embed_documents(self, docs: List[Document]) -> np.ndarray:
        """
        Create embeddings for a list of documents.

        :param docs: List of documents to embed.
        :return: Embeddings, one per input document, shape: (documents, embedding_dim)
        """
        doc_text = [{"text": d.content} for d in docs]
        dataloader = self._create_dataloader(doc_text)

        embeddings: List[np.ndarray] = []
        disable_tqdm = True if len(dataloader) == 1 else not self.progress_bar

        for batch in tqdm(dataloader, desc="Creating Embeddings", unit=" Batches", disable=disable_tqdm):
            batch = {key: batch[key].to(self.embedding_model.device) for key in batch}
            with torch.inference_mode():
                q_reps = (
                    self.embedding_model.embed_answers(
                        input_ids=batch["input_ids"], attention_mask=batch["padding_mask"]
                    )
                    .cpu()
                    .numpy()
                )
            embeddings.append(q_reps)

        return np.concatenate(embeddings)

    def _create_dataloader(self, text_to_encode: List[dict]) -> "NamedDataLoader":
        dataset, tensor_names = self.dataset_from_dicts(text_to_encode)
        dataloader = NamedDataLoader(
            dataset=dataset, sampler=SequentialSampler(dataset), batch_size=self.batch_size, tensor_names=tensor_names
        )
        return dataloader

    def dataset_from_dicts(self, dicts: List[dict]):
        texts = [x["text"] for x in dicts]
        tokenized_batch = self.embedding_tokenizer(
            texts,
            return_token_type_ids=True,
            return_attention_mask=True,
            max_length=self.max_length,
            truncation=True,
            padding=True,
        )

        features_flat = flatten_rename(
            tokenized_batch,
            ["input_ids", "token_type_ids", "attention_mask"],
            ["input_ids", "segment_ids", "padding_mask"],
        )
        dataset, tensornames = convert_features_to_dataset(features=features_flat)
        return dataset, tensornames

    def train(
        self,
        training_data: List[Dict[str, Any]],
        learning_rate: float = 2e-5,
        n_epochs: int = 1,
        num_warmup_steps: Optional[int] = None,
        batch_size: int = 16,
        train_loss: Literal["mnrl", "margin_mse"] = "mnrl",
        num_workers: int = 0,
        use_amp: bool = False,
        **kwargs,
    ):
        raise NotImplementedError(
            "You can't train this retriever. You can only use the `train` method with sentence-transformers EmbeddingRetrievers."
        )

    def save(self, save_dir: Union[Path, str]):
        raise NotImplementedError(
            "You can't save your record as `save` only works for sentence-transformers EmbeddingRetrievers."
        )


class _CohereEmbeddingEncoder(_BaseEmbeddingEncoder):
    def __init__(self, retriever: "EmbeddingRetriever"):
        torch_and_transformers_import.check()

        # See https://docs.cohere.com/reference/embed for more details
        # Cohere has a max seq length of 4096 tokens and a max batch size of 96
        self.max_seq_len = min(4096, retriever.max_seq_len)
        self.url = "https://api.cohere.ai/embed"
        self.api_key = retriever.api_key
        self.batch_size = min(96, retriever.batch_size)
        self.progress_bar = retriever.progress_bar
        self.model: str = next(
            (m for m in COHERE_EMBEDDING_MODELS if m in retriever.embedding_model), "multilingual-22-12"
        )

    @retry(
        retry=retry_if_exception_type(CohereError),
        wait=wait_exponential(multiplier=COHERE_BACKOFF),
        stop=stop_after_attempt(COHERE_MAX_RETRIES),
    )
    def embed(self, model: str, text: List[str]) -> np.ndarray:
        payload = {"model": model, "texts": text, "truncate": "END"}
        headers = {"Authorization": f"BEARER {self.api_key}", "Content-Type": "application/json"}
        response = requests.request("POST", self.url, headers=headers, data=json.dumps(payload), timeout=COHERE_TIMEOUT)
        res = json.loads(response.text)
        if response.status_code == 401:
            raise CohereUnauthorizedError(f"Invalid Cohere API key. {response.text}")
        if response.status_code != 200:
            raise CohereError(response.text, status_code=response.status_code)
        generated_embeddings = list(res["embeddings"])
        return np.array(generated_embeddings)

    def embed_batch(self, text: List[str]) -> np.ndarray:
        all_embeddings = []
        for i in tqdm(
            range(0, len(text), self.batch_size), disable=not self.progress_bar, desc="Calculating embeddings"
        ):
            batch = text[i : i + self.batch_size]
            generated_embeddings = self.embed(self.model, batch)
            all_embeddings.append(generated_embeddings)
        return np.concatenate(all_embeddings)

    def embed_queries(self, queries: List[str]) -> np.ndarray:
        return self.embed_batch(queries)

    def embed_documents(self, docs: List[Document]) -> np.ndarray:
        return self.embed_batch([d.content for d in docs])

    def train(
        self,
        training_data: List[Dict[str, Any]],
        learning_rate: float = 2e-5,
        n_epochs: int = 1,
        num_warmup_steps: Optional[int] = None,
        batch_size: int = 16,
        train_loss: Literal["mnrl", "margin_mse"] = "mnrl",
        num_workers: int = 0,
        use_amp: bool = False,
        **kwargs,
    ):
        raise NotImplementedError(f"Training is not implemented for {self.__class__}")

    def save(self, save_dir: Union[Path, str]):
        raise NotImplementedError(f"Saving is not implemented for {self.__class__}")


class _BedrockEmbeddingEncoder(_BaseEmbeddingEncoder):
    def __init__(self, retriever: "EmbeddingRetriever"):
        """Embedding Encoder for Bedrock models
        See https://docs.aws.amazon.com/bedrock/latest/userguide/embeddings.html for more details.
        The maximum input text is 8K tokens and the maximum output vector length is 1536.
        Titan embeddings do not support batch operations.

        :param retriever: EmbeddingRetriever object
        """
        boto3_import.check()
        if retriever.embedding_model not in BEDROCK_EMBEDDING_MODELS:
            raise ValueError("Model not supported by Bedrock Embedding Encoder")
        self.model = retriever.embedding_model
        self.client = self._initialize_boto3_session(retriever.aws_config).client("bedrock-runtime")

    def _initialize_boto3_session(self, aws_config: Optional[Dict[str, Any]]):
        if aws_config is None:
            raise ValueError(
                "`aws_config` is not set. To use Bedrock models, you should set `aws_config` when initializing the retriever."
            )

        aws_access_key_id = aws_config.get("aws_access_key_id", None)
        aws_secret_access_key = aws_config.get("aws_secret_access_key", None)
        aws_session_token = aws_config.get("aws_session_token", None)
        region_name = aws_config.get("region_name", None)
        profile_name = aws_config.get("profile_name", None)
        try:
            return boto3.Session(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                aws_session_token=aws_session_token,
                region_name=region_name,
                profile_name=profile_name,
            )
        except BotoCoreError as e:
            raise AWSConfigurationError(
                f"Failed to initialize the session with provided AWS credentials {aws_config}"
            ) from e

    def _embed_batch_cohere(
        self, texts: List[str], input_type: Literal["search_query", "search_document"]
    ) -> np.ndarray:
        cohere_payload = {"texts": texts, "input_type": input_type, "truncate": "RIGHT"}
        response = self._invoke_model(cohere_payload)
        embeddings = np.array(response["embeddings"])
        return embeddings

    def _embed_titan(self, text: str) -> np.ndarray:
        titan_payload = {"inputText": text}
        response = self._invoke_model(titan_payload)
        embeddings = np.array(response["embedding"])
        return embeddings

    def _invoke_model(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        body = json.dumps(payload)
        response = self.client.invoke_model(
            body=body, modelId=self.model, accept="application/json", contentType="application/json"
        )
        body = response.get("body").read().decode("utf-8")
        response_body = json.loads(body)
        return response_body

    def embed_queries(self, queries: List[str]) -> np.ndarray:
        if self.model == "amazon.titan-embed-text-v1":
            all_embeddings = []
            for query in queries:
                generated_embeddings = self._embed_titan(query)
                all_embeddings.append(generated_embeddings)
            return np.stack(all_embeddings)
        else:
            return self._embed_batch_cohere(queries, input_type="search_query")

    def embed_documents(self, docs: List[Document]) -> np.ndarray:
        if self.model == "amazon.titan-embed-text-v1":
            all_embeddings = []
            for doc in docs:
                generated_embeddings = self._embed_titan(doc.content)
                all_embeddings.append(generated_embeddings)
            return np.stack(all_embeddings)
        else:
            contents = [d.content for d in docs]
            return self._embed_batch_cohere(contents, input_type="search_document")

    def train(
        self,
        training_data: List[Dict[str, Any]],
        learning_rate: float = 2e-5,
        n_epochs: int = 1,
        num_warmup_steps: Optional[int] = None,
        batch_size: int = 16,
        train_loss: Literal["mnrl", "margin_mse"] = "mnrl",
        num_workers: int = 0,
        use_amp: bool = False,
        **kwargs,
    ):
        raise NotImplementedError(f"Training is not implemented for {self.__class__}")

    def save(self, save_dir: Union[Path, str]):
        raise NotImplementedError(f"Saving is not implemented for {self.__class__}")


_EMBEDDING_ENCODERS: Dict[str, Callable] = {
    "farm": _DefaultEmbeddingEncoder,
    "transformers": _DefaultEmbeddingEncoder,
    "sentence_transformers": _SentenceTransformersEmbeddingEncoder,
    "retribert": _RetribertEmbeddingEncoder,
    "openai": _OpenAIEmbeddingEncoder,
    "cohere": _CohereEmbeddingEncoder,
    "bedrock": _BedrockEmbeddingEncoder,
}
