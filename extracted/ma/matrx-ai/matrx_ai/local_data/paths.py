"""Canonical paths used by matrx-ai provider catalog sync utilities."""

import os

_HERE = os.path.dirname(os.path.abspath(__file__))

ANTHROPIC_MODELS_FILE = os.path.join(_HERE, "anthropic_models_data.py")
OPENAI_MODELS_FILE = os.path.join(_HERE, "openai_models_data.py")
GOOGLE_MODELS_FILE = os.path.join(_HERE, "google_models_data.py")
GROQ_MODELS_FILE = os.path.join(_HERE, "groq_models_data.py")
TOGETHER_MODELS_FILE = os.path.join(_HERE, "together_models_data.py")
XAI_MODELS_FILE = os.path.join(_HERE, "xai_models_data.py")
CEREBRAS_MODELS_FILE = os.path.join(_HERE, "cerebras_models_data.py")

MODELS_DATA_FILE = os.path.join(_HERE, "models_data.py")
MODELS_TS_FILE = None
HISTORY_FILE = os.path.join(_HERE, "data_history.json")
