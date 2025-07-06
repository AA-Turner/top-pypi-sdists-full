# THIS IS AN AUTOMATICALLY GENERATED FILE, DO NOT MODIFY DIRECTLY

import pytest

from zimscraperlib.rewriting.url_rewriting import ArticleUrlRewriter

from .utils import ContentForTests


@pytest.fixture(
    params=[


        ContentForTests(
            "foobargooglevideo.com/videoplayback?id=1576&key=value",
            "youtube.fuzzy.replayweb.page/videoplayback?id=1576",
        ),



        ContentForTests(
            "foobargooglevideo.com/videoplayback?some=thing&id=1576",
            "youtube.fuzzy.replayweb.page/videoplayback?id=1576",
        ),



        ContentForTests(
            "foobargooglevideo.com/videoplayback?some=thing&id=1576&key=value",
            "youtube.fuzzy.replayweb.page/videoplayback?id=1576",
        ),



        ContentForTests(
            "foobargooglevideo.com/videoplaybackandfoo?some=thing&id=1576&key=value",
        ),



        ContentForTests(
            "foobargoogle_video.com/videoplaybackandfoo?some=thing&id=1576&key=value",
        ),


    ]
)
def googlevideo_com_case(request: pytest.FixtureRequest):
    yield request.param


def test_fuzzyrules_googlevideo_com(googlevideo_com_case: ContentForTests):
    assert (
        ArticleUrlRewriter.apply_additional_rules(googlevideo_com_case.input_str)
        == googlevideo_com_case.expected_str
    )

@pytest.fixture(
    params=[


        ContentForTests(
            "www.youtube.com/get_video_info?video_id=123ah",
            "youtube.fuzzy.replayweb.page/get_video_info?video_id=123ah",
        ),



        ContentForTests(
            "www.youtube.com/get_video_info?foo=bar&video_id=123ah",
            "youtube.fuzzy.replayweb.page/get_video_info?video_id=123ah",
        ),



        ContentForTests(
            "www.youtube.com/get_video_info?video_id=123ah&foo=bar",
            "youtube.fuzzy.replayweb.page/get_video_info?video_id=123ah",
        ),



        ContentForTests(
            "youtube.com/get_video_info?video_id=123ah",
            "youtube.fuzzy.replayweb.page/get_video_info?video_id=123ah",
        ),



        ContentForTests(
            "youtube-nocookie.com/get_video_info?video_id=123ah",
            "youtube.fuzzy.replayweb.page/get_video_info?video_id=123ah",
        ),



        ContentForTests(
            "www.youtube-nocookie.com/get_video_info?video_id=123ah",
            "youtube.fuzzy.replayweb.page/get_video_info?video_id=123ah",
        ),



        ContentForTests(
            "www.youtube-nocookie.com/get_video_info?foo=bar",
        ),



        ContentForTests(
            "www.youtubeqnocookie.com/get_video_info?video_id=123ah",
        ),


    ]
)
def youtube_video_info_case(request: pytest.FixtureRequest):
    yield request.param


def test_fuzzyrules_youtube_video_info(youtube_video_info_case: ContentForTests):
    assert (
        ArticleUrlRewriter.apply_additional_rules(youtube_video_info_case.input_str)
        == youtube_video_info_case.expected_str
    )

