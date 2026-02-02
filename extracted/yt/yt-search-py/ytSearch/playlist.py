import copy
import json
import re
from typing import Dict, Any, Union, Optional
from urllib.parse import urlencode

from ytSearch.core.requests import RequestCore
from ytSearch.core.constants import *


class PlaylistCore(RequestCore):
    """Core class for playlist operations"""
    
    def __init__(self, playlistLink: str, componentMode: str, timeout: int = 2):
        super().__init__()
        self.playlistLink = playlistLink
        self.componentMode = componentMode  # None, 'getInfo', or 'getVideos'
        self.timeout = timeout
        self.continuationKey = None
        self.playlistComponent = None
        self.response = None
        self.responseSource = None
        
    def _extractPlaylistId(self) -> str:
        """Extract playlist ID from URL"""
        match = re.search(r"(?<=list=)([a-zA-Z0-9+/=_-]+)", self.playlistLink)
        if not match:
            raise Exception('ERROR: Invalid playlist link.')
        return match.group()
    
    def _prepareFirstRequest(self):
        """Prepare the initial request"""
        playlistId = self._extractPlaylistId()
        browseId = "VL" + playlistId if not playlistId.startswith("VL") else playlistId
        
        self.url = 'https://www.youtube.com/youtubei/v1/browse' + '?' + urlencode({
            'key': searchKey,
        })
        
        requestBody = copy.deepcopy(requestPayload)
        requestBody['browseId'] = browseId
        self.data = requestBody
    
    def _prepareNextRequest(self):
        """Prepare continuation request for more videos"""
        requestBody = copy.deepcopy(requestPayload)
        requestBody['continuation'] = self.continuationKey
        self.data = requestBody
        self.url = 'https://www.youtube.com/youtubei/v1/browse' + '?' + urlencode({
            'key': searchKey,
        })
    
    async def _makeAsyncRequest(self) -> None:
        """Make async request to YouTube API"""
        request = await self.asyncPostRequest()
        if request.status_code == 200:
            self.response = request.text
        else:
            raise Exception(f'ERROR: Invalid status code {request.status_code}.')
    
    def _parseSource(self) -> None:
        """Parse JSON response"""
        try:
            self.responseSource = json.loads(self.response)
        except:
            raise Exception('ERROR: Could not parse YouTube response.')
    
    def _getValue(self, source: dict, path: list) -> Union[str, int, dict, list, None]:
        """Navigate nested dictionary with path"""
        value = source
        for key in path:
            if value is None:
                return None
            if isinstance(key, str):
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    return None
            elif isinstance(key, int):
                if isinstance(value, list) and len(value) > abs(key):
                    value = value[key]
                else:
                    return None
        return value
    
    def _getComponents(self) -> None:
        """Extract playlist info and videos from response"""
        try:
            # Get sidebar for playlist info
            sidebar = self._getValue(self.responseSource, ["sidebar", "playlistSidebarRenderer", "items"])
            if not sidebar:
                raise Exception('ERROR: Could not find playlist sidebar.')
            
            infoRenderer = self._getValue(sidebar, [0, "playlistSidebarPrimaryInfoRenderer"])
            channel_details_available = len(sidebar) > 1
            channelRenderer = self._getValue(sidebar, [1, "playlistSidebarSecondaryInfoRenderer", "videoOwner", "videoOwnerRenderer"]) if channel_details_available else None
            
            # Get video list
            videoRenderer = self._getValue(self.responseSource, [
                "contents", "twoColumnBrowseResultsRenderer", "tabs", 0, "tabRenderer",
                "content", "sectionListRenderer", "contents", 0, "itemSectionRenderer",
                "contents", 0, "playlistVideoListRenderer", "contents"
            ])
            
            videos = []
            if videoRenderer:
                for video in videoRenderer:
                    if "playlistVideoRenderer" in video:
                        v = video["playlistVideoRenderer"]
                        videoData = {
                            "id": self._getValue(v, ["videoId"]),
                            "title": self._getValue(v, ["title", "runs", 0, "text"]),
                            "thumbnails": self._getValue(v, ["thumbnail", "thumbnails"]),
                            "duration": self._getValue(v, ["lengthText", "simpleText"]),
                            "channel": {
                                "name": self._getValue(v, ["shortBylineText", "runs", 0, "text"]),
                                "id": self._getValue(v, ["shortBylineText", "runs", 0, "navigationEndpoint", "browseEndpoint", "browseId"]),
                            },
                            "isPlayable": self._getValue(v, ["isPlayable"]),
                        }
                        if videoData["id"]:
                            videoData["link"] = f"https://www.youtube.com/watch?v={videoData['id']}"
                        if videoData["channel"]["id"]:
                            videoData["channel"]["link"] = f"https://www.youtube.com/channel/{videoData['channel']['id']}"
                        videos.append(videoData)
                    elif "continuationItemRenderer" in video:
                        self.continuationKey = self._getValue(video, ["continuationItemRenderer", "continuationEndpoint", "continuationCommand", "token"])
            
            # Build playlist info
            playlistInfo = {
                "id": self._extractPlaylistId(),
                "title": self._getValue(infoRenderer, ["title", "runs", 0, "text"]),
                "thumbnails": self._getValue(infoRenderer, ["thumbnailRenderer", "playlistVideoThumbnailRenderer", "thumbnail", "thumbnails"]),
                "videoCount": self._getValue(infoRenderer, ["stats", 0, "runs", 0, "text"]),
                "viewCount": self._getValue(infoRenderer, ["stats", 1, "simpleText"]),
                "link": self._getValue(self.responseSource, ["microformat", "microformatDataRenderer", "urlCanonical"]),
            }
            
            if channel_details_available and channelRenderer:
                playlistInfo["channel"] = {
                    "name": self._getValue(channelRenderer, ["title", "runs", 0, "text"]),
                    "id": self._getValue(channelRenderer, ["title", "runs", 0, "navigationEndpoint", "browseEndpoint", "browseId"]),
                    "thumbnails": self._getValue(channelRenderer, ["thumbnail", "thumbnails"]),
                }
                if playlistInfo["channel"]["id"]:
                    playlistInfo["channel"]["link"] = f"https://www.youtube.com/channel/{playlistInfo['channel']['id']}"
            
            # Set component based on mode
            if self.componentMode == "getInfo":
                self.playlistComponent = playlistInfo
            elif self.componentMode == "getVideos":
                self.playlistComponent = {"videos": videos}
            else:
                self.playlistComponent = {
                    "info": playlistInfo,
                    "videos": videos
                }
                
        except Exception as e:
            raise Exception(f'ERROR: Could not extract playlist components: {str(e)}')
    
    def _getNextComponents(self) -> None:
        """Extract videos from continuation response"""
        try:
            continuationElements = self._getValue(self.responseSource, [
                'onResponseReceivedActions', 0, 'appendContinuationItemsAction', 'continuationItems'
            ])
            
            if not continuationElements:
                return
            
            videos = []
            self.continuationKey = None
            
            for videoElement in continuationElements:
                if "playlistVideoRenderer" in videoElement:
                    v = videoElement["playlistVideoRenderer"]
                    videoData = {
                        "id": self._getValue(v, ["videoId"]),
                        "title": self._getValue(v, ["title", "runs", 0, "text"]),
                        "thumbnails": self._getValue(v, ["thumbnail", "thumbnails"]),
                        "duration": self._getValue(v, ["lengthText", "simpleText"]),
                        "channel": {
                            "name": self._getValue(v, ["shortBylineText", "runs", 0, "text"]),
                            "id": self._getValue(v, ["shortBylineText", "runs", 0, "navigationEndpoint", "browseEndpoint", "browseId"]),
                        },
                        "isPlayable": self._getValue(v, ["isPlayable"]),
                    }
                    if videoData["id"]:
                        videoData["link"] = f"https://www.youtube.com/watch?v={videoData['id']}"
                    if videoData["channel"]["id"]:
                        videoData["channel"]["link"] = f"https://www.youtube.com/channel/{videoData['channel']['id']}"
                    videos.append(videoData)
                elif "continuationItemRenderer" in videoElement:
                    self.continuationKey = self._getValue(videoElement, ["continuationItemRenderer", "continuationEndpoint", "continuationCommand", "token"])
            
            # Append to existing videos or create new list
            if isinstance(self.playlistComponent, dict):
                if "videos" in self.playlistComponent:
                    self.playlistComponent["videos"].extend(videos)
                else:
                    self.playlistComponent = {"videos": videos}
            else:
                self.playlistComponent = {"videos": videos}
                
        except Exception as e:
            raise Exception(f'ERROR: Could not extract continuation components: {str(e)}')
    
    async def _asyncCreate(self):
        """Initial async request"""
        self._prepareFirstRequest()
        await self._makeAsyncRequest()
        self._parseSource()
        self._getComponents()
    
    async def _asyncNext(self):
        """Fetch next page of videos"""
        if not self.continuationKey:
            # First call
            await self._asyncCreate()
        else:
            # Continuation
            self._prepareNextRequest()
            await self._makeAsyncRequest()
            self._parseSource()
            self._getNextComponents()


