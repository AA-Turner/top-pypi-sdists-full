"""
Face Recognition with Embeddings Module

This module provides facial recognition capabilities with embedding extraction
for staff identification and unknown face management.

Key Features:
- Face detection and embedding extraction using MTCNN + MobileFaceNet
- Staff recognition via vector search API
- Unknown face processing with image upload
- Real-time tracking and analytics
- Metadata extraction (quality score, capture angle, timestamp)

Quick Start:
    from matrice_analytics.post_processing.face_reg import (
        FaceRecognitionEmbeddingUseCase,
        FaceRecognitionEmbeddingConfig,
    )

    # Create config
    config = FaceRecognitionEmbeddingConfig(
        similarity_threshold=0.8,
        confidence_threshold=0.5
    )

    # Process face recognition
    processor = FaceRecognitionEmbeddingUseCase()
    result = processor.process(model_output, config)
"""

from .embedding_manager import EmbeddingConfig, EmbeddingManager
from .face_recognition import (
    FaceRecognitionEmbeddingConfig,
    FaceRecognitionEmbeddingUseCase,
)

__all__ = [
    "FaceRecognitionEmbeddingUseCase",
    "FaceRecognitionEmbeddingConfig",
    "EmbeddingManager",
    "EmbeddingConfig",
]
