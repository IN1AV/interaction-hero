from classes.Song import Song

# If you want to make your own Song, look at the Song class and which attributes it needs to create one.
# Example below is also usefull in understanding the working of the different attributes of a Song.

example_song_short = Song(
    "tarkan_simarik.txt",
    notes_bpm=380,
    bg_game_header="Tarkan Simarik",             # bg_game_header
)

example_song_long = Song(
    'ode_to_joy.txt',
)