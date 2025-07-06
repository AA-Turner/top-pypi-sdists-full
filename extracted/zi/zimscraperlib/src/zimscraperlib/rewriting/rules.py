# THIS IS AN AUTOMATICALLY GENERATED FILE, DO NOT MODIFY DIRECTLY

FUZZY_RULES = [
  {
    "pattern": r".*googlevideo.com/(videoplayback(?=\?)).*[?&](id=[^&]+).*",
    "replace": r"youtube.fuzzy.replayweb.page/\1?\2",
  },
  {
    "pattern": r"(?:www\.)?youtube(?:-nocookie)?\.com/(get_video_info\?).*(video_id=[^&]+).*",
    "replace": r"youtube.fuzzy.replayweb.page/\1\2",
  },
  {
    "pattern": r"i\.ytimg\.com\/vi\/(.*?)\/.*?\.(\w*?)(?:\?.*|$)",
    "replace": r"i.ytimg.com.fuzzy.replayweb.page/vi/\1/thumbnail.\2",
  },
  {
    "pattern": r"([^?]+)\?[\d]+$",
    "replace": r"\1",
  },
  {
    "pattern": r"(?:www\.)?youtube(?:-nocookie)?\.com\/(youtubei\/[^?]+).*(videoId[^&]+).*",
    "replace": r"youtube.fuzzy.replayweb.page/\1?\2",
  },
  {
    "pattern": r"(?:www\.)?youtube(?:-nocookie)?\.com/embed/([^?]+).*",
    "replace": r"youtube.fuzzy.replayweb.page/embed/\1",
  },
  {
    "pattern": r".*(?:gcs-vimeo|vod|vod-progressive|vod-adaptive)\.akamaized\.net.*\/(.+?.mp4)\?.*range=(.*?)(?:&.*|$)",
    "replace": r"vimeo-cdn.fuzzy.replayweb.page/\1?range=\2",
  },
  {
    "pattern": r".*(?:gcs-vimeo|vod|vod-progressive)\.akamaized\.net.*?\/([\d/]+.mp4)$",
    "replace": r"vimeo-cdn.fuzzy.replayweb.page/\1",
  },
  {
    "pattern": r".*player.vimeo.com\/(video\/[\d]+)\?.*",
    "replace": r"vimeo.fuzzy.replayweb.page/\1",
  },
  {
    "pattern": r".*i\.vimeocdn\.com\/(.*)\?.*",
    "replace": r"i.vimeocdn.fuzzy.replayweb.page/\1",
  },
  {
    "pattern": r"cheatography\.com\/scripts\/(.*).js.*[?&](v=[^&]+).*",
    "replace": r"cheatography.com.fuzzy.replayweb.page/scripts/\1.js?\2",
  },
  {
    "pattern": r"blogger.googleusercontent.com\/img\/(.*\.jpg)=.*",
    "replace": r"blogger.googleusercontent.com.fuzzy.replayweb.page/img/\1.resized",
  },
  {
    "pattern": r"(iranwire\.com\/questions\/detail\/.*)\?.*",
    "replace": r"\1",
  },

]