@pytest.fixture(
    params=[


        ContentForTests(
            "i.ytimg.com/vi/-KpLmsAR23I/maxresdefault.jpg?sqp=-oaymwEmCIAKENAF8quKqQMa8AEB-AH-CYAC0AWKAgwIABABGHIgTyg-MA8=&rs=AOn4CLDr-FmDmP3aCsD84l48ygBmkwHg-g",
            "i.ytimg.com.fuzzy.replayweb.page/vi/-KpLmsAR23I/thumbnail.jpg",
        ),



        ContentForTests(
            "i.ytimg.com/vi/-KpLmsAR23I/maxresdefault.png?sqp=-oaymwEmCIAKENAF8quKqQMa8AEB-AH-CYAC0AWKAgwIABABGHIgTyg-MA8=&rs=AOn4CLDr-FmDmP3aCsD84l48ygBmkwHg-g",
            "i.ytimg.com.fuzzy.replayweb.page/vi/-KpLmsAR23I/thumbnail.png",
        ),



        ContentForTests(
            "i.ytimg.com/vi/-KpLmsAR23I/maxresdefault.jpg",
            "i.ytimg.com.fuzzy.replayweb.page/vi/-KpLmsAR23I/thumbnail.jpg",
        ),



        ContentForTests(
            "i.ytimg.com/vi/-KpLmsAR23I/max-res.default.jpg",
            "i.ytimg.com.fuzzy.replayweb.page/vi/-KpLmsAR23I/thumbnail.jpg",
        ),


    ]
)
def youtube_thumbnails_case(request: pytest.FixtureRequest):
    yield request.param


def test_fuzzyrules_youtube_thumbnails(youtube_thumbnails_case: ContentForTests):
    assert (
        ArticleUrlRewriter.apply_additional_rules(youtube_thumbnails_case.input_str)
        == youtube_thumbnails_case.expected_str
    )

@pytest.fixture(
    params=[


        ContentForTests(
            "www.example.com/page?1234",
            "www.example.com/page",
        ),



        ContentForTests(
            "www.example.com/page?foo=1234",
        ),



        ContentForTests(
            "www.example.com/page1234",
        ),



        ContentForTests(
            "www.example.com/page?foo=bar&1234",
        ),



        ContentForTests(
            "www.example.com/page?1234=bar",
        ),



        ContentForTests(
            "www.example.com/page?1234&foo=bar",
        ),


    ]
)
def trim_digits_only_case(request: pytest.FixtureRequest):
    yield request.param


def test_fuzzyrules_trim_digits_only(trim_digits_only_case: ContentForTests):
    assert (
        ArticleUrlRewriter.apply_additional_rules(trim_digits_only_case.input_str)
        == trim_digits_only_case.expected_str
    )

@pytest.fixture(
    params=[


        ContentForTests(
            "www.youtube-nocookie.com/youtubei/page/?videoId=123ah",
            "youtube.fuzzy.replayweb.page/youtubei/page/?videoId=123ah",
        ),



        ContentForTests(
            "youtube-nocookie.com/youtubei/page/?videoId=123ah",
            "youtube.fuzzy.replayweb.page/youtubei/page/?videoId=123ah",
        ),



        ContentForTests(
            "youtube.com/youtubei/page/?videoId=123ah",
            "youtube.fuzzy.replayweb.page/youtubei/page/?videoId=123ah",
        ),



        ContentForTests(
            "www.youtube.com/youtubei/page/?videoId=123ah",
            "youtube.fuzzy.replayweb.page/youtubei/page/?videoId=123ah",
        ),



        ContentForTests(
            "youtube.com/youtubei/page/videoId=123ah",
            "youtube.fuzzy.replayweb.page/youtubei/page/?videoId=123ah",
        ),



        ContentForTests(
            "youtube.com/youtubei/page/videoIdqqq=123ah",
            "youtube.fuzzy.replayweb.page/youtubei/page/?videoIdqqq=123ah",
        ),



        ContentForTests(
            "youtube.com/youtubei/page/videoId=123ah&foo=bar",
            "youtube.fuzzy.replayweb.page/youtubei/page/?videoId=123ah",
        ),



        ContentForTests(
            "youtube.com/youtubei/page/?foo=bar&videoId=123ah",
            "youtube.fuzzy.replayweb.page/youtubei/page/?videoId=123ah",
        ),



        ContentForTests(
            "youtube.com/youtubei/page/foo=bar&videoId=123ah",
            "youtube.fuzzy.replayweb.page/youtubei/page/foo=bar&?videoId=123ah",
        ),



        ContentForTests(
            "youtube.com/youtubei/?videoId=123ah",
        ),


    ]
)
def youtubei_case(request: pytest.FixtureRequest):
    yield request.param


