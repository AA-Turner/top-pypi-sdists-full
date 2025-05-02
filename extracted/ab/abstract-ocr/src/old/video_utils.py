from .functions import (VideoFileClip,
                        cv2,
                        os,
                        np,
                        math)
from .ocr_utils import extract_image_texts_from_directory
def clip_frames(items,initial=None,end=None):
    initial = initial or 35
    end = end or 35
    items_length = len(items)
    if items_length> initial:
        items = items[initial:]
    items_length = len(items)
    if items_length> end:
        items = items[:-end]
    return items
def pick_optimal_thumbnail(whisper_result, directory, *args,keywords=None,initial=None,end=None,**kwargs):
    scores = []
    keywords = keywords or []
    dirbase = os.path.basename(os.path.dirname(directory))
    image_files = sort_frames(directory=directory)
    image_files = clip_frames(image_files)
    first_image_file = image_files[0]
    thumb_name,thumb_ext = os.path.splitext(os.listdir(directory)[0])
    # Process each Whisper segment
    for segment in whisper_result["segments"]:
        text = segment["text"].lower().strip()
        start_time = segment["start"]        # Find the closest thumbnail based on start time
        frame_number = math.floor(start_time)
        thumbnail_name = f"{dirbase}_frame_{frame_number}{thumb_ext}"
        
        # Check if thumbnail exists
        if thumbnail_name not in thumbnails:
            continue
        
        # Score the caption
        keyword_score = sum(1 for kw in keywords if kw.lower() in text)
        clarity_score = 1 if len(text) > 20 else 0
        end_phrase_penalty = -1 if "thanks for watching" in text else 0
        total_score = keyword_score + clarity_score + end_phrase_penalty
        
        # Store thumbnail path, score, and caption
        thumbnail_path = os.path.join(directory, thumbnail_name)
        scores.append((thumbnail_path, total_score, text))
       
    # Sort by score (highest first)
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return scores[0] if scores else None
def pick_optimal_thumbnail_slim(video_text,
                           combined_keywords):
    scores = []
    for entry in video_text:
        
        text = entry['text'].lower()
        
        keyword_score = sum(1 for kw in combined_keywords if kw.lower() in text)
        
        clarity_score = 1 if len(text.strip()) > 20 else 0  # basic clarity check
        
        end_phrase_penalty = -1 if "thanks for watching" in text else 0
        
        total_score = keyword_score + clarity_score + end_phrase_penalty
        
        scores.append((entry['frame'],
                       total_score,
                       text.strip()))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return scores[0] if scores else None
def extract_video_frames(video_path,output_directory,frame_interval=None):
    frame_interval = frame_interval or = 1
    video = VideoFileClip(video_path)
    duration = video.duration
    for t in range(0, int(duration), frame_interval):
        frame_path = os.path.join(output_directory,f"{video_id}_frame_{t}.jpg")
        if not os.path.isfile(frame_path):
            frame = video.get_frame(t)
            cv2.imwrite(frame_path, cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR))
def analyze_video_text(video_path,
                       output_directory=None,
                       image_texts=None,
                       remove_phrases=None,
                       video_id=None,
                       frame_interval=None):
    if video_path == None or not video_path or not os.path.isfile(video_path):
        return image_texts
    remove_phrases=remove_phrases or []
    output_directory = output_directory or os.getcwd()
    
    extract_video_frames(video_path=video_path,
                          output_directory=output_directory,
                          frame_interval=frame_interval)
    image_texts = extract_image_texts_from_directory(output_directory=output_directory,
                                                     image_texts=image_texts,
                                                     remove_phrases=remove_phrases)
    
    return image_texts
def get_video_metadata(file_path):
    video = mp.VideoFileClip(file_path)
    
    metadata = {
        'resolution': f"{video.w}x{video.h}",
        'format': 'MP4',
        'file_size_mb': os.path.getsize(file_path) / (1024 * 1024)
    }
    
    video.close()
    return metadata
