# src/pipeline.py
from .imports import *
get_video_record

def get_thumbnails(video_id: str, video_path: str, thumbnails_path: str):
    """
    Extract thumbnails + OCR → persist into DB JSON.
    """
##    print(f"video_id=={video_id}\nvideo_path=={video_path}\nthumbnails_path={thumbnails_path}")
    paths = extract_video_frames_unique(video_path, thumbnails_path, video_id=video_id)
    texts = [ocr_image(p) for p in paths]
    thumbnails = {"paths": paths, "texts": texts}
    upsert_video(video_id, thumbnails=thumbnails)
    return thumbnails

def get_video_id_from_vars(url=None,video_id=None,video_path=None):
    if video_id:
        return video_id
    video_id =   get_video_id(
        url=url,
        video_id=video_id,
        video_path=video_path)
    if video_id:
        return video_id
    if url:
        video_id = get_video_id(url)
    if video_id:
        return video_id
    if video_path:
        path_parts = [part for part in video_path.split(VIDEOS_ROOT_DEFAULT)[-1].split('/') if part]
        if path_parts:
            video_id = path_parts[0]
        if not video_id:
            video_id = generate_video_id(video_path)
    return video_id
def get_video_path_from_vars(url=None,video_id=None,video_path=None):
    if video_path:
        return video_path

    video_id = get_video_id_from_vars(url=url,video_id=video_id,video_path=video_path)
    video_path = os.path.join(VIDEOS_ROOT_DEFAULT,video_id,'video.mp4')
    return video_path
def get_video_url_from_vars(url=None,video_id=None,video_path=None):
    if url:
        return url
    video_info = get_video_info(
        url=url,
        video_id=video_id,
        video_path=video_path)
    for key in ['original_url','webpage_url']:
        url = make_list(get_any_value(video_info,key) or None)[0]
        if url:
            return url
    return url
def get_all_meadata(video_id,data):
    base_url = "https://clownworld.biz"
    record = get_video_record(video_id)
    video_info = record.get("info") or {}
    directory = video_info.get("directory")
    meta_file_path = os.path.join(directory, "meta.json")
    metadict = build_seo_meta_from_result(data, base_url=base_url)
    # Make sure all paths inside metadict are URL-style before saving
    metadict_public = convert_paths_to_urls(metadict, base_url=base_url)
    upsert_video(video_id, metatags=metadict_public)
    safe_dump_to_json(data=metadict_public, file_path=meta_file_path)
    return metadict_public
def search_keys_nested(data, query, path=None, results=None):
    """
    Search all dictionary keys (recursively) for matches to `query`
    and categorize results by the branch where they occur.

    Returns:
        {
            "a.b.c": ["matching_key1", "matching_key2"],
            ...
        }
    """
    if results is None:
        results = {}

    if path is None:
        path = []

    if not isinstance(data, dict):
        return results

    for key, value in data.items():
        current_path = path + [key]

        # Check if key matches the search text
        if query.lower() in key.lower():
            branch = ".".join(path) or "<root>"
            results.setdefault(branch, []).append(key)

        # Recurse into dicts
        if isinstance(value, dict):
            search_keys_nested(value, query, current_path, results)

        # Recurse into lists of dicts
        elif isinstance(value, list):
            for idx, item in enumerate(value):
                if isinstance(item, dict):
                    list_path = current_path + [f"[{idx}]"]
                    search_keys_nested(item, query, list_path, results)

    return results
def get_key_from_dict(comp_key,dict_obj):
    if not comp_key:
        return 
    keys = list(dict_obj.keys())
    if comp_key in keys:
        return comp_key
    for key in keys:
        if comp_key in key:
            return key
    result = search_keys_nested(get_dict_example(), comp_key)
    collect_vals = {}
    all_keys = []
    for key,values in result.items():
        key_head = key.split('.')[0]
        if key_head not in collect_vals:
            collect_vals[key_head]={}
        for value in values:
           if value not in collect_vals[key_head]:
               collect_vals[key_head][value] = 0
               all_keys.append(value)
           collect_vals[key_head][value]+=1
    
    highest = [0,None]
    closest_match = get_closest_match_from_list(comp_key,all_keys)
    for main_key,keys in collect_vals.items():

        count = keys.get(closest_match)
        if count != None and (highest[-1] == None or count > highest[0]):
            highest = [count,main_key]
  
    return highest[-1]
            
