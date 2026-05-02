import spotixplore.starting_point as st

import spotixplore.tracks.get_tracks as track
import spotixplore.artists.get_artists as artist

import spotixplore.output.graph as tg
import spotixplore.output.dataframing as df

# First, you need to define credentials in "credentials.py"
# Second, you have to define playlists in "starting_pint.py"

playlists = st.PLAYLISTS
bool_traks = True
related_n = 15
bool_artits = True


def main(playlists, bool_traks, bool_artits, related_n):

	for playlist in playlists:

		track_list = track.explore_tracks(playlist, bool_traks, related_n)
		artist_list = artist.explore_artists(track_list, bool_artits)

		all_nodes_frame = tg.graph_generator(track_list, artist_list, playlist)

		all_tracks_frame, all_artists_frame = df.dataframing(track_list, artist_list, playlist)

		print("Job Done!")

		return all_nodes_frame, all_tracks_frame, all_artists_frame

if __name__ == "__main__":
	main(playlists, bool_traks, bool_artits)
	






