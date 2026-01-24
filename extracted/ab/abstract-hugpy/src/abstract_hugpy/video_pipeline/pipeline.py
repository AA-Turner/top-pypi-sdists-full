# src/pipeline.py
from .pipeline_utils import *


class VideoPipeline:
    def __init__(
        self,
        video_url: str | None = None,
        video_id: str | None = None,
        video_path: str | None = None,
        force_refresh: bool = False,
        videoId: str | None = None,
    ):

        # 1) Normalize inputs
        self.video_url = video_url
        self.video_path = video_path
        self.video_id = video_id or videoId
##        logger.info(f"running VideoPipeline with self.video_id = {self.video_id} self.video_url = {self.video_url} self.video_path = {self.video_path}")

        # 2) Normalize URL first (strip &t, mobile variants, etc.)
        if self.video_url:
            self.video_url = get_corrected_url(self.video_url)
##        logger.info(f"self.video_url == {self.video_url}")

        # 3) Compute a solid video_id BEFORE we hit the registry
        #    Use your helper that knows how to look at URL / video_path.
        self.video_id = get_video_id_from_vars(
            url=self.video_url,
            video_id=self.video_id,
            video_path=self.video_path,
        )
##        logger.info(f"running elf.registry with self.video_id = {self.video_id} self.video_url = {self.video_url} self.video_path = {self.video_path}")

        # As a final fallback: generate an ID so we never have None
        if not self.video_id:
            if self.video_path:
                self.video_id = generate_video_id(self.video_path)
            elif self.video_url:
                # deterministic from URL so we don’t collide
                self.video_id = generate_video_id(self.video_url)
            else:
                # absolute last resort, random-ish ID
                self.video_id = generate_video_id("no_input")
        
        # 4) Now we can talk to the registry safely
        self.registry = infoRegistry()
##        logger.info(f"running elf.registry with self.video_id = {self.video_id} self.video_url = {self.video_url} self.video_path = {self.video_path}")
        self.info = (
            self.registry.get_video_info(
                url=self.video_url,
                video_id=self.video_id,
                video_path=self.video_path,
                force_refresh=force_refresh,
            )
            or {}
        )

        self.video_info = self.info.get("info") or {}

        # 5) Once we have info, refine paths/urls if needed
        self.video_path = get_video_path_from_vars(
            url=self.video_url,
            video_id=self.video_id,
            video_path=self.video_path,
        )
        logger.info(f"self.video_path == {self.video_path}")
        self.video_url = get_video_url_from_vars(
            url=self.video_url,
            video_id=self.video_id,
            video_path=self.video_path,
        )
        logger.info(f"self.video_url == {self.video_url}")
    def get_video_info(self):
        
        video_info =  get_video_info(
            url=self.video_url,
            video_id=self.video_id,
            video_path=self.video_path,
            registry=self.registry,
            download_video=False,
        )
        return video_info
    def download_video(self):
        
        video_info = downloadvideo(
            url=self.video_url,
            registry=self.registry,
            download_video=True,
        )
        return video_info
    def get_file_path(self, key: str):
        """
        Safely fetch a path from self.video_info and tell whether it exists on disk.
        """
        path = self.video_info.get(key)
        if not path:
            logger.info(f"{key} is empty or missing in video_info")
            return None, False

        exists = os.path.isfile(path)
        isexist = "exists" if exists else "does not exist"
        logger.info(f"{key} is {path} and {isexist}")
        return path, exists
    # === CAPTIONS ===
    def get_rawdata(self):
        record = get_video_record(self.video_id) or {}
        rawdata = record.get("rawdata")
        if record and rawdata:
            return record["rawdata"]
        video_info = record.get("info") or {}
        video_url = self.video_url
        directory = video_info.get("directory")
