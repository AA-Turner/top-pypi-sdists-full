import asyncio
from collections.abc import Callable
from typing import List
import contextlib
import numpy as np
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    AutoModelForTokenClassification,
    BertForSequenceClassification,
    BertTokenizer,
    BertweetTokenizer,
    RobertaTokenizer,
    RobertaForSequenceClassification,
    pipeline
)
from nltk.tokenize import sent_tokenize
import torch
from ..exceptions import ComponentError
from .flow import FlowComponent


class ModelPrediction:
    """
    ModelPrediction

        Overview

        Performs sentiment analysis and emotion detection on text using Hugging Face Transformers.

        This class utilizes pre-trained models for sentiment analysis and emotion detection.
        It supports different model architectures like BERT, BERTweet, and RoBERTa.
        The class handles text chunking for inputs exceeding the maximum token length
        and provides detailed sentiment and emotion scores along with predicted labels.

    Attributes:
        sentiment_model (str): Name of the sentiment analysis model to use from Hugging Face.
        Defaults to 'tabularisai/robust-sentiment-analysis'.
        emotions_model (str): Name of the emotion detection model to use from Hugging Face.
        Defaults to 'bhadresh-savani/distilbert-base-uncased-emotion'.
        classification (str): Type of classification pipeline to use (e.g., 'sentiment-analysis').
        Defaults to 'sentiment-analysis'.
        levels (int): Number of sentiment levels for sentiment analysis (2, 3, or 5).
        Default is 5.
        max_length (int): Maximum token length for input texts. Defaults to 512.
        use_bertweet (bool): If True, uses BERTweet model for sentiment analysis. Defaults to False.
        use_bert (bool): If True, uses BERT model for sentiment analysis. Defaults to False.
        use_roberta (bool): If True, uses RoBERTa model for sentiment analysis. Defaults to False.

    Returns:
        DataFrame: A DataFrame with sentiment and emotion analysis results.
        Includes columns for sentiment scores, sentiment labels, emotion scores, and emotion labels.

    Raises:
        ComponentError: If there is an issue during text processing or data handling.


        Example:

        ```yaml
        SentimentAnalysis:
          text_column: text
          sentiment_model: tabularisai/robust-sentiment-analysis
          sentiment_levels: 5
          emotions_model: bhadresh-savani/distilbert-base-uncased-emotion
        ```

    """  # noqa

    def __init__(
        self,
        sentiment_model: str = "tabularisai/robust-sentiment-analysis",
        emotions_model: str = "bhadresh-savani/distilbert-base-uncased-emotion",
        classification: str = 'sentiment-analysis',
        levels: int = 5,
        max_length: int = 512,
        use_bertweet: bool = False,
        use_bert: bool = False,
        use_roberta: bool = False
    ):
        """
        Initializes the ModelPrediction component.

        Sets up the sentiment analysis and emotion detection models and tokenizers
        based on the provided configurations.
        """
        print(f"[DEBUG] Creating new ModelPrediction instance with model: {sentiment_model}")
        self.max_length = max_length
        self.levels = levels
        self.use_bertweet: bool = use_bertweet
        if use_bert:
            self.model = BertForSequenceClassification.from_pretrained(
                sentiment_model,
                num_labels=abs(levels),
                ignore_mismatched_sizes=True
            )
            self.tokenizer = BertTokenizer.from_pretrained(sentiment_model)
        elif use_roberta:
            self.model = RobertaForSequenceClassification.from_pretrained(sentiment_model)
            self.tokenizer = RobertaTokenizer.from_pretrained(sentiment_model)
        elif use_bertweet:
            self.model = AutoModelForSequenceClassification.from_pretrained(sentiment_model)
            self.tokenizer = BertweetTokenizer.from_pretrained(sentiment_model)
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(
                sentiment_model,
                truncation=True,
                max_length=self.max_length
                # normalization=True
            )
            self.model = AutoModelForSequenceClassification.from_pretrained(
                sentiment_model,
            )
        # And the Emotional Model:
        self.emotional_model = AutoModelForSequenceClassification.from_pretrained(
            emotions_model
        )
        self.emo_tokenizer = AutoTokenizer.from_pretrained(
            emotions_model,
            truncation=True,
            max_length=self.max_length
        )
        self._device = self._get_device()
        self.emotion_classifier = pipeline(
            classification,
            model=self.emotional_model,
            tokenizer=self.emo_tokenizer,
            device=self._device,
            top_k=None,
            # ensure the pipeline is forcibly truncating on re-tokenize
            truncation=True,
            max_length=512
        )
        # sentiment classifier:
        self.sentiment_classifier = pipeline(
            classification,
            model=self.model,
            tokenizer=self.tokenizer,
            device=self._device,
            top_k=None,
            # ensure the pipeline is forcibly truncating on re-tokenize
            truncation=True,
            max_length=512
        )

    def _get_device(self, use_device: str = 'cpu', cuda_number: int = 0):
        """
        Determines and returns the appropriate device (CPU, CUDA, MPS) for model execution.

        Utilizes CUDA if available, then MPS, and defaults to CPU if neither is accessible or if specified.

        Args:
            use_device (str):  Desired device to use ('cpu', 'cuda'). Defaults to 'cpu'.
            cuda_number (int): CUDA device number to use, if CUDA is selected. Defaults to 0.

        Returns:
            torch.device: The device object representing the chosen execution environment.
        """
        torch.backends.cudnn.deterministic = True
        if torch.cuda.is_available():
            # Use CUDA GPU if available
            device = torch.device(f'cuda:{cuda_number}')
        elif torch.backends.mps.is_available():
            # Use CUDA Multi-Processing Service if available
            device = torch.device("mps")
        elif use_device == 'cuda':
            device = torch.device(f'cuda:{cuda_number}')
        else:
            device = torch.device(use_device)
        return device

    def predict_emotion(self, text: str) -> dict:
        """
        Predicts the emotion of the input text.

        Handles text chunking for long texts to ensure they fit within the model's
        token limit. Returns a dictionary containing emotion predictions.

        Args:
            text (str): The input text to predict emotion for.

        Returns:
            dict: A dictionary containing emotion predictions.
            For example: {'emotions': [{'label': 'joy', 'score': 0.99}]}
            Returns an empty dictionary if the input text is empty.
        """
        if not text:
            return {}

        # Tokenize the text to check its length
        encoded_text = self.emo_tokenizer.encode(
            str(text),
            truncation=False,
            add_special_tokens=True
        )

        # Handle long texts by splitting them into chunks if needed
        if len(encoded_text) > self.max_length:
            text_chunks = self._split_text(text, self.max_length)
            return self._predict_multiple_emotion_chunks(text_chunks)

        # Use the pipeline to predict emotion for shorter texts
        prediction = self.emotion_classifier(str(text))

        if len(prediction) > 0 and isinstance(prediction[0], list):  # When top_k=None
            emotions = [emo_pred for emo_pred in prediction[0] if emo_pred['score'] >= 0.5]  # Apply threshold
            if not emotions:
                emotions.append({"label": "neutral", "score": 0})
            return {'emotions': emotions}

        return {}

    def _predict_multiple_emotion_chunks(self, chunks: list) -> dict:
        """
        Predicts emotions for multiple text chunks and aggregates the results.

        Used for processing long texts that have been split into smaller chunks.
        Aggregates emotion predictions from each chunk.

        Args:
            chunks (list): List of text chunks (strings) to predict emotions for.

        Returns:
            dict: A dictionary containing aggregated emotion predictions.
            For example: {'emotions': [{'label': 'joy', 'score': 0.99}, {'label': 'surprise', 'score': 0.6}]}
            Returns emotions with scores above a threshold (e.g., 0.5). If no emotion meets the threshold,
            it returns neutral emotion with a score of 0.
        """
        all_emotions = []

        for chunk in chunks:
            predictions = self.emotion_classifier(chunk)
            if len(predictions) > 0 and isinstance(predictions[0], list):
                # Filter predictions for significant emotions
                emotions = [emo_pred for emo_pred in predictions[0] if emo_pred['score'] >= 0.5]
                if emotions:
                    all_emotions.extend(emotions)

        # Aggregate emotions across all chunks
        if not all_emotions:
            return {'emotions': [{"label": "neutral", "score": 0}]}

        # Optionally, you can further process and aggregate emotions, but this returns them all
        return {'emotions': all_emotions}

    def _get_sentiment_map(self) -> dict:
        """
        Provides a mapping of sentiment class indices to sentiment labels based on the configured levels.

        Returns a dictionary that maps the numerical index of sentiment classes to
        their corresponding descriptive labels (e.g., 'Positive', 'Negative', 'Neutral').
        The mapping is determined by the `levels` attribute set during initialization.

        Returns:
            dict: A dictionary mapping sentiment class indices to sentiment labels.
            For example, for 5 levels: {0: "Very Negative", 1: "Negative", 2: "Neutral", 3: "Positive", 4: "Very Positive"}.
        """ # noqa
        if self.levels == -3:  # Inverted
            return {
                0: "Neutral",
                1: "Positive",
                2: "Negative",
            }
        elif self.levels == 5:
            return {
                0: "Very Negative",
                1: "Negative",
                2: "Neutral",
                3: "Positive",
                4: "Very Positive"
            }
        elif self.levels == 3:
            return {
                0: "Negative",
                1: "Neutral",
                2: "Positive",
            }
        else:
            return {
                0: "Negative",
                1: "Positive",
            }

    def predict_sentiments_batch(self, texts: List[str]) -> List[dict]:
        results = self.sentiment_classifier(texts, truncation=True)
        sentiments = []
        for prediction in results:
            scores = prediction
            probabilities = [item['score'] for item in scores]
            labels = [item['label'] for item in scores]
            if all(label.lower() in ['positive', 'neutral', 'negative'] for label in labels):
                predicted_label = max(scores, key=lambda x: x['score'])['label']
                sentiments.append({
                    "score": probabilities,
                    "predicted_sentiment": predicted_label.capitalize()
                })
                continue

            label_to_index = {label: idx for idx, label in enumerate(labels)}
            predicted_label = max(scores, key=lambda x: x['score'])['label']
            predicted_class = label_to_index[predicted_label]
            sentiment_map = self._get_sentiment_map()
            sentiments.append({
                "score": probabilities,
                "predicted_sentiment": sentiment_map.get(predicted_class, predicted_label)
            })
        return sentiments

    def predict_sentiment(self, text: str) -> dict:
        """
        Predicts the sentiment of the input text.

        Utilizes the sentiment analysis pipeline to classify the text and returns
        sentiment scores and the predicted sentiment label. Handles text chunking
        for texts exceeding the maximum token length.

        Args:
            text (str): The text to analyze for sentiment.

        Returns:
            dict: A dictionary containing sentiment analysis results.
            Includes 'score' (list of sentiment scores) and 'predicted_sentiment' (string label).
            Returns None if the input text is empty.
        """
        if not text:
            return None
        if isinstance(text, float):
            text = str(text)

        # Tokenize the text to check its length
        encoded_text = self.tokenizer.encode(text, truncation=False, add_special_tokens=True)

        # Handle long texts by splitting them into chunks if needed
        if len(encoded_text) > self.max_length:
            text_chunks = self._split_text(text, self.max_length)
            return self._predict_multiple_chunks_pipeline(text_chunks)

        # Use the pipeline to predict sentiment for shorter texts
        predictions = self.sentiment_classifier(text)

        # Since top_k=None, predictions is a list of lists
        # Each inner list contains dicts with 'label' and 'score'
        scores = predictions[0]

        # Extract scores and labels
        probabilities = [item['score'] for item in scores]
        labels = [item['label'] for item in scores]

        # Check if labels are descriptive (e.g., 'positive', 'neutral', 'negative')
        if all(label.lower() in ['positive', 'neutral', 'negative'] for label in labels):
            # If labels are descriptive, no need for custom mapping
            predicted_label = max(scores, key=lambda x: x['score'])['label']
            return {
                "score": probabilities,
                "predicted_sentiment": predicted_label.capitalize()
            }

        # Map labels to indices
        label_to_index = {}
        for _, label in enumerate(labels):
            if label.startswith("LABEL_"):
                label_idx = int(label.replace("LABEL_", ""))
                label_to_index[label] = label_idx
        if not label_to_index:
            label_to_index = {label: idx for idx, label in enumerate(labels)}

        predicted_label = max(scores, key=lambda x: x['score'])['label']
        predicted_class = label_to_index[predicted_label]

        # Map predicted_class to sentiment
        sentiment_map = self._get_sentiment_map()

        predicted_sentiment = sentiment_map.get(predicted_class, predicted_label)

        return {
            "score": probabilities,
            "predicted_sentiment": predicted_sentiment
        }

    def _predict_multiple_chunks_pipeline(self, chunks: list) -> dict:
        """
        Predicts sentiment for multiple text chunks using the pipeline and aggregates the results.

        Averages sentiment probabilities across all chunks to determine the overall sentiment.
        This method is specifically designed for handling long texts split into smaller processable chunks.

        Args:
            chunks (list): A list of text chunks (strings) to analyze for sentiment.

        Returns:
            dict: A dictionary containing the aggregated sentiment analysis results.
            Includes 'score' (list of averaged sentiment probabilities) and 'predicted_sentiment' (string label
            of the overall predicted sentiment).
        """  # noqa
        all_probabilities = []
        for chunk in chunks:
            predictions = self.sentiment_classifier(chunk)
            scores = predictions[0]
            probabilities = [item['score'] for item in scores]
            all_probabilities.append(torch.tensor(probabilities))

        # Averaging probabilities across chunks
        avg_probabilities = torch.mean(torch.stack(all_probabilities), dim=0)
        predicted_class = torch.argmax(avg_probabilities).item()

        sentiment_map = self._get_sentiment_map()
        predicted_sentiment = sentiment_map.get(predicted_class, "Unknown")

        return {
            "score": avg_probabilities.tolist(),
            "predicted_sentiment": predicted_sentiment
        }

    def _split_text(self, text: str, max_length: int) -> List[str]:
        """
        Splits input text into processable chunks based on sentence boundaries and token count.

        Ensures that each chunk does not exceed the maximum token length limit of the model.
        It attempts to split text at sentence boundaries to maintain semantic integrity where possible.
        Handles cases where sentences themselves are too long by further splitting them.

        Args:
            text (str): The input text to be split.
            max_length (int): The maximum token length allowed for each chunk.

        Returns:
            List[str]: A list of text chunks, each guaranteed to be within the token limit.
        """
        chunks = []
        current_chunk = []
        split_by_sentences = text.split(". ")

        for sentence in split_by_sentences:
            sentence_tokens = self.tokenizer.encode(sentence, add_special_tokens=False)
            # +1 for potential separator
            if len(current_chunk) + len(sentence_tokens) + 1 <= max_length:
                current_chunk.extend(sentence_tokens)
                # Add a separator between sentences
                current_chunk.append(self.tokenizer.sep_token_id)
            else:
                # Sentence is too long, add current chunk
                if current_chunk:
                    chunks.append(self.tokenizer.decode(current_chunk))
                    current_chunk = []
                # Handle long sentence: split it into smaller parts
                temp_sentence_chunks = []
                temp_sentence_chunks.extend(
                    sentence_tokens[i: i + max_length]
                    for i in range(0, len(sentence_tokens), max_length)
                )
                # If there are sentences shorter than the max_length
                if len(temp_sentence_chunks) > 1:
                    for i, chunk in enumerate(temp_sentence_chunks):
                        if i < len(temp_sentence_chunks) - 1:
                            chunks.append(self.tokenizer.decode(chunk))
                        else:
                            current_chunk.extend(chunk)
                else:
                    current_chunk.extend(sentence_tokens)

                if current_chunk:
                    current_chunk.append(self.tokenizer.sep_token_id)

        if current_chunk:
            chunks.append(self.tokenizer.decode(current_chunk))

        # Remove extra sentence separators that are not required
        for i, chunk in enumerate(chunks):
            if chunk.endswith(self.tokenizer.sep_token):
                chunks[i] = chunk[:-len(self.tokenizer.sep_token)]

        return chunks

    def split_into_sentences(self, text):
        """
        Splits a text into sentences using NLTK's sentence tokenizer.

        Leverages nltk.tokenize.sent_tokenize for robust sentence splitting,
        handling various sentence terminators and abbreviations.

        Args:
            text (str): The input text to be split into sentences.

        Returns:
            list: A list of strings, where each string is a sentence from the input text.
        """
        return sent_tokenize(text)

    def aggregate_sentiments(self, sentiments, levels):
        """
        Aggregates sentiment predictions from multiple texts to produce a single overall sentiment.

        Calculates the average sentiment score across a list of sentiment predictions
        and determines the overall predicted sentiment based on these averages.

        Args:
            sentiments (list): A list of dictionaries, each containing sentiment prediction results
            for a text (output from `predict_sentiment`).
            levels (int): The number of sentiment levels used in the analysis, determining the sentiment map.

        Returns:
            str: The aggregated predicted sentiment label (e.g., 'Positive', 'Negative', 'Neutral').
        """
        # Initialize an array to hold cumulative scores
        cumulative_scores = torch.zeros(levels)
        for sentiment in sentiments:
            scores = torch.tensor(sentiment['score'][0])
            cumulative_scores += scores

        # Calculate average scores
        avg_scores = cumulative_scores / len(sentiments)
        predicted_class = torch.argmax(avg_scores).item()

        if levels == 5:
            sentiment_map = {
                0: "Very Negative",
                1: "Negative",
                2: "Neutral",
                3: "Positive",
                4: "Very Positive"
            }
        elif levels == 3:
            sentiment_map = {
                0: "Negative",
                1: "Neutral",
                2: "Positive",
            }
        else:
            sentiment_map = {
                0: "Negative",
                1: "Positive",
            }

        return sentiment_map[predicted_class]