def test_fuzzyrules_youtubei(youtubei_case: ContentForTests):
    assert (
        ArticleUrlRewriter.apply_additional_rules(youtubei_case.input_str)
        == youtubei_case.expected_str
    )

@pytest.fixture(
    params=[


        ContentForTests(
            "www.youtube-nocookie.com/embed/foo",
            "youtube.fuzzy.replayweb.page/embed/foo",
        ),



        ContentForTests(
            "www.youtube-nocookie.com/embed/bar",
            "youtube.fuzzy.replayweb.page/embed/bar",
        ),



        ContentForTests(
            "www.youtube-nocookie.com/embed/foo/bar",
            "youtube.fuzzy.replayweb.page/embed/foo/bar",
        ),



        ContentForTests(
            "www.youtube.com/embed/foo",
            "youtube.fuzzy.replayweb.page/embed/foo",
        ),



        ContentForTests(
            "youtube.com/embed/foo",
            "youtube.fuzzy.replayweb.page/embed/foo",
        ),



        ContentForTests(
            "youtube-nocookie.com/embed/foo",
            "youtube.fuzzy.replayweb.page/embed/foo",
        ),



        ContentForTests(
            "youtube.com/embed/foo?bar=alice",
            "youtube.fuzzy.replayweb.page/embed/foo",
        ),


    ]
)
def youtube_embed_case(request: pytest.FixtureRequest):
    yield request.param


def test_fuzzyrules_youtube_embed(youtube_embed_case: ContentForTests):
    assert (
        ArticleUrlRewriter.apply_additional_rules(youtube_embed_case.input_str)
        == youtube_embed_case.expected_str
    )

@pytest.fixture(
    params=[


        ContentForTests(
            "gcs-vimeo.akamaized.net/123.mp4?range=123-456",
            "vimeo-cdn.fuzzy.replayweb.page/123.mp4?range=123-456",
        ),



        ContentForTests(
            "vod.akamaized.net/123.mp4?range=123-456",
            "vimeo-cdn.fuzzy.replayweb.page/123.mp4?range=123-456",
        ),



        ContentForTests(
            "vod-progressive.akamaized.net/123.mp4?range=123-456",
            "vimeo-cdn.fuzzy.replayweb.page/123.mp4?range=123-456",
        ),



        ContentForTests(
            "vod-adaptive.akamaized.net/123.mp4?range=123-456",
            "vimeo-cdn.fuzzy.replayweb.page/123.mp4?range=123-456",
        ),



        ContentForTests(
            "vod.akamaized.net/123.mp4?foo=bar&range=123-456",
            "vimeo-cdn.fuzzy.replayweb.page/123.mp4?range=123-456",
        ),



        ContentForTests(
            "vod.akamaized.net/123.mp4?foo=bar&range=123-456&bar=foo",
            "vimeo-cdn.fuzzy.replayweb.page/123.mp4?range=123-456",
        ),



        ContentForTests(
            "vod.akamaized.net/123.mp4?range=123-456&bar=foo",
            "vimeo-cdn.fuzzy.replayweb.page/123.mp4?range=123-456",
        ),



        ContentForTests(
            "foovod.akamaized.net/123.mp4?range=123-456",
            "vimeo-cdn.fuzzy.replayweb.page/123.mp4?range=123-456",
        ),



        ContentForTests(
            "vod.akamaized.net/1/23.mp4?range=123-456",
            "vimeo-cdn.fuzzy.replayweb.page/23.mp4?range=123-456",
        ),



        ContentForTests(
            "vod.akamaized.net/a/23.mp4?range=123-456",
            "vimeo-cdn.fuzzy.replayweb.page/23.mp4?range=123-456",
        ),



        ContentForTests(
            "vod.akamaized.net/foo/bar/23.mp4?range=123-456",
            "vimeo-cdn.fuzzy.replayweb.page/23.mp4?range=123-456",
        ),



        ContentForTests(
            "foo.akamaized.net/123.mp4?range=123-456",
        ),


    ]
)
def vimeo_cdn_fix_case(request: pytest.FixtureRequest):
    yield request.param


