from classes.Song import Song

# If you want to make your own Song, look at the Song class and which attributes it needs to create one.
# Example below is also usefull in understanding the working of the different attributes of a Song.

tarkan_simarik = Song(
    "tarkan_simarik.txt",
    notes_bpm=280,
    bg_game_header="Tarkan Simarik",
    font_filename="Calibri.ttf"
)

example_song_short = Song(
    "example_notes.txt",
)

example_song_long = Song(
    'ode_to_joy.txt',
    bg_game_header="Beethoven - Ode to Joy",
    font_filename="Calibri.ttf"
)