class SentimentAnalysis(FlowComponent):
    """
    Applies sentiment analysis and emotion detection to a DataFrame of text data.

    This component processes a DataFrame, applying Hugging Face Transformer models
    to analyze the sentiment and emotions expressed in a specified text column.
    It leverages the `ModelPrediction` class to perform the actual predictions
    and integrates these results back into the DataFrame.

    Properties:
        text_column (str): The name of the DataFrame column containing the text to analyze.
        Defaults to 'text'.
        sentiment_model (str): Model name for sentiment analysis.
        Defaults to 'tabularisai/robust-sentiment-analysis'.
        emotions_model (str): Model name for emotion detection.
        Defaults to 'cardiffnlp/twitter-roberta-base-emotion'.
        pipeline_classification (str): Classification type for the pipeline (e.g., 'sentiment-analysis').
        Defaults to 'sentiment-analysis'.
        with_average (bool): Boolean to indicate if sentiment should be averaged across rows (if applicable).
        Defaults to True.
        sentiment_levels (int): Number of sentiment levels (2, 3, or 5). Default is 5.
        use_bert (bool): Boolean to use BERT model for sentiment analysis. Defaults to False.
        use_roberta (bool): Boolean to use RoBERTa model for sentiment analysis. Defaults to False.
        use_bertweet (bool): Boolean to use BERTweet model for sentiment analysis. Defaults to False.

    Returns:
        DataFrame: The input DataFrame augmented with new columns for sentiment scores,
        predicted sentiment, emotion scores, and predicted emotion.
        Specifically, it adds: 'sentiment_scores', 'sentiment_score', 'emotions_score',
        'predicted_emotion', and 'predicted_sentiment' columns.

    Raises:
        ComponentError: If input data is not a Pandas DataFrame or if the text column is not found.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          SentimentAnalysis:
          # attributes here
        ```
    """
    _version = "1.0.0"
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Extract sentiment analysis."""
        self.parallel: bool = kwargs.pop('parallel', False)
        self.text_column: str = kwargs.pop('text_column', 'text')
        self._sentiment_model: str = kwargs.pop(
            'sentiment_model',
            'tabularisai/robust-sentiment-analysis'
        )
        self._emotion_model: str = kwargs.pop(
            'emotions_model',
            "cardiffnlp/twitter-roberta-base-emotion"
        )
        self._classification: str = kwargs.pop(
            'pipeline_classification',
            'sentiment-analysis'
        )
        self.with_average: bool = kwargs.pop('with_average', True)
        self.sentiment_levels: int = kwargs.pop('sentiment_levels', 5)
        self._use_bert: bool = kwargs.pop('use_bert', False)
        self._use_roberta: bool = kwargs.pop('use_roberta', False)
        self._use_bertweet: bool = kwargs.pop('use_bertweet', False)
        # Increase batch size for better performance
        self.chunk_size: int = 1000
        self.max_workers: int = 1  # Reduce workers to avoid multiple pipeline instances
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError(
                "Data Not Found",
                status=404
            )
        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError(
                "Incompatible Data, we need a Pandas Dataframe",
                status=404
            )
        # Create a single instance of the predictor
        print("[DEBUG] Creating single ModelPrediction instance")
        self._predictor = ModelPrediction(
            sentiment_model=self._sentiment_model,
            emotions_model=self._emotion_model,
            classification=self._classification,
            max_length=512,
            levels=self.sentiment_levels,
            use_bertweet=self._use_bertweet,
            use_bert=self._use_bert,
            use_roberta=self._use_roberta
        )
        return True

    async def close(self):
        pass

    def _analyze_chunk(self, chunk: pd.DataFrame, predictor: ModelPrediction):
        """
        Analyzes a chunk of the DataFrame using the shared predictor instance.

        Args:
            chunk (pd.DataFrame): The DataFrame chunk to process.
            predictor (ModelPrediction): Optional shared predictor instance (for sequential mode only).
        """

        chunk = chunk.copy()
        chunk['sentiment'] = predictor.predict_sentiments_batch(
            chunk[self.text_column].astype(str).fillna("").tolist()
        )
        chunk['emotions'] = chunk[self.text_column].astype(str).fillna("").apply(
            predictor.predict_emotion
        )
        with contextlib.suppress(Exception):
            torch.cuda.empty_cache()
        return chunk

    async def run(self):
        """
        Executes the sentiment analysis and emotion detection process on the input DataFrame.

        Uses a single shared predictor instance to process data in larger batches.
        After processing, it concatenates the results and extracts relevant prediction scores and labels.

        Returns:
            pd.DataFrame: The DataFrame with added sentiment and emotion analysis results.
        """
        print("[DEBUG] Starting sentiment analysis with single predictor instance")
        # Split the dataframe into larger chunks
        num_chunks = np.ceil(len(self.data) / self.chunk_size).astype(int)
        chunks = np.array_split(self.data, num_chunks)

        # Process chunks sequentially using the shared predictor
        processed_chunks = []
        for i, chunk in enumerate(chunks):
            print(f"[DEBUG] Processing chunk {i+1}/{len(chunks)}")
            processed_chunk = self._analyze_chunk(chunk, self._predictor)
            processed_chunks.append(processed_chunk)

        # Concatenate all the chunks back into a single DataFrame
        df = pd.concat(processed_chunks)
        # extract the predicted sentiment and emotion
        try:
            # Extract 'sentiment_score' from 'sentiment' column (e.g., first score in the list)
            df['sentiment_scores'] = df['sentiment'].apply(
                lambda x: x.get('score', []) if x and isinstance(x.get('score', []), list) else []
            )
            # Max value of sentiments
            df['sentiment_score'] = df['sentiment_scores'].apply(
                lambda x: max(x) if isinstance(x, list) and len(x) > 0 else None
            )
            # Extract 'emotions_score' from 'emotions' column (e.g., score from the first emotion)
            df['emotions_score'] = df['emotions'].apply(
                lambda x: x.get('emotions', [{'score': None}])[0]['score'] if x and isinstance(x.get('emotions', []), list) and len(x['emotions']) > 0 else None  # noqa
            )
            # Expand the 'emotions' and 'sentiments' column to extract the label
            df['predicted_emotion'] = df['emotions'].apply(
                lambda x: x.get('emotions', [{'label': None}])[0]['label'] if x and isinstance(x.get('emotions', []), list) and len(x.get('emotions', [])) > 0 else None  # noqa
            )
            df['predicted_sentiment'] = df['sentiment'].apply(
                lambda x: x.get('predicted_sentiment', None) if x else None
            )
        except Exception as e:
            print(e)
            pass
        self._result = df
        if self._debug is True:
            print("== DATA PREVIEW ==")
            print(self._result)
            print()
            print("::: Printing Column Information === ")
            for column, t in df.dtypes.items():
                print(column, "->", t, "->", df[column].iloc[0])
        return self._result