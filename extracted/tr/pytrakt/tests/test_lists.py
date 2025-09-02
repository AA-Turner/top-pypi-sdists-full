# -*- coding: utf-8 -*-
from trakt.movies import Movie
from trakt.tv import TVEpisode, TVSeason, TVShow
from trakt.users import PublicList


def test_public_list():
    trakt_id = 1248149
    l = PublicList.load(trakt_id)

    assert isinstance(l, PublicList)
    assert l.name == "MARVEL Cinematic Universe"
    assert l.privacy == "public"
    assert l.share_link == "https://trakt.tv/lists/1248149"

    # Test iter
    assert len(l) == 4

    # enumerate list items
    instancetypes = (Movie, TVShow, TVSeason, TVEpisode)
    assert all([isinstance(k.item, instancetypes) for k in l])

    # trakt id is a number
    assert all([isinstance(k.trakt, int) for k in l])
