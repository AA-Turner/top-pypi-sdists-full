from typing import List, Union
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import json
import copy

from ytSearch.core.constants import *


class ComponentHandler:
    def _getVideoComponent(self, element: dict, shelfTitle: str = None) -> dict:
        video = element[videoElementKey]
        component = {
            'type':                           'video',
            'id':                              self._getValue(video, ['videoId']),
            'title':                           self._getValue(video, ['title', 'runs', 0, 'text']),
            'publishedTime':                   self._getValue(video, ['publishedTimeText', 'simpleText']),
            'duration':                        self._getValue(video, ['lengthText', 'simpleText']),
            'viewCount': {
                'text':                        self._getValue(video, ['viewCountText', 'simpleText']),
                'short':                       self._getValue(video, ['shortViewCountText', 'simpleText']),
            },
            'thumbnails':                      self._getValue(video, ['thumbnail', 'thumbnails']),
            'richThumbnail':                   self._getValue(video, ['richThumbnail', 'movingThumbnailRenderer', 'movingThumbnailDetails', 'thumbnails', 0]),
            'descriptionSnippet':              self._getValue(video, ['detailedMetadataSnippets', 0, 'snippetText', 'runs']),
            'channel': {
                'name':                        self._getValue(video, ['ownerText', 'runs', 0, 'text']),
                'id':                          self._getValue(video, ['ownerText', 'runs', 0, 'navigationEndpoint', 'browseEndpoint', 'browseId']),
                'thumbnails':                  self._getValue(video, ['channelThumbnailSupportedRenderers', 'channelThumbnailWithLinkRenderer', 'thumbnail', 'thumbnails']),
            },
            'accessibility': {
                'title':                       self._getValue(video, ['title', 'accessibility', 'accessibilityData', 'label']),
                'duration':                    self._getValue(video, ['lengthText', 'accessibility', 'accessibilityData', 'label']),
            },
        }
        component['link'] = 'https://www.youtube.com/watch?v=' + component['id']
        if component['channel']['id'] : component['channel']['link'] = 'https://www.youtube.com/channel/' + component['channel']['id']
        component['shelfTitle'] = shelfTitle
        return component

    def _getChannelComponent(self, element: dict) -> dict:
        channel = element[channelElementKey]
        component = {
            'type':                           'channel',
            'id':                              self._getValue(channel, ['channelId']),
            'title':                           self._getValue(channel, ['title', 'simpleText']),
            'thumbnails':                      self._getValue(channel, ['thumbnail', 'thumbnails']),
            'videoCount':                      self._getValue(channel, ['videoCountText', 'runs', 0, 'text']),
            'descriptionSnippet':              self._getValue(channel, ['descriptionSnippet', 'runs']),
            'subscribers':                     self._getValue(channel, ['subscriberCountText', 'simpleText']),
        }
        component['link'] = 'https://www.youtube.com/channel/' + component['id']
        return component

    def _getPlaylistComponent(self, element: dict) -> dict:
        if playlistElementKey in element:
            playlist = element[playlistElementKey]
            component = {
                "type": "playlist",
                "id": self._getValue(playlist, ["playlistId"]),
                "title": self._getValue(playlist, ["title", "simpleText"]),
                "videoCount": self._getValue(playlist, ["videoCount"]),
                "channel": {
                    "name": self._getValue(
                        playlist, ["shortBylineText", "runs", 0, "text"]
                    ),
                    "id": self._getValue(
                        playlist,
                        [
                            "shortBylineText",
                            "runs",
                            0,
                            "navigationEndpoint",
                            "browseEndpoint",
                            "browseId",
                        ],
                    ),
                },
                "thumbnails": self._getValue(
                    playlist,
                    [
                        "thumbnailRenderer",
                        "playlistVideoThumbnailRenderer",
                        "thumbnail",
                        "thumbnails",
                    ],
                ),
            }
        elif "lockupViewModel" in element:
            lockup = element["lockupViewModel"]
            component = {
                "type": "playlist",
                "id": self._getValue(lockup, ["contentId"]),
                "title": self._getValue(
                    lockup,
                    ["metadata", "lockupMetadataViewModel", "title", "content"],
                ),
                "thumbnails": self._getValue(
                    lockup,
                    [
                        "contentImage",
                        "collectionThumbnailViewModel",
                        "primaryThumbnail",
                        "thumbnailViewModel",
                        "image",
                        "sources",
                    ],
                ),
                "videoCount": self._getValue(
                    lockup,
                    [
                        "contentImage",
                        "collectionThumbnailViewModel",
                        "primaryThumbnail",
                        "thumbnailViewModel",
                        "overlays",
                        0,
                        "thumbnailOverlayBadgeViewModel",
                        "thumbnailBadges",
                        0,
                        "thumbnailBadgeViewModel",
                        "text",
                    ],
                ),
                "channel": {
                    "name": self._getValue(
                        lockup,
                        [
                            "metadata",
                            "lockupMetadataViewModel",
                            "metadata",
                            "contentMetadataViewModel",
                            "metadataRows",
                            0,
                            "metadataParts",
                            0,
                            "text",
                            "content",
                        ],
                    ),
                    "id": self._getValue(
                        lockup,
                        [
                            "metadata",
                            "lockupMetadataViewModel",
                            "metadata",
                            "contentMetadataViewModel",
                            "metadataRows",
                            0,
                            "metadataParts",
                            0,
                            "text",
                            "commandRuns",
                            0,
                            "onTap",
                            "innertubeCommand",
                            "browseEndpoint",
                            "browseId",
                        ],
                    ),
                },
            }
        else:
            raise ValueError(
                "ERROR: Could not parse playlist element."
            )
        
        component["link"] = "https://www.youtube.com/playlist?list=" + component["id"]
        if component["channel"]["id"]: component["channel"]["link"] = ("https://www.youtube.com/channel/" + component["channel"]["id"])
        return component
    
    def _getVideoFromChannelSearch(self, elements: list) -> list:
        channelsearch = []
        for element in elements:
            element = self._getValue(element, ["childVideoRenderer"])
            json = {
                "id":                                    self._getValue(element, ["videoId"]),
                "title":                                 self._getValue(element, ["title", "simpleText"]),
                "uri":                                   self._getValue(element, ["navigationEndpoint", "commandMetadata", "webCommandMetadata", "url"]),
                "duration": {
                    "simpleText":                        self._getValue(element, ["lengthText", "simpleText"]),
                    "text":                              self._getValue(element, ["lengthText", "accessibility", "accessibilityData", "label"])
                }
            }
            channelsearch.append(json)
        return channelsearch
    
    def _getChannelSearchComponent(self, elements: list) -> list:
        channelsearch = []
        for element in elements:
            responsetype = None

            if 'gridPlaylistRenderer' in element:
                element = element['gridPlaylistRenderer']
                responsetype = 'gridplaylist'
            elif 'itemSectionRenderer' in element:
                first_content = element["itemSectionRenderer"]["contents"][0]
                if 'videoRenderer' in first_content:
                    element = first_content['videoRenderer']
                    responsetype = "video"
                elif 'playlistRenderer' in first_content:
                    element = first_content["playlistRenderer"]
                    responsetype = "playlist"
                else:
                    raise Exception(f'Unexpected first_content {first_content}')
            elif 'continuationItemRenderer' in element:
                # for endless scrolling, not needed here
                # TODO: Implement endless scrolling
                continue
            else:
                raise Exception(f'Unexpected element {element}')
            
            if responsetype == "video":
                json = {
                    "id":                                    self._getValue(element, ["videoId"]),
                    "thumbnails": {
                        "normal":                            self._getValue(element, ["thumbnail", "thumbnails"]),
                        "rich":                              self._getValue(element, ["richThumbnail", "movingThumbnailRenderer", "movingThumbnailDetails", "thumbnails"])
                    },
                    "title":                                 self._getValue(element, ["title", "runs", 0, "text"]),
                    "descriptionSnippet":                    self._getValue(element, ["descriptionSnippet", "runs", 0, "text"]),
                    "uri":                                   self._getValue(element, ["navigationEndpoint", "commandMetadata", "webCommandMetadata", "url"]),
                    "views": {
                        "precise":                           self._getValue(element, ["viewCountText", "simpleText"]),
                        "simple":                            self._getValue(element, ["shortViewCountText", "simpleText"]),
                        "approximate":                       self._getValue(element, ["shortViewCountText", "accessibility", "accessibilityData", "label"])
                    },
                    "duration": {
                        "simpleText":                        self._getValue(element, ["lengthText", "simpleText"]),
                        "text":                              self._getValue(element, ["lengthText", "accessibility", "accessibilityData", "label"])
                    },
                    "published":                             self._getValue(element, ["publishedTimeText", "simpleText"]),
                    "channel": {
                        "name":                              self._getValue(element, ["ownerText", "runs", 0, "text"]),
                        "thumbnails":                        self._getValue(element, ["channelThumbnailSupportedRenderers", "channelThumbnailWithLinkRenderer", "thumbnail", "thumbnails"])
                    },
                    "type":                                  responsetype
                }
            elif responsetype == 'playlist':
                json = {
                    "id":                                    self._getValue(element, ["playlistId"]),
                    "videos":                                self._getVideoFromChannelSearch(self._getValue(element, ["videos"])),
                    "thumbnails": {
                        "normal":                            self._getValue(element, ["thumbnails"]),
                    },
                    "title":                                 self._getValue(element, ["title", "simpleText"]),
                    "uri":                                   self._getValue(element, ["navigationEndpoint", "commandMetadata", "webCommandMetadata", "url"]),
                    "channel": {
                        "name":                              self._getValue(element, ["longBylineText", "runs", 0, "text"]),
                    },
                    "type":                                  responsetype
                }
            else:
                json = {
                    "id":                                    self._getValue(element, ["playlistId"]),
                    "thumbnails": {
                        "normal":                            self._getValue(element, ["thumbnail", "thumbnails", 0]),
                    },
                    "title":                                 self._getValue(element, ["title", "runs", 0, "text"]),
                    "uri":                                   self._getValue(element, ["navigationEndpoint", "commandMetadata", "webCommandMetadata", "url"]),
                    "type":                                  'playlist'
                }
            channelsearch.append(json)
        return channelsearch

    def _getShelfComponent(self, element: dict) -> dict:
        shelf = element[shelfElementKey]
        return {
            'title':                           self._getValue(shelf, ['title', 'simpleText']),
            'elements':                        self._getValue(shelf, ['content', 'verticalListRenderer', 'items']),
        }

    def _getValue(self, source: dict, path: List[str]) -> Union[str, int, dict, None]:
        value = source
        for key in path:
            if type(key) is str:
                if key in value.keys():
                    value = value[key]
                else:
                    value = None
                    break
            elif type(key) is int:
                if len(value) != 0:
                    value = value[key]
                else:
                    value = None
                    break
        return value

