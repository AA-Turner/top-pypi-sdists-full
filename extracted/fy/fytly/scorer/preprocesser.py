# preprocessor.py
import re
import string
import spacy
from nltk.corpus import stopwords
import nltk

# Download NLTK stopwords (run once or ensure it’s available)
nltk.download('stopwords')

class GraderPreprocessor:
    nlp = spacy.load("en_core_web_sm")  # Load spaCy's small English model
    stop_words = set(stopwords.words('english'))  # NLTK stopwords

    # Custom noise words (common resume "filler" terms)
    custom_noise = {
        "standard", "ix", "x", "class", "email", "phone", "number", "pin", "code",
        "address", "dob", "status", "unmarried", "gender", "female", "name",
        "language", "known", "detail", "percentage", "cgpa"
    }

    @staticmethod
    def preprocess(text: str) -> str:
        """
        Preprocess text by lowercasing, removing digits/punctuation, and lemmatizing.

        Args:
            text (str): Input text to preprocess

        Returns:
            str: Preprocessed text
        """
        # Lowercase the text
        text = text.lower()

        # Remove digits and punctuation
        text = re.sub(r'\d+', ' ', text)
        text = text.translate(str.maketrans('', '', string.punctuation))

        # Tokenize and lemmatize with spaCy
        doc = GraderPreprocessor.nlp(text)

        # Filter out stopwords, custom noise, and whitespace
        lemmatized_words = [
            token.lemma_
            for token in doc
            if token.text not in GraderPreprocessor.stop_words
            and token.text not in GraderPreprocessor.custom_noise
            and not token.is_space
        ]

        return ' '.join(lemmatized_words)