class Playlist:
    """
    Fetches information and videos for a given playlist link.
    
    The information of the playlist can be accessed in the `info` field.
    The retrieved videos are in the `videos` field as a list.
    
    Call `getNextVideos()` to fetch more videos (up to 100 at a time).
    `hasMoreVideos` indicates if more videos can be fetched.
    
    Args:
        playlistLink (str): Link to the YouTube playlist.
        
    Examples:
        >>> playlist = Playlist('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
        >>> await playlist.getNextVideos()
        >>> print(f'Videos: {len(playlist.videos)}')
    """
    
    def __init__(self, playlistLink: str, timeout: int = 2):
        self.playlistLink = playlistLink
        self.timeout = timeout
        self.videos = []
        self.info = None
        self.hasMoreVideos = True
        self._playlist = None
    
    async def getNextVideos(self) -> None:
        """Fetch more videos and append to the videos list."""
        if not self._playlist:
            self._playlist = PlaylistCore(self.playlistLink, None, self.timeout)
            await self._playlist._asyncNext()
            
            if isinstance(self._playlist.playlistComponent, dict):
                self.info = copy.deepcopy(self._playlist.playlistComponent.get("info", {}))
                self.videos = self._playlist.playlistComponent.get("videos", [])
                self.hasMoreVideos = self._playlist.continuationKey is not None
        else:
            await self._playlist._asyncNext()
            if isinstance(self._playlist.playlistComponent, dict):
                new_videos = self._playlist.playlistComponent.get("videos", [])
                self.videos.extend(new_videos)
                self.hasMoreVideos = self._playlist.continuationKey is not None
    
    @staticmethod
    async def get(playlistLink: str, timeout: int = 2) -> Optional[Dict[str, Any]]:
        """
        Fetch full playlist information including videos.
        
        Args:
            playlistLink (str): Link to the YouTube playlist.
            timeout (int): Request timeout in seconds.
            
        Returns:
            Dict with 'info' and 'videos' keys, or None if unavailable.
            
        Examples:
            >>> result = await Playlist.get('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
            >>> print(result['info']['title'])
        """
        try:
            playlist = PlaylistCore(playlistLink, None, timeout)
            await playlist._asyncCreate()
            return playlist.playlistComponent
        except:
            return None
    
    @staticmethod
    async def getInfo(playlistLink: str, timeout: int = 2) -> Optional[Dict[str, Any]]:
        """
        Fetch only playlist information (no videos).
        
        Args:
            playlistLink (str): Link to the YouTube playlist.
            timeout (int): Request timeout in seconds.
            
        Returns:
            Dict with playlist info, or None if unavailable.
            
        Examples:
            >>> info = await Playlist.getInfo('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
            >>> print(info['title'])
        """
        try:
            playlist = PlaylistCore(playlistLink, "getInfo", timeout)
            await playlist._asyncCreate()
            return playlist.playlistComponent
        except:
            return None
    
    @staticmethod
    async def getVideos(playlistLink: str, timeout: int = 2) -> Optional[Dict[str, Any]]:
        """
        Fetch only playlist videos (no info).
        
        Args:
            playlistLink (str): Link to the YouTube playlist.
            timeout (int): Request timeout in seconds.
            
        Returns:
            Dict with 'videos' key containing video list, or None if unavailable.
            
        Examples:
            >>> result = await Playlist.getVideos('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
            >>> print(f'Found {len(result["videos"])} videos')
        """
        try:
            playlist = PlaylistCore(playlistLink, "getVideos", timeout)
            await playlist._asyncCreate()
            return playlist.playlistComponent
        except:
            return None