def test_fuzzyrules_vimeo_cdn_fix(vimeo_cdn_fix_case: ContentForTests):
    assert (
        ArticleUrlRewriter.apply_additional_rules(vimeo_cdn_fix_case.input_str)
        == vimeo_cdn_fix_case.expected_str
    )

@pytest.fixture(
    params=[


        ContentForTests(
            "vod.akamaized.net/23.mp4",
            "vimeo-cdn.fuzzy.replayweb.page/23.mp4",
        ),



        ContentForTests(
            "vod.akamaized.net/23/12332.mp4",
            "vimeo-cdn.fuzzy.replayweb.page/23/12332.mp4",
        ),



        ContentForTests(
            "https://vod-progressive.akamaized.net/exp=1635528595~acl=%2Fvimeo-prod-skyfire-std-us%2F01%2F4423%2F13%2F347119375%2F1398505169.mp4~hmac=27c31f1990aab5e5429f7f7db5b2dcbcf8d2f5c92184d53102da36920d33d53e/vimeo-prod-skyfire-std-us/01/4423/13/347119375/1398505169.mp4",
            "vimeo-cdn.fuzzy.replayweb.page/01/4423/13/347119375/1398505169.mp4",
        ),


    ]
)
def vimeo_cdn_case(request: pytest.FixtureRequest):
    yield request.param


def test_fuzzyrules_vimeo_cdn(vimeo_cdn_case: ContentForTests):
    assert (
        ArticleUrlRewriter.apply_additional_rules(vimeo_cdn_case.input_str)
        == vimeo_cdn_case.expected_str
    )

@pytest.fixture(
    params=[


        ContentForTests(
            "player.vimeo.com/video/1234?foo=bar",
            "vimeo.fuzzy.replayweb.page/video/1234",
        ),



        ContentForTests(
            "foo.player.vimeo.com/video/1234?foo=bar",
            "vimeo.fuzzy.replayweb.page/video/1234",
        ),



        ContentForTests(
            "player.vimeo.com/video/1234?foo",
            "vimeo.fuzzy.replayweb.page/video/1234",
        ),



        ContentForTests(
            "player.vimeo.com/video/1/23?foo=bar",
        ),



        ContentForTests(
            "player.vimeo.com/video/123a?foo=bar",
        ),



        ContentForTests(
            "player.vimeo.com/video/?foo=bar",
        ),


    ]
)
def vimeo_player_case(request: pytest.FixtureRequest):
    yield request.param


def test_fuzzyrules_vimeo_player(vimeo_player_case: ContentForTests):
    assert (
        ArticleUrlRewriter.apply_additional_rules(vimeo_player_case.input_str)
        == vimeo_player_case.expected_str
    )

@pytest.fixture(
    params=[


        ContentForTests(
            "i.vimeocdn.com/image/1234?foo=bar",
            "i.vimeocdn.fuzzy.replayweb.page/image/1234",
        ),



        ContentForTests(
            "i.vimeocdn.com/something/a456?foo",
            "i.vimeocdn.fuzzy.replayweb.page/something/a456",
        ),


    ]
)
def i_vimeo_cdn_case(request: pytest.FixtureRequest):
    yield request.param


def test_fuzzyrules_i_vimeo_cdn(i_vimeo_cdn_case: ContentForTests):
    assert (
        ArticleUrlRewriter.apply_additional_rules(i_vimeo_cdn_case.input_str)
        == i_vimeo_cdn_case.expected_str
    )

