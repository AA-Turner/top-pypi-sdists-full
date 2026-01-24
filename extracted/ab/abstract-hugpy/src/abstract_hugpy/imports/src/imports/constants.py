from .init_imports import *
from .module_imports import *
from .directory_manager import *
DEFAULT_REL_FILE_PATH = "datas/modules.json"
# Optional: Hugging Face local cache directory for safety

# near your helpers
YT_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
DATA_SCHEMA = {
    "data_id": None,
    "url": None,
    "file_path": None,
    "info_path": "info.json",

    # text + metadata
    "text_path": "document.txt",
    "metadata_path": "metadata.json",
    "summary_path": "summary.txt",
    "keywords_path": "keywords.json",

    # optional audio/video derivatives
    "audio_path": "audio.wav",
    "speech_path": "speech.json",
    "preview_image": "preview.jpg",

    # aggregations
    "total_info_path": "total_info.json",
    "total_aggregated_path": "total_aggregated.json",

    # analysis
    "embeddings_path": "embeddings.npy",
    "entities_path": "entities.json",
    "topics_path": "topics.json",
    "metatags_path": "meta.json",
    "pagedata_path": "page.json"
}



# Full schema
VIDEO_SCHEMA = {
    "video_path": "video.mp4",
    "info_path": "info.json",
    "audio_path": "audio.wav",
    "whisper_path": "whisper.json",
    "captions_path": "captions.srt",
    "metadata_path": "metadata.json",
    "thumbnail_path": "thumb.jpg",
    "thumbnails_path": "thumbnails.json",
    "total_info_path": "total_info.json",
    "total_aggregated_path": "total_aggregated.json",
    "aggregated_directory": "aggregated",
    "aggregated_dir": {
        "aggregated_json_path": "aggregated.json",
        "aggregated_metadata_path": "aggregated_metadata.json",
        "best_clip_path": "best_clip.txt",
        "hashtags_path": "hashtags.txt",
    },
    "thumbnails_directory": "thumbnails",
    "thumbnails_dir": {
        "frames": "{video_id}_frame_{i}.jpg",  # pattern
    },
    "metatags_path": "meta.json",
    "pagedata_path": "page.json"
}
REMOVE_PHRASES = ['Video Converter', 'eeso', 'Auseesott', 'Aeseesott', 'esoft']
FULL_KEY_MAP = {
    "title":        {"keys": ["title", "fulltitle", "seo_title"]},
    "description":  {"keys": ["description", "summary", "seo_description"]},
    "keywords":     {"keys": ["keywords", "categories", "tags", "seo_tags"]},
    "category":     {"keys": ["category", "categories"], "derive": "classify_category"},
    "transcript":   {"keys": ["text", "captions"], "source": ["whisper_result.json", "captions.srt"]},
    "thumbnails":   {"keys": ["thumbnail", "image", "thumbnail_url", "thumbnail_paths"]},
    "url":          {"keys": ["webpage_url", "url", "domain", "canonical_url"]},
    "duration":     {"keys": ["duration", "duration_seconds", "duration_formatted"]},
    "format":       {"keys": ["format", "format_note", "resolution"]},
    "file_size":    {"keys": ["file_size", "file_size_mb"]},
    "uploader":     {"keys": ["uploader", "uploader_id", "uploader_url"]},
    "publication_date": {"keys": ["upload_date", "publication_date"]},
    "schema_markup":    {"keys": ["schema_markup"]},
    "social_metadata":  {"keys": ["social_metadata"]},
    "video_url":    {"keys": ["contentUrl", "video_url"]},
    "audio_path":   {"keys": ["audio_path"]},
    "video_path":   {"keys": ["video_path"]},
    "metatags_path":   {"keys": ["metatags_path"]},
    "pagedata_path":   {"keys": ["pagedata_path"]},
    "info_flags":   {"keys": ["info", "metadata", "whisper", "captions", "thumbnails"]}  # from total_info.json
}


MODULE_DEFAULTS = {
    "whisper": {
        "path": "/mnt/24T/hugging_face/modules/whisper_base",
        "repo_id": "openai/whisper-base",
        "handle": "whisper"
    },
    "keybert": {
        "path": "/mnt/24T/hugging_face/modules/all_minilm_l6_v2",
        "repo_id": "sentence-transformers/all-MiniLM-L6-v2",
        "handle": "keybert"
    },
    "summarizer": {
        "path": "/mnt/24T/hugging_face/modules/text_summarization",
        "repo_id": "Falconsai/text_summarization",
        "handle": "summarizer"
    },
    "flan": {
        "path": "/mnt/24T/hugging_face/modules/flan_t5_xl",
        "repo_id": "google/flan-t5-xl",
        "handle": "flan"
    },
    "bigbird": {
        "path": "/mnt/24T/hugging_face/modules/led_large_16384",
        "repo_id": "allenai/led-large-16384",
        "handle": "bigbird"
    },
    "deepcoder": {
        "path": "/mnt/24T/hugging_face/modules/DeepCoder-14B",
        "repo_id": "agentica-org/DeepCoder-14B-Preview",
        "handle": "deepcoder"
    },
    "huggingface": {
        "path": "/mnt/24T/hugging_face/modules/hugging_face_models",
        "repo_id": "huggingface/hub",
        "handle": "hugging_face_models"
    },
    "zerosearch": {
        "path": "/mnt/24T/hugging_face/modules/ZeroSearch_model",
        "repo_id": "Alibaba-NLP/ZeroSearch-3B",
        "handle": "ZeroSearch"
    }
}

DEFAULT_MODULE_PATHS = {k:v.get('path') for k,v in MODULE_DEFAULTS.items()}
DEFAULT_MODULE_NAMES = {k:v.get('name') for k,v in MODULE_DEFAULTS.items()}
DEFAULT_MODULE_IDS = {k:v.get('id') for k,v in MODULE_DEFAULTS.items()}
