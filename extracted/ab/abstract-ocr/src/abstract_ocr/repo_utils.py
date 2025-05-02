from .functions import update_json_data,execute_if_bool,generate_file_id
from .variable_utils import *
from .video_utils import extract_audio_from_video,analyze_video_text
from .audio_utils import transcribe_with_whisper_local
from .text_utils import refine_keywords,get_summary
from .seo_utils import get_seo_data

def get_summary_data(info_data=None,**kwargs):
    info_data = info_data or {}
    result = get_summary(keywords=info_data.get('keywords'),
        full_text=info_data.get('full_text'))
    info_data['summary'] = result
    return info_data
def transcribe_with_whisper_local_data(info_data=None,**kwargs):
    info_data = info_data or {}
    result = transcribe_with_whisper_local(
        audio_path=info_data.get('audio_path'),
        model_size=info_data.get('model_size',"tiny"),
        use_silence=info_data.get('use_silence'),
        info_data=info_data.get('info_data'))
    info_data['whisper_result'] = result
    return info_data
def analyze_video_text_data(info_data=None,**kwargs):
    info_data = info_data or {}
    result = analyze_video_text(video_path=info_data.get('video_path'),
        directory=info_data.get('thumbnails_directory'),
        image_texts=info_data.get('video_text',[]),
        remove_phrases=info_data.get('remove_phrases',[]),
        video_id=info_data.get('video_id'),
        frame_interval=info_data.get('frame_interval'))
    info_data['video_text'] = result
    return info_data
def get_initial_info_data(video_path=None,info_dir=None):
    keys = ['video_path',
            'basename',
            'filename',
            'ext',
            'title',
            'video_id',
            'info_dir',
            'info_path',
            'parent_directory',
            'audio_path',
            'thumbnails_directory',
            'uploader',
            'domain',
            'videos_url',
            'canonical_url',
            'remove_phrases',
            'categories',
            'videos_url',
            'repository_dir',
            'directory_links',
            'videos_dir',
            'infos_dir',
            'base_url',
            'model_size',
            'language']
    info = {'video_path':video_path}
    info['video_id'] = generate_file_id(video_path)
    info['info_dir'] = make_dirs(get_video_info_dir(**info))
    info['info_path'] = get_video_info_path(**info)
    info_data = get_video_info_data(**info)
    new_data,info_data = get_key_vars(keys,info_data=info_data,data=info)
    
    return info_data

def extract_audio_from_video_call(req=None,info_data=None):
    keys = ['audio_path',
            'video_path']
    new_data = {}
    for key in keys:
        new_data[key] = info_data.get(key)
        if not new_data[key]:
            if key == 'audio_path':
                new_data[key] = get_audio_path(**all_data)
            elif key == 'video_path':
                new_data[key] = all_data.get('video_path')
    extract_audio_from_video(**new_data)
    return info_data

def transcribe_with_wisper_call(req=None,info_data=None):
    keys = ['audio_path',
            'model_size',
            'language',
            'use_silence',
            'info_data']
    bool_key = 'whisper_result'
    function = transcribe_with_whisper_local_data
    info_data = execute_if_bool(bool_key,function,keys,req=req,info_data=info_data)
    return info_data


def analyze_video_text_call(req=None,info_data=None):
    keys = ['video_path',
            'thumbnails_directory',
            'info_data',
            'remove_phrases',
            'video_id']
    bool_key = 'video_text'
    function = analyze_video_text_data
    info_data = execute_if_bool(bool_key,function,keys,req=req,info_data=info_data)
    return info_data

def refine_keywords_call(req=None,info_data=None):
    keys = ['keywords',
            'full_text',
            'info_data']
    bool_key = 'combined_keywords'
    function = refine_keywords
    info_data = execute_if_bool(bool_key,function,keys,req=req,info_data=info_data)
    return info_data

def get_summary_call(req=None,info_data=None):
    keys = ['keywords',
            'full_text',
            'info_data']
    bool_key = 'summary'
    function = get_summary_data
    info_data = execute_if_bool(bool_key,function,keys,info_data=info_data)
    return info_data
def get_seo_data_call(req=None,info_data=None):
    keys = ['uploader',
            'domain',
            'categories',
            'videos_url',
            'repository_dir',
            'directory_links',
            'videos_dir',
            'infos_dir',
            'base_url',
            'generator',
            'LEDTokenizer',
            'LEDForConditionalGeneration',
            'info_data']
    bool_key = 'seo_description'
    function = get_seo_data
    info_data = execute_if_bool(bool_key,function,keys,info_data=info_data)
    return info_data

def get_all_info_data_call(video_path,info_dir=None):
    info_data = get_initial_info_data(video_path=video_path,info_dir=info_dir)
    info_data = extract_audio_from_video_call(info_data = info_data)
    info_data = transcribe_with_wisper_call(info_data = info_data)
    info_data = analyze_video_text_call(info_data = info_data)
    info_data['full_text'] = info_data.get('whisper_result',{}).get('text')
    info_data = refine_keywords_call(info_data = info_data)
    info_data = get_summary_call(info_data = info_data)
    info_data = get_seo_data_call(info_data = info_data)
    return info_data
