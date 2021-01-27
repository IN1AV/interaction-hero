from classes.Song import Song

# If you want to make your own Song, look at the Song class and which attributes it needs to create one.
# Example below is also usefull in understanding the working of the different attributes of a Song.

tarkan_simarik = Song(
    "tarkan_simarik.txt",
    notes_bpm=280,
    bg_game_header="Now playing: Tarkan - Simarik",
    font_filename="Calibri.ttf"
)

ode_to_joy = Song(
    'ode_to_joy.txt',
    bg_game_header="Now playing: Beethoven - Ode to Joy",
    font_filename="Calibri.ttf"
)

debug_song = Song(
    "example_notes.txt",
)