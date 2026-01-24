# /mnt/24T/hugging_face/new_hugs/keybertManager/functions/module/keybert_module.py
from ..imports import *
logger = get_logFile(__name__)
DEFAULT_WHISPER_MODEL_PATH = DEFAULT_MODULE_PATHS.get("whisper")
class whisperManager(metaclass=SingletonMeta):
    def __init__(self,
                 model_size: str = None,
                 whisper_model_path: str = None):
        model_size = model_size or "base"
        if not hasattr(self, 'initialized') or not hasattr(self, 'model_size') or model_size != self.model_size:
            self.whisper = get_whisper()
            self.whisper_model_path = whisper_model_path or DEFAULT_WHISPER_MODEL_PATH
            self.model_size = model_size
            self.whisper_model = self.whisper.load_model(self.model_size, download_root=self.whisper_model_path)
    def run_whisper_func(self,func,*args,**kwargs):
        return run_pruned_func(func, *args, **kwargs)
def get_whisperManager(
        model_size=None,
        whisper_model_path=None
        ):
    whisper_mgr = whisperManager(
        model_size=model_size,
        whisper_model_path=whisper_model_path
        )
    return whisper_mgr
def get_whisper_model(
        model_size=None,
        whisper_model_path=None,
    ):
    whisper_mgr = whisperManager(
        model_size=model_size,
        whisper_model_path=whisper_model_path
        )
    return whisper_mgr.whisper_model
def run_whisper_func(func,
                     *args,
                     model_size=None,
                     whisper_model_path=None,
                     **kwargs
                     ):
    
    whisper_mgr = get_whisperManager(
        model_size=model_size,
        whisper_model_path=whisper_model_path
        )
    return whisper_mgr.run_whisper_func(func, *args, **kwargs)
def whisper_transcribe(
    audio_path: str = None,
    model_size: str = "small",
    language: str = "english",
    use_silence: bool = True,
    task=None,
    whisper_model_path: str = None
):
    model = get_whisper_model(model_size=model_size, whisper_model_path=whisper_model_path)
    return model.transcribe(audio_path, language=language)

def get_metadata_data(self, video_url=None, video_id=None):
    return self.get_spec_data(
        'metadata',
        'metadata_path',
        video_url=video_url,
        video_id=video_id
        )

def get_whisper_text(self, video_url):
    whisper_result = self.get_whisper_result(video_url)
    return whisper_result.get('text')

def get_whisper_segments(self, video_url):
    whisper_result = self.get_whisper_result(video_url)
    return whisper_result.get('segments')