##        outtmpl = os.path.join(directory, "video.%(ext)s")
##        with yt_dlp.YoutubeDL(build_ydl_opts(outtmpl)) as ydl:
##            rawdata = ydl.extract_info(video_url, download=False)
        logger.info(f"running get_rawdata with video_info = {video_info} video_url = {video_url} directory = {directory}")
        logger.info(f"running get_rawdata with video_info = {video_info} self.video_url = {self.video_url} directory = {directory}")
        rawdata = get_video_info(url=video_url,directory=directory)
        upsert_video(self.video_id, rawdata=rawdata)
        return rawdata
    # === AUDIO ===
    def ensure_audio(self):
        record = get_video_record(self.video_id) or {}

        audio_path, exists = self.get_file_path("audio_path")
        if record and audio_path and exists:
            audio_format = audio_path.split(".")[-1]
            return audio_path, audio_format

        # Need to (re)create audio
        self.download_video()
        video_path, v_exists = self.get_file_path("video_path")
        if not video_path or not v_exists:
            raise RuntimeError(f"Video file not found for {self.video_id}")

        # Choose a sensible default audio file name if missing
        if not audio_path:
            base, _ = os.path.splitext(video_path)
            audio_path = base + ".wav"

        os.system(
            f"ffmpeg -y -i {video_path} -vn -acodec pcm_s16le -ar 16000 -ac 1 {audio_path}"
        )
        audio_format = audio_path.split(".")[-1]

        upsert_video(self.video_id, audio_path=audio_path, audio_format=audio_format)
        return audio_path, audio_format

    # === WHISPER ===
    def get_whisper(self):
        record = get_video_record(self.video_id) or {}
        whisper_result = record.get("whisper")

        if record and whisper_result:
            return whisper_result

        audio_path, fmt = self.ensure_audio()
        result = whisper_transcribe(audio_path)

        upsert_video(self.video_id, whisper=result)
        return result

    # === CAPTIONS ===
    def get_captions(self):
        record = get_video_record(self.video_id) or {}
        if record and record.get("captions"):
            return record["captions"]

        whisper = self.get_whisper()
        captions = [
            {"start": seg["start"], "end": seg["end"], "text": seg["text"]}
            for seg in whisper.get("segments", [])
        ]

        upsert_video(self.video_id, captions=captions)
        return captions

    # === METADATA ===
    def get_metadata(self):
        record = get_video_record(self.video_id) or {}
        if record and record.get("metadata"):
            return record["metadata"]

        whisper = self.get_whisper()
        captions = self.get_captions()

        text_blob = " ".join([whisper.get("text", "")] + [c["text"] for c in captions])
        title = (
            self.info.get("title")
            or self.video_info.get("title")
            or text_blob[:50]
            or "Untitled"
        )
        summary = get_summarizer_summary(text=text_blob)

        keywords = self.info.get("keywords") or self.video_info.get("keywords") or []
        tags = self.info.get("tags") or self.video_info.get("tags") or []
        extracted_keywords = get_extracted_keywords(text=text_blob) or []
        keywords = make_list(keywords + tags + extracted_keywords)

        category = classify_category(make_list(keywords),title=title,description=summary)
        if len(keywords) >= 10:
            keywords = keywords[:10]

        metadata = {
            "title": title,
            "summary": summary,
            "category": category,
            "keywords": keywords,
        }

        upsert_video(self.video_id, metadata=metadata)
        return metadata

    # === THUMBNAILS ===
    def get_thumbnails(self):
        record = get_video_record(self.video_id) or {}
        if record and record.get("thumbnails"):
            return record["thumbnails"]

        self.download_video()
        video_id = self.video_id
        video_path = self.video_info.get("video_path")
        thumbnails_dir = self.video_info.get("thumbnails_directory")
        
        thumbnails = get_thumbnails(video_id, video_path, thumbnails_dir)
        upsert_video(self.video_id, thumbnails=thumbnails)
        return thumbnails

    # === SEODATA ===
    def get_seodata(self):
        record = get_video_record(self.video_id) or {}
        if record and record.get("seodata"):
            return record["seodata"]
        
        dl = VideoDownloader(url=self.video_url, download_video=True)
        whisper_result = self.get_whisper()
        captions = self.get_captions()

        thumbnails = self.get_thumbnails()
        thumbnails_dir = self.video_info.get("thumbnails_directory")
        thumbnails_paths = thumbnails.get("paths")
        
        metadata = self.get_metadata()
        title = metadata.get("title")
        summary = metadata.get("summary")
        keywords = metadata.get("keywords")
        description = metadata.get("description", summary)

        video_id = self.video_id
        video_path = self.video_info.get("video_path")
        if not (video_path and os.path.isfile(video_path)):
            file_map = get_file_map(video_path, types="video")
            video_paths = file_map.get("video")
            if video_paths:
                video_path = video_paths[0]

        audio_path = self.video_info.get("audio_path")
        if not (audio_path and os.path.isfile(audio_path)):
            file_map = get_file_map(video_path, types="audio")
            audio_paths = file_map.get("audio")
            if audio_paths:
                audio_path = audio_paths[0]

        seodata = get_seo_data(
            video_path=video_path,
            filename=video_id,
            title=title,
            summary=summary,
            description=description,
            keywords=keywords,
            thumbnails_dir=thumbnails_dir,
            thumbnail_paths=thumbnails_paths,
            whisper_result=whisper_result,
            audio_path=audio_path,
            domain="clownworld.biz",
        )

        # Store raw seodata (filesystem paths), frontend will get URL-converted
        upsert_video(self.video_id, seodata=seodata)
        return seodata

    # === AGGREGATED ===
    def get_aggregated_data(self):
        record = get_video_record(self.video_id) or {}
        if record and record.get("aggregated"):
            return record["aggregated"]

        video_info = record.get("info") or {}
        directory = video_info.get("directory")
        aggregated = aggregate_from_base_dir(directory=directory)

        upsert_video(self.video_id, aggregated=aggregated)
        return aggregated

    # === METATAGS / META.JSON ===
    def get_meta_tags(self):
        """
        Build meta tags, persist them, and return a version where
        all filesystem/static paths are converted to public URLs.
        """
        record = get_video_record(self.video_id) or {}
        if record and record.get("metatags"):
            return record["metatags"]
        data = self.get_all_data()
        return get_all_meadata(video_id = self.video_id,data = data)
    # === METATAGS / META.JSON ===
    def get_json_page(self):
        """
        Build meta tags, persist them, and return a version where
        all filesystem/static paths are converted to public URLs.
        """
        record = get_video_record(self.video_id) or {}
        if record and record.get("pagedata"):
            return record["pagedata"]

        video_info = record.get("info") or {}
        directory = video_info.get("directory")
        video_url = video_info.get("video_url")
        self.get_meta_tags()
        pagedata = build_page_json(directory=directory,video_url = video_url,source_video_url = video_url)
        
        return pagedata
    # === METATAGS / META.JSON ===
    def get_extract_fields(self):
        """
        Build meta tags, persist them, and return a version where
        all filesystem/static paths are converted to public URLs.
        """
        extractfields = {}
        record = get_video_record(self.video_id) or {}
        video_info = record.get("info") or {}
        directory = video_info.get("directory")
        video_path = f"{directory}/video.mp4"
        video_id = str(self.video_id)
        basename = os.path.basename(video_path)
        filename,ext = os.path.splitext(basename)
        original_url = video_info.get("original_url") or self.video_url or video_info.get("video_url") 
        clownworld_video_url = f"https://clownworld.biz/videos/{video_id}/video.mp4"
        share_url = f"https://clownworld.biz/videos/?video_id={video_id}"
        video_url = original_url
        if is_file(video_path):
            video_url = clownworld_video_url
        extractfields["videoId"] = video_id
        extractfields["video_id"] = video_id
        extractfields["original_url"] = original_url
        extractfields["video_url"] = video_url
        extractfields["optimized_video_url"] = video_url
        extractfields["share_url"] =share_url
        info = self.get_info()
        for key in ["pagedata","metatags","seodata","thumbnails","metadata","rawdata"]:
            values = info.get(key)
            if values and isinstance(values,dict):
                nufields = [get_values(STRINGS_VARS,values) or {},extract_video_fields(values) or {}]
                for nufield in nufields:
                    for fkey,fval in nufield.items():
                            extractfields[fkey] = extractfields.get(fkey) or fval
        info.update(extractfields)
        meadata =  get_all_meadata(video_id=video_id,data=info)
        pagedata = build_page_json(directory=directory,video_url = video_url)
        extractfields['pagedata']=pagedata
        return extractfields
    # === INFO / ALL ===
    def get_info(self):
        self.get_rawdata()
        return get_video_record(self.video_id, hide_audio=True) or {}
    # === INFO / ALL ===
    def get_video_url(self):
        rawdata = self.get_rawdata()
        record = get_video_record(self.video_id, hide_audio=True) or {}
        return self.video_url or record.get('video_url') or record.get("info").get('original_url')
        # === INFO / ALL ===
    def get_video_id(self):
        rawdata = self.get_rawdata()
        
        return self.video_id or record.get('video_id') or generate_video_id(self.video_url) or generate_video_id(self.video_path)
    def get_video_path(self):
        self.get_rawdata()
        return self.video_path or get_video_record(self.video_id, hide_audio=True) or {}
    def get_video_dir(self):
        video_path = self.get_video_path()
        if video_path:
            return os.path.dirname(video_path)

    def get_all_data(self):
        return {
            "info": self.get_info(),
            "rawdata": self.get_rawdata(),
            "whisper": self.get_whisper(),
            "captions": self.get_captions(),
            "metadata": self.get_metadata(),
            "thumbnails": self.get_thumbnails(),
            "seodata": self.get_seodata(),
            "aggregated": self.get_aggregated_data(),
        }

    def get_all(self):
        return {
            "info": self.get_info(),
            "rawdata": self.get_rawdata(),
            "whisper": self.get_whisper(),
            "captions": self.get_captions(),
            "metadata": self.get_metadata(),
            "thumbnails": self.get_thumbnails(),
            "seodata": self.get_seodata(),
            "aggregated": self.get_aggregated_data(),
            "metatags": self.get_meta_tags(),
            "pagedata": self.get_json_page(),
        }