class RequestHandler(ComponentHandler):
    def _makeRequest(self) -> None:
        ''' Fixes #47 '''
        requestBody = copy.deepcopy(requestPayload)
        requestBody['query'] = self.query
        requestBody['client'] = {
            'hl': self.language,
            'gl': self.region,
        }
        if self.searchPreferences:
            requestBody['params'] = self.searchPreferences
        if self.continuationKey:
            requestBody['continuation'] = self.continuationKey
        requestBodyBytes = json.dumps(requestBody).encode('utf_8')
        request = Request(
            'https://www.youtube.com/youtubei/v1/search' + '?' + urlencode({
                'key': searchKey,
            }),
            data = requestBodyBytes,
            headers = {
                'Content-Type': 'application/json; charset=utf-8',
                'Content-Length': len(requestBodyBytes),
                'User-Agent': userAgent,
            }
        )
        try:
            self.response = urlopen(request, timeout=self.timeout).read().decode('utf_8')
        except:
            raise Exception('ERROR: Could not make request.')
    
    def _parseSource(self) -> None:
        try:
            if not self.continuationKey:
                responseContent = self._getValue(json.loads(self.response), contentPath)
            else:
                responseContent = self._getValue(json.loads(self.response), continuationContentPath)
            if responseContent:
                for element in responseContent:
                    if itemSectionKey in element.keys():
                        self.responseSource = self._getValue(element, [itemSectionKey, 'contents'])
                    if continuationItemKey in element.keys():
                        self.continuationKey = self._getValue(element, continuationKeyPath)
            else:
                self.responseSource = self._getValue(json.loads(self.response), fallbackContentPath)
                self.continuationKey = self._getValue(self.responseSource[-1], continuationKeyPath)
        except:
            raise Exception('ERROR: Could not parse YouTube response.')