@pytest.fixture(
    params=[


        ContentForTests(
            "cheatography.com/scripts/useful.min.js?v=2&q=1719438924",
            "cheatography.com.fuzzy.replayweb.page/scripts/useful.min.js?v=2",
        ),



        ContentForTests(
            "cheatography.com/scripts/foo.js?v=2&q=1719438924",
            "cheatography.com.fuzzy.replayweb.page/scripts/foo.js?v=2",
        ),



        ContentForTests(
            "cheatography.com/scripts/useful.min.js?q=1719438924&v=2",
            "cheatography.com.fuzzy.replayweb.page/scripts/useful.min.js?v=2",
        ),



        ContentForTests(
            "cheatography.com/scripts/useful.min.js?q=1719438924&v=2&foo=bar",
            "cheatography.com.fuzzy.replayweb.page/scripts/useful.min.js?v=2",
        ),


    ]
)
def cheatography_com_case(request: pytest.FixtureRequest):
    yield request.param


def test_fuzzyrules_cheatography_com(cheatography_com_case: ContentForTests):
    assert (
        ArticleUrlRewriter.apply_additional_rules(cheatography_com_case.input_str)
        == cheatography_com_case.expected_str
    )

@pytest.fixture(
    params=[


        ContentForTests(
            "blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjlN4LY6kFVwL8-rinDWp3kJp1TowOVD8vq8TP8nl3Lf1sI-hx0DE1GQA1jw7DT7XvK3FjghzJ17_1pvyXyDBAV0vtigJRnFCNfMxnndBnN3NYoXUvKQQsQ7JTGXOSajdo0mNQIv8wss_AxPBMrR4-Dd_EEacV7ZMS3m_IL2dz0WsbbKn7FD7ntsfOe0JUq/s600-rw/tickerzugtier2.jpg=w487-h220-p-k-no-nu",
            "blogger.googleusercontent.com.fuzzy.replayweb.page/img/b/R29vZ2xl/AVvXsEjlN4LY6kFVwL8-rinDWp3kJp1TowOVD8vq8TP8nl3Lf1sI-hx0DE1GQA1jw7DT7XvK3FjghzJ17_1pvyXyDBAV0vtigJRnFCNfMxnndBnN3NYoXUvKQQsQ7JTGXOSajdo0mNQIv8wss_AxPBMrR4-Dd_EEacV7ZMS3m_IL2dz0WsbbKn7FD7ntsfOe0JUq/s600-rw/tickerzugtier2.jpg.resized",
        ),



        ContentForTests(
            "blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjlN4LY6kFVwL8-rinDWp3kJp1TowOVD8vq8TP8nl3Lf1sI-hx0DE1GQA1jw7DT7XvK3FjghzJ17_1pvyXyDBAV0vtigJRnFCNfMxnndBnN3NYoXUvKQQsQ7JTGXOSajdo0mNQIv8wss_AxPBMrR4-Dd_EEacV7ZMS3m_IL2dz0WsbbKn7FD7ntsfOe0JUq/w72-h72-p-k-no-nu/tickerzugtier2.jpg",
        ),


    ]
)
def der_postillon_com_case(request: pytest.FixtureRequest):
    yield request.param


def test_fuzzyrules_der_postillon_com(der_postillon_com_case: ContentForTests):
    assert (
        ArticleUrlRewriter.apply_additional_rules(der_postillon_com_case.input_str)
        == der_postillon_com_case.expected_str
    )

@pytest.fixture(
    params=[


        ContentForTests(
            "iranwire.com/questions/detail/1723?&_=1721804954220",
            "iranwire.com/questions/detail/1723",
        ),



        ContentForTests(
            "iranwire.com/questions/detail/1725?foo=bar&_=1721804454220",
            "iranwire.com/questions/detail/1725",
        ),


    ]
)
def iranwire_com_case(request: pytest.FixtureRequest):
    yield request.param


def test_fuzzyrules_iranwire_com(iranwire_com_case: ContentForTests):
    assert (
        ArticleUrlRewriter.apply_additional_rules(iranwire_com_case.input_str)
        == iranwire_com_case.expected_str
    )