##def append_key_value(values,value,all_keys):
##    if value not in all_keys:
##        values.append(value)
##        all_keys.append(value)
##    return values,all_keys        
##def add_to_values(key,values,all_keys=None):
##    js_values = []
##    all_keys=all_keys or []
##    js_values,all_keys  = append_key_value(js_values,key,all_keys)
##    for value in values:
##        js_values,all_keys  = append_key_value(js_values,value,all_keys)
##        values = value.split('_')
##        for value in values:
##            js_values,all_keys  = append_key_value(js_values,value,all_keys)
##    return js_values,all_keys
##def get_keys_js():
##    all_keys = []
##    all_js = {"all": ["all","all_data","get_all"],
##        "info": ["video_info"],
##        "id": ["video_id"],
##        "url": ["video_url"],
##        "raw":["raw","raw_data"],
##        "extract":["extract_fields"],
##        "download": ["download_video"],
##        "audio": ["extract_audio"],
##        "whisper": ["whisper"],
##        "captions": ["captions"],
##        "metadata": ["meta_data"],
##        "thumbnails": ["extract_fields"],
##        "seodata":["seo_data"],
##        "metatags": ["meta_tags"],
##        "pagedata":["page_data"]}
##    for key,values in all_js.items():
##        js_values,all_keys = add_to_values(key,values,all_keys=all_keys)
##        all_js[key] = js_values
##    input(all_js)
def get_pipeline_key(key):
    pipeline_key_map = {'all': ['all', 'all_data', 'data', 'get_all', 'get'],
     'info': ['info', 'video_info', 'video'],
     'id': ['id', 'video_id'],
     'url': ['url', 'video_url'],
     'path': ['path', 'video_path'],
     'dir': ['directory', 'video_directory','video_dir','dir'],
     'raw': ['raw', 'raw_data'],
     'extract': ['extract', 'extract_fields', 'fields'],
     'download': ['download', 'download_video'],
     'audio': ['audio', 'extract_audio'],
     'whisper': ['whisper'],
     'captions': ['captions'],
     'metadata': ['metadata', 'meta_data', 'meta'],
     'thumbnails': ['thumbnails'],
     'seodata': ['seodata', 'seo_data', 'seo'],
     'metatags': ['metatags', 'meta_tags', 'tags'],
     'pagedata': ['pagedata', 'page_data', 'page']
     }
    if key:
        if pipeline_key_map.get(key):
            return key
        for pipe_key,pipe_values in pipeline_key_map.items():
            if key in pipe_values:
                return pipe_key
    return "info"
