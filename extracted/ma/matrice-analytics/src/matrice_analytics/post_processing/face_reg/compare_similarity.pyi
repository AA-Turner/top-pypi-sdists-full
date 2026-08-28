"""Auto-generated stub for module: compare_similarity."""
from typing import Any, Dict, List, Optional, Tuple

from ..Trackers.integration import ConfigDrivenTracker, TrackerProfile

# Constants
ALIGN: bool
DETECTOR_BACKEND: str
MODEL_NAME: str

# Functions
def compare_identity_and_samples(identity_folder: str, sample_folder: str, threshold: float = 0.82) -> Any:
    """
    Compare each sample image against all identities (subdirectories) using average similarity.
    """
    ...
def compute_pairwise_similarities(embeddings: List[List[float]]) -> Dict[Tuple[int, int], float]:
    """
    Computes pairwise cosine similarities for a list of embeddings using NumPy.
    """
    ...
def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Cosine similarity using NumPy operations with numeric safety.
    """
    ...
def detect_identity_in_video(video_path: str, identity_folder: str, output_path: str = 'output_identity_detection.mp4', threshold: float = 0.75, person_to_embs: Any = None) -> Any: ...
def get_embedding(image_path: str) -> List[float]:
    """
    Return the first face embedding from an image using DeepFace.represent, normalized to unit length.
    """
    ...
def get_embeddings_from_folder(folder_path: str, max_images: Optional[int] = None) -> Tuple[List[List[float]], List[str]]: ...
def get_embeddings_per_person(identity_root: str, max_images_per_person: Optional[int] = None) -> Dict[str, List[List[float]]]:
    """
    Build a mapping: person (subdirectory name) -> list of embeddings from all images inside it.
    """
    ...
def normalize_embedding(vec: List[float]) -> List[float]:
    """
    Normalize an embedding vector to unit length (L2).
    
        Returns a float32 list to ensure consistent downstream math and JSON safety.
    """
    ...

# Classes
class FaceTracker:
    # Embedding-based face tracker (mirrors tracker logic in face_recognition_model.py):
    # - Matches new face embeddings to existing tracks via cosine similarity
    # - Creates a new track when no match exceeds the similarity threshold

    def __init__(self: Any, similarity_threshold: float = 0.6) -> None: ...

    def assign_track_id(self: Any, embedding: List[float], frame_id: Optional[int] = None) -> str: ...

class TemporalIdentityManager:
    # Maintains stable identity labels per track using temporal smoothing and embedding history.
    #
    # - Suppresses brief misclassifications (1-2 frames)
    # - Holds previous identity during short UNKNOWN gaps using unknown_patience
    # - Fallback: when current is UNKNOWN, match the prototype (mean) embedding history to identities

    def __init__(self: Any, person_to_embs: Dict[str, List[List[float]]], recognition_threshold: float = 0.7, history_size: int = 20, unknown_patience: int = 7, switch_patience: int = 5, fallback_margin: float = 0.05) -> None: ...

    def update(self: Any, track_id: int, emb: List[float], inst_label: Optional[str], inst_sim: float) -> Tuple[str, float]: ...

