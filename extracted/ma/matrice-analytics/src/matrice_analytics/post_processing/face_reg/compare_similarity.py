import os
from typing import List, Dict, Tuple, Optional, Any
from pathlib import Path
from collections import deque, defaultdict

import numpy as np
import cv2
from deepface import DeepFace
import hashlib

# Advanced tracker (ByteTrack-like)
from advanced_tracker import AdvancedTracker
from advanced_tracker.config import TrackerConfig

# Global DeepFace configuration
MODEL_NAME = "Facenet512"       # per DeepFace docs
DETECTOR_BACKEND = "retinaface"  # RetinaFace
ALIGN = True                     # enable face alignment


def normalize_embedding(vec: List[float]) -> List[float]:
    """Normalize an embedding vector to unit length (L2).

    Returns a float32 list to ensure consistent downstream math and JSON safety.
    """
    arr = np.asarray(vec, dtype=np.float32)
    if arr.size == 0:
        return []
    n = np.linalg.norm(arr)
    if n > 0:
        arr = arr / n
    return arr.tolist()


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Cosine similarity using NumPy operations with numeric safety."""
    a = np.asarray(vec1, dtype=np.float32)
    b = np.asarray(vec2, dtype=np.float32)
    if a.size == 0 or b.size == 0:
        return 0.0
    an = np.linalg.norm(a)
    bn = np.linalg.norm(b)
    if an == 0.0 or bn == 0.0:
        return 0.0
    sim = float(np.dot(a, b) / (an * bn))
    if sim > 1.0:
        sim = 1.0
    elif sim < -1.0:
        sim = -1.0
    return sim


class FaceTracker:
    """
    Embedding-based face tracker (mirrors tracker logic in face_recognition_model.py):
    - Matches new face embeddings to existing tracks via cosine similarity
    - Creates a new track when no match exceeds the similarity threshold
    """

    def __init__(self, similarity_threshold: float = 0.60) -> None:
        self.similarity_threshold = similarity_threshold
        self.tracks: Dict[str, Dict[str, object]] = {}
        self.track_counter: int = 1

    def _find_matching_track(self, new_embedding: List[float]) -> Optional[str]:
        if not new_embedding:
            return None
        best_similarity: float = 0.0
        best_track_id: Optional[str] = None
        for track_id, data in self.tracks.items():
            stored_embedding = data.get("embedding")
            if stored_embedding:
                sim = cosine_similarity(new_embedding, stored_embedding)
                if sim > self.similarity_threshold and sim > best_similarity:
                    best_similarity = sim
                    best_track_id = track_id
        return best_track_id

    def assign_track_id(self, embedding: List[float], frame_id: Optional[int] = None) -> str:
        match_id = self._find_matching_track(embedding)
        if match_id is not None and match_id in self.tracks:
            # Update last seen frame for the matched track
            self.tracks[match_id]["last_seen_frame"] = frame_id
            return match_id

        # Create a new track
        new_id = f"face_id_{self.track_counter}"
        self.tracks[new_id] = {
            "embedding": normalize_embedding(embedding),
            "created_frame": frame_id,
            "last_seen_frame": frame_id,
        }
        self.track_counter += 1
        return new_id


def get_embedding(image_path: str) -> List[float]:
    """Return the first face embedding from an image using DeepFace.represent, normalized to unit length."""
    reps = DeepFace.represent(
        img_path=image_path,
        model_name=MODEL_NAME,
        detector_backend=DETECTOR_BACKEND,
        align=ALIGN,
    )
    #TODO: Normalize embedding to unit length?

    # DeepFace.represent returns a list of dicts; take the first face
    if reps:
        return reps[0]["embedding"]
    else: return None


def compute_pairwise_similarities(embeddings: List[List[float]]) -> Dict[Tuple[int, int], float]:
    """
    Computes pairwise cosine similarities for a list of embeddings using NumPy.
    """
    # Convert the list of lists to a NumPy array
    embedding_matrix = np.array(embeddings)
    

    norms = np.linalg.norm(embedding_matrix, axis=1, keepdims=True)
    # Avoid division by zero for zero-vectors
    norms = np.where(norms == 0, 1, norms)
    normalized_embeddings = embedding_matrix / norms
    
    # 2. Compute the dot product of the normalized matrix with its transpose.
    #    For unit vectors, the dot product is equivalent to the cosine similarity.
    similarity_matrix = normalized_embeddings @ normalized_embeddings.T
    
    # 3. Extract the upper triangle of the matrix (where j > i) to match the original output.
    n = len(embeddings)
    # np.triu_indices(n, k=1) gets the indices (rows, cols) of the upper triangle,
    # excluding the diagonal (k=1).
    rows, cols = np.triu_indices(n, k=1)
    
    # 4. Create the dictionary from the indices and the corresponding similarity values.
    similarity_dict = {(r, c): similarity_matrix[r, c] for r, c in zip(rows, cols)}
    
    return similarity_dict


def get_embeddings_from_folder(folder_path: str, max_images: Optional[int] = None) -> Tuple[List[List[float]], List[str]]:
    image_paths = sorted([p for p in Path(folder_path).iterdir() if p.suffix.lower() in {'.jpg', '.jpeg', '.png'}])
    if max_images is not None:
        image_paths = image_paths[:max_images]
    embeddings: List[List[float]] = []
    img_names: List[str] = []
    for img_path in image_paths:
        try:
            emb = get_embedding(str(img_path))
            embeddings.append(emb)
            img_names.append(img_path.name)
        except Exception as e:
            print(f"Skipping {img_path}: {e}")
    return embeddings, img_names


def get_embeddings_per_person(identity_root: str, max_images_per_person: Optional[int] = None) -> Dict[str, List[List[float]]]:
    """Build a mapping: person (subdirectory name) -> list of embeddings from all images inside it."""
    root = Path(identity_root)
    if not root.exists():
        raise FileNotFoundError(f"Identity root does not exist: {identity_root}")

    # discover subdirectories (persons)
    person_dirs = [p for p in sorted(root.iterdir()) if p.is_dir()]

    person_to_embeddings: Dict[str, List[List[float]]] = {}
    for person_dir in person_dirs:
        image_paths = [p for p in sorted(person_dir.iterdir()) if p.suffix.lower() in {'.jpg', '.jpeg', '.png'}]
        if max_images_per_person is not None:
            image_paths = image_paths[:max_images_per_person]

        embeddings: List[List[float]] = []
        for img_path in image_paths:
            try:
                embeddings.append(get_embedding(str(img_path)))
            except Exception as e:
                print(f"Skipping {img_path}: {e}")
        if embeddings:
            person_to_embeddings[person_dir.name] = embeddings

    # Fallback: if there were no subdirectories, try treating root images as one person (root name)
    if not person_to_embeddings:
        root_embs, _ = get_embeddings_from_folder(identity_root, max_images_per_person)
        if root_embs:
            person_to_embeddings[root.name] = root_embs

    return person_to_embeddings


def compare_identity_and_samples(identity_folder: str, sample_folder: str, threshold: float = 0.82):
    """Compare each sample image against all identities (subdirectories) using average similarity."""
    person_to_embs = get_embeddings_per_person(identity_folder)
    sample_embs, sample_names = get_embeddings_from_folder(sample_folder)

    if not person_to_embs or not sample_embs:
        print("No embeddings extracted from one of the folders – aborting.")
        return

    print(f"Computed identities: {list(person_to_embs.keys())}")
    print(f"Computed {sum(len(v) for v in person_to_embs.values())} identity embeddings across {len(person_to_embs)} persons and {len(sample_embs)} sample embeddings.")

    for s_emb, s_name in zip(sample_embs, sample_names):
        print(f"\nAverage similarity for sample '{s_name}':")
        best_person = None
        best_avg = -1.0
        for person, embs in person_to_embs.items():
            if not embs:
                continue
            scores = [cosine_similarity(s_emb, e) for e in embs]
            avg_score = float(np.mean(scores)) if scores else 0.0
            flag = "<-- MATCH" if avg_score >= threshold else ""
            print(f"    {person:20s}: {avg_score:.4f} {flag}")
            if avg_score > best_avg:
                best_avg = avg_score
                best_person = person
        print(f"--> Top-1: {best_person} ({best_avg:.4f})")


class TemporalIdentityManager:
    """
    Maintains stable identity labels per track using temporal smoothing and embedding history.

    - Suppresses brief misclassifications (1-2 frames)
    - Holds previous identity during short UNKNOWN gaps using unknown_patience
    - Fallback: when current is UNKNOWN, match the prototype (mean) embedding history to identities
    """

    def __init__(
        self,
        person_to_embs: Dict[str, List[List[float]]],
        recognition_threshold: float = 0.7,
        history_size: int = 20,
        unknown_patience: int = 7,
        switch_patience: int = 5,
        fallback_margin: float = 0.05,
    ) -> None:
        self.person_to_embs = person_to_embs
        self.threshold = recognition_threshold
        self.history_size = history_size
        self.unknown_patience = unknown_patience
        self.switch_patience = switch_patience
        self.fallback_margin = fallback_margin
        self.tracks: Dict[int, Dict[str, object]] = {}

    def _ensure_track(self, track_id: int) -> None:
        if track_id not in self.tracks:
            self.tracks[track_id] = {
                "stable_label": None,
                "label_votes": defaultdict(int),  # type: ignore
                "embedding_history": deque(maxlen=self.history_size),
                "unknown_streak": 0,
                "streaks": defaultdict(int),  # label -> consecutive frames count
            }

    def _compute_best_identity(self, emb: List[float]) -> Tuple[Optional[str], float]:
        best_person = None
        best_avg = -1.0
        if not emb:
            return None, -1.0
        for person, embs in self.person_to_embs.items():
            if not embs:
                continue
            scores = [cosine_similarity(emb, e) for e in embs]
            avg_score = float(np.mean(scores)) if scores else 0.0
            if avg_score > best_avg:
                best_avg = avg_score
                best_person = person
        return best_person, best_avg

    def _compute_best_identity_from_history(self, track_state: Dict[str, object]) -> Tuple[Optional[str], float]:
        hist: deque = track_state["embedding_history"]  # type: ignore
        if not hist:
            return None, -1.0
        proto = np.mean(np.asarray(hist, dtype=np.float32), axis=0)
        return self._compute_best_identity(proto.tolist())

    def update(self, track_id: int, emb: List[float], inst_label: Optional[str], inst_sim: float) -> Tuple[str, float]:
        self._ensure_track(track_id)
        s = self.tracks[track_id]

        # Update embedding history
        if emb:
            s["embedding_history"].append(emb)  # type: ignore

        stable: Optional[str] = s["stable_label"]  # type: ignore

        # Determine candidate from instantaneous prediction
        if inst_label is not None and inst_label != "Unknown" and inst_sim >= self.threshold:
            s["label_votes"][inst_label] += 1  # type: ignore
            s["streaks"][inst_label] += 1  # type: ignore
            s["unknown_streak"] = 0  # type: ignore

            if stable is None:
                s["stable_label"] = inst_label
                return inst_label, inst_sim

            if inst_label == stable:
                return stable, inst_sim

            # Competing identity: switch only if sustained
            if s["streaks"][inst_label] >= self.switch_patience:  # type: ignore
                prev_votes = s["label_votes"][stable] if stable else 0  # type: ignore
                cand_votes = s["label_votes"][inst_label]  # type: ignore
                if cand_votes >= max(2, 0.75 * prev_votes) and inst_sim >= (self.threshold + 0.02):
                    s["stable_label"] = inst_label
                    # Reset other streaks to prevent oscillations
                    for k in list(s["streaks"].keys()):  # type: ignore
                        if k != inst_label:
                            s["streaks"][k] = 0  # type: ignore
                    return inst_label, inst_sim

            # Do not switch yet
            return stable if stable is not None else "Unknown", inst_sim

        # Instantaneous is UNK or low similarity
        s["unknown_streak"] = int(s["unknown_streak"]) + 1  # type: ignore
        # Short UNK bursts: keep previous label
        if stable is not None and s["unknown_streak"] <= self.unknown_patience:  # type: ignore
            return stable, inst_sim

        # Fallback: use prototype from history to infer identity
        fb_label, fb_sim = self._compute_best_identity_from_history(s)
        if fb_label is not None and fb_sim >= max(0.0, self.threshold - self.fallback_margin):
            s["label_votes"][fb_label] += 1  # type: ignore
            s["stable_label"] = fb_label
            s["unknown_streak"] = 0  # type: ignore
            return fb_label, fb_sim

        # No confident identity
        s["stable_label"] = stable  # keep whatever was last (may be None)
        return (stable if stable is not None else "Unknown"), inst_sim


def detect_identity_in_video(
        video_path: str,
        identity_folder: str,
        output_path: str = "output_identity_detection.mp4", threshold: float = 0.75, person_to_embs: Any=None):

    # Build per-person embeddings from identity root
    if not person_to_embs:
      person_to_embs = get_embeddings_per_person(identity_folder)
      if not person_to_embs:
          print("No identity embeddings – aborting video processing.")
          return

      print(f"Identities discovered: {list(person_to_embs.keys())}")
    else:
      print(f"Using Pre-computed Identities: {list(person_to_embs.keys())}")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Could not open video", video_path)
        return

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Advanced BYTETrack-like tracker configuration tuned for faces
    tracker_config = TrackerConfig(
        track_high_thresh=0.5,
        track_low_thresh=0.05,
        new_track_thresh=0.5,
        match_thresh=0.8,
        track_buffer=int(max(30, fps) * 10),  # allow short occlusions
        max_time_lost=int(max(30, fps) * 5),
        fuse_score=True,
        enable_gmc=False,
        frame_rate=int(max(1, fps))
    )
    adv_tracker = AdvancedTracker(tracker_config)

    # Temporal identity smoothing manager
    id_manager = TemporalIdentityManager(
        person_to_embs=person_to_embs,
        recognition_threshold=threshold,
        history_size=20,
        unknown_patience=7,
        switch_patience=5,
        fallback_margin=0.05,
    )

    # Unique track IDs across the whole video
    unique_track_ids = set()

    # Display and recognition gating settings
    PROBATION_FRAMES = 260  # suppress UNK label until this many frames for a track
    MIN_FACE_W = 40        # require minimum width for recognition attempt
    MIN_FACE_H = 80        # require minimum height for recognition attempt

    ##TODO: Consider aspect ratio of bounding box as well -- width/height > 0.5

    # Colors: pending/unknown (red), identified Navy Blue #(dark cyan-ish)
    COLOR_PENDING = (0, 0, 255)
    COLOR_IDENTIFIED = (128,0,0) #(160, 160, 0)

    # Track first seen frame index for probation logic
    track_first_seen: Dict[int, int] = {}

    def _track_id_to_color(track_id: str) -> Tuple[int, int, int]:
        """Deterministically map a track_id to a visible BGR color."""
        h = hashlib.md5((track_id or "").encode("utf-8")).digest()
        b, g, r = int(h[0]), int(h[1]), int(h[2])
        b = int(0.6 * b + 0.4 * 255)
        g = int(0.6 * g + 0.4 * 255)
        r = int(0.6 * r + 0.4 * 255)
        return (b, g, r)

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        try:
            # Get all face representations in the frame
            reps = DeepFace.represent(
                img_path=frame,
                model_name=MODEL_NAME,
                detector_backend=DETECTOR_BACKEND,
                align=ALIGN,
            )
        except Exception:
            reps = []

        # Prepare detections for the advanced tracker
        detections: List[Dict] = []
        for rep in reps:
            emb = rep.get("embedding", [])
            region = rep.get("facial_area", None)
            conf = rep.get("face_confidence", 0.99)
            if not region:
                continue
            x, y, w, h = region.get("x", 0), region.get("y", 0), region.get("w", 0), region.get("h", 0)
            x1, y1, x2, y2 = int(x), int(y), int(x + w), int(y + h)
            det = {
                "bounding_box": {"xmin": x1, "ymin": y1, "xmax": x2, "ymax": y2},
                "confidence": float(conf if isinstance(conf, (int, float)) else 0.99),
                "category": "face",
                "embedding": normalize_embedding(emb) if emb is not None else [],
                "facial_area": region,
                "frame_id": frame_idx,
            }
            detections.append(det)

        # Run tracker update
        tracked_dets: List[Dict] = adv_tracker.update(detections, img=frame) if detections else []

        # Draw and label tracked faces
        for det in tracked_dets:
            bbox = det.get("bounding_box", {})
            x1, y1, x2, y2 = int(bbox.get("xmin", 0)), int(bbox.get("ymin", 0)), int(bbox.get("xmax", 0)), int(bbox.get("ymax", 0))
            track_id = int(det.get("track_id", 0))
            conf = float(det.get("confidence", 0.0))
            emb = det.get("embedding", [])
            region = det.get("facial_area", {})

            # Track probation age & size gating
            if track_id not in track_first_seen:
                track_first_seen[track_id] = frame_idx
            age_frames = frame_idx - track_first_seen[track_id] + 1
            w_box = max(1, x2 - x1)
            h_box = max(1, y2 - y1)
            eligible_for_recognition = (w_box >= MIN_FACE_W and h_box >= MIN_FACE_H)

            # Compute instantaneous prediction only if eligible by size
            best_person = None
            best_avg = -1.0
            if emb: # embeddings from DeepFace are already list-like; we normalized when building dets
                for person, embs in person_to_embs.items():
                    if not embs:
                        continue
                    # person library may not be normalized if precomputed; normalize on the fly once
                    scores = [cosine_similarity(emb, normalize_embedding(e)) for e in embs]
                    avg_score = float(np.mean(scores)) if scores else 0.0
                    if avg_score > best_avg:
                        best_avg = avg_score
                        best_person = person

            # Update temporal identity only if eligible; otherwise keep last stable
            if eligible_for_recognition:
                inst_label = best_person if (best_person is not None and best_avg >= threshold) else "Unknown"
                final_label, final_sim = id_manager.update(track_id, emb, inst_label, best_avg)
            else:
                track_state = id_manager.tracks.get(track_id, {})
                stable_label = track_state.get("stable_label") if isinstance(track_state, dict) else None
                final_label = stable_label if stable_label is not None else "Unknown"
                final_sim = best_avg

            # Determine color and whether to show label
            unique_track_ids.add(track_id)
            is_identified = (final_label is not None and final_label != "Unknown")
            box_color = COLOR_IDENTIFIED if is_identified else COLOR_PENDING
            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 3)

            # Label text: show only if identified OR probation exceeded and still unknown
            resolution = str(w_box) + "x" + str(h_box)
            show_label = is_identified or (age_frames >= PROBATION_FRAMES and not is_identified)
            if show_label:
                label = final_label if is_identified else "Unknown"
                #label_text = f"{label} id:{track_id} conf:{conf:.2f} sim:{final_sim:.2f} res:{resolution}"
                label_text = f"{label}"
                text_org = (x1, max(0, y1 - 10))
                # Get text size (width, height)
                (text_w, text_h), baseline = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 1.35, 3)

                # Draw white rectangle as background
                cv2.rectangle(frame, (text_org[0], text_org[1] - text_h - baseline),   # top-left corner
                              (text_org[0] + text_w, text_org[1] + baseline),  # bottom-right corner
                              (255, 255, 255),  # white background
                              -1)               # thickness=-1 → filled
                cv2.putText(frame, label_text, text_org, cv2.FONT_HERSHEY_SIMPLEX, 1.35, box_color, 3, cv2.LINE_AA)

            # # Draw landmarks as red dots if present in region
            # landmarks = ["left_eye", "right_eye", "nose", "mouth_left", "mouth_right"]
            # for lm in landmarks:
            #     if isinstance(region, dict) and lm in region and region[lm]:
            #         lx, ly = region[lm]
            #         cv2.circle(frame, (int(lx), int(ly)), 4, (0, 0, 255), -1)

        # Overlay counts (top-right)
        # curr_count = len(tracked_dets)
        # total_count = len(unique_track_ids)
        # hud_text = f"Curr:{curr_count} Total:{total_count} Frame:{frame_idx}"
        # (tw, th), _ = cv2.getTextSize(hud_text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
        # cv2.rectangle(frame, (width - tw - 20, 10), (width - 10, 10 + th + 10), (0, 0, 0), -1)
        # cv2.putText(frame, hud_text, (width - tw - 15, 10 + th), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
        out.write(frame)
        frame_idx += 1

    cap.release()
    out.release()
    print("Video saved to", output_path)
    
if __name__ == "__main__":
    IDENTITY_FOLDER = "/content/JBK_Stream_Faces_Identities_EMP_NEW"
    SAMPLE_FOLDER = "/content/Test"


    VIDEO_PATH = "/content/Turnstile_Entry_Short_3.mp4"
    OUTPUT_VIDEO = "/content/entry_short3_debug1.mp4"


    THRESHOLD = 0.6

    # Image-folder comparison can keep a threshold for reporting
    #compare_identity_and_samples(IDENTITY_FOLDER, SAMPLE_FOLDER, THRESHOLD)

    # Video detection: no threshold; always draw best label
    if VIDEO_PATH and os.path.exists(VIDEO_PATH):
        detect_identity_in_video(VIDEO_PATH, IDENTITY_FOLDER, OUTPUT_VIDEO, THRESHOLD)
    else:
        print("Skipping video detection – VIDEO_PATH not set or file does not exist.")