def get_local_db_data(
    url: str=None,
    video_id: str=None,
    key: str | None = None,
    videoId: str=None,
    video_url: str=None,
    videoUrl: str=None,
    base_url: str = "https://clownworld.biz"
    ):
    url = url or video_url or videoUrl
    video_id = video_id or videoId
    
    p = VideoPipeline(video_url=url,video_id=video_id)
    if p.video_url == None and p.video_path == None:
        return
    pipeline_js = {
        "info": p.get_info,
        "id": p.get_video_id,
        "url": p.get_video_url,
        "path": p.get_video_path,
        "dir": p.get_video_dir,
        "rawdata": p.get_rawdata,
        "extractfields":p.get_extract_fields,
        "download": p.download_video,
        "audio": p.ensure_audio,
        "whisper": p.get_whisper,
        "captions": p.get_captions,
        "metadata": p.get_metadata,
        "thumbnails": p.get_thumbnails,
        "seodata": p.get_seodata,
        "metatags": p.get_meta_tags,
        "pagedata":p.get_json_page,
        "all": p.get_all,
    }
    
    
    def _call_and_convert(func):
        result = func
        if not isinstance(func,str):
            result = func()
        data = convert_paths_to_urls(result, base_url=base_url)
        return data
    if key:
        key = get_pipeline_key(key)
        func = pipeline_js.get(key)
        if func:
            return _call_and_convert(func)
    return _call_and_convert(p.get_all)
def get_pipeline_data(*args, **kwargs):
    engine = getHugpyDbEngine(*args, **kwargs)
    
    if not is_db_available(engine):
        url = "https://clownworld.biz/api/video/get_pipeline_data"
        return postRequest(url=url, data=kwargs)
    
    return get_local_db_data(*args, **kwargs)

    
