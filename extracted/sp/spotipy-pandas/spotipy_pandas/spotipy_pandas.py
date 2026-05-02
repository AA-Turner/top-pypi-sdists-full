import pandas as pd


def flatten_spotify_iterator(sp, iter):
    results = iter["items"]
    while iter["next"]:
        iter = sp.next(iter)
        results.extend(iter["items"])
    return results


def rebuild_track_dict(track):
    return {
        "id": track["id"],
        "track_name": track["name"],
        "artist_id": track["artists"][0]["id"],
        "artist_name": track["artists"][0]["name"],
        "album_id": track["album"].get("id"),
        "album_name": track["album"].get("name"),
        "release_date": track["album"].get("release_date"),
        "duration": track["duration_ms"] / 1000,
        "uri": track["uri"],
    }


def track_api_output_to_dataframe(tracks):
    tracks = [rebuild_track_dict(track) for track in tracks if track]
    columns = tracks[0].keys()
    tracks_df = pd.DataFrame(tracks, columns=columns)
    tracks_df["playlist_offset"] = tracks_df.index
    return tracks_df


def get_playlist_tracks(sp, playlist_id, audio_features=False):
    tracks = flatten_spotify_iterator(sp, sp.playlist_tracks(playlist_id))
    if not tracks:
        return None
    tracks = [playlist_track["track"] for playlist_track in tracks]
    tracks_df = track_api_output_to_dataframe(tracks)
    if audio_features:
        track_ids = tracks_df["id"]
        track_features = []
        remaining_track_ids = track_ids.to_list()
        while remaining_track_ids:
            track_id_subset = remaining_track_ids[:100]
            remaining_track_ids = remaining_track_ids[100:]
            track_features.extend(sp.audio_features(track_id_subset))
        track_features = filter(None, track_features)
        track_features_df = pd.DataFrame(
            track_features, columns=track_features[0].keys()
        )
        tracks_df = pd.merge(tracks_df, track_features_df, on=["id"], how="left")
    return tracks_df


def get_artists_top_tracks(sp, artist_ids):
    collected_tracks = []
    for artist_id in artist_ids:
        collected_tracks += sp.artist_top_tracks(artist_id)["tracks"]
    return track_api_output_to_dataframe(collected_tracks)


def iterative_batch_action(sp, batch_action, items, batch_size=50):
    while True:
        if not items:
            return
        current_batch = items[:batch_size]
        items = items[batch_size:]
        batch_action(current_batch)


def add_tracks_to_playlist(sp, playlist_id, tracks):
    track_ids = list(tracks["id"])
    iterative_batch_action(
        sp,
        batch_action=lambda batch: sp.playlist_add_items(playlist_id, batch),
        items=track_ids,
    )


def remove_tracks_from_playlist(sp, playlist_id, tracks):
    track_ids = tracks["id"].to_list()
    iterative_batch_action(
        sp,
        batch_action=lambda batch: sp.playlist_remove_all_occurrences_of_items(
            playlist_id, batch
        ),
        items=track_ids,
    )


def truncate_playlist(sp, playlist_id):
    current_tracks = get_playlist_tracks(sp, playlist_id)
    if current_tracks is None:
        return
    remove_tracks_from_playlist(sp, playlist_id, current_tracks)


def overwrite_playlist(sp, playlist_id, tracks):
    truncate_playlist(sp, playlist_id)
    add_tracks_to_playlist(sp, playlist_id, tracks)


def get_saved_tracks(sp):
    playlist_tracks = flatten_spotify_iterator(sp, sp.current_user_saved_tracks())
    tracks = [playlist_track["track"] for playlist_track in playlist_tracks]
    if not tracks:
        return None
    return track_api_output_to_dataframe(tracks)


def save_tracks_to_library(sp, tracks):
    track_ids = list(tracks["id"])
    iterative_batch_action(
        sp,
        batch_action=lambda batch: sp.current_user_saved_tracks_add(batch),
        items=track_ids,
    )


def remove_tracks_from_library(sp, tracks):
    track_ids = list(tracks["id"])
    iterative_batch_action(
        sp,
        batch_action=lambda batch: sp.current_user_saved_tracks_delete(batch),
        items=track_ids,
    )
