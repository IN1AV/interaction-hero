from utils import load_sound, load_font
from classes.GpioButton import GpioButton
from classes.Hitbox import Hitbox
from classes.ScoreHandler import ScoreHandler
from classes.BackgroundHandler import BackgroundHandler
from classes.MusicPlayer import MusicPlayer
from classes.NoteDropper import NoteDropper
from pygame import font, time


class GameState():

    def __init__(self, allsprites, song):
        self.state = 'prestart'

        self.allsprites = allsprites
        self.keyboard_button = []
        self.song = song

        self.font = load_font(song.get_font_filename(), 36)

        self.notes_are_dropping = False
        self.song_is_finished = False

        # Reads and plays audio from notes files
        self.music_player = MusicPlayer(song, self)

        # Responsible for loading and animating the background
        self.background_handler = BackgroundHandler(song)

        # Assigns falling notes to correct hitbox
        self.note_dropper = NoteDropper(self.music_player)

        # Responsible for managing (high) scores
        self.scoreHandler = ScoreHandler(self.allsprites,self, self.song, 1150, 10) 

        # COMBO
        self.combo = ScoreHandler(self.allsprites,self, self.song, 1280/2, 300, "0", 40) 
        # Center the text
        self.combo.change_pos((1280/2) - (self.combo.get_text_width() / 2) )

        # Multiplier
        self.multiplier = ScoreHandler(self.allsprites,self, self.song, 1280/2, 400, " ", 18)
        # Center the text
        self.multiplier.change_pos((1280/2) - (self.multiplier.get_text_width() / 2) )

        # Load sound which plays when a note is missed
        self.sounds_miss = load_sound(song.get_sound_miss())
        
        # Define Hitboxes
        input_keys = ['d', 'f', 'j', 'k']
        self.hitboxes = [
            Hitbox('hitbox-example.png', 0, input_keys[0], self.allsprites),
            Hitbox('hitbox-example.png', 1, input_keys[1], self.allsprites),
            Hitbox('hitbox-example.png', 2, input_keys[2], self.allsprites),
            Hitbox('hitbox-example.png', 3, input_keys[3], self.allsprites),
        ]


    def restart(self, move_speed=10, bpm=0):
        # 0: default bpm.
        # -1: half bpm.
        # 1: 1.5 * bpm
        if bpm == 0:
            bpm = self.song.get_notes_bpm()
        elif bpm < 0:
            bpm = self.song.get_notes_bpm()//2
        elif bpm > 0:
            bpm = int(self.song.get_notes_bpm() * 1.5)
        self.state = 'playing'
        self.notes_are_dropping = False
        self.song_is_finished = False
        self.scoreHandler.restart()
        self.combo.restart()
        self.multiplier.restart()
        self.music_player.restart(move_speed, bpm)


    def drop_next_note_sprite(self, note, move_speed=10):
        self.note_dropper.drop(note, self.hitboxes, move_speed=move_speed)


    def get_background(self):
        return self.background_handler.background


    def end_song(self):
        self.wait_untill_notes_gone = time.get_ticks() + 2000
        self.song_is_finished = True
        self.notes_are_dropping = True


    def update(self):

        self.combo.change_text(str(self.combo.getCombo()))
        self.combo.change_pos((1280/2) - (self.combo.get_text_width() / 2))

        self.multiplier.updateMulitplier()
        self.multiplier.change_pos((1280/2) - (self.multiplier.get_text_width() / 2) )

        self.background_handler.update_background()

        # While the program is not in the menu it loops through this
        if self.state == 'playing':
            # When the song is done and there are no more notes dropping: go to menu
            if self.song_is_finished and not self.notes_are_dropping:
                self.state = 'prestart'
            # When the song is done and there are notes dropping: wait
            elif self.song_is_finished and self.notes_are_dropping:
                # After some time assume no more notes are dropping
                if self.wait_untill_notes_gone < time.get_ticks():
                    self.notes_are_dropping = False
            # Otherwise (when song is not finished) keep updating
            else:
                self.music_player.update()

        # Menu loop, which simply doesn't run other code
        elif self.state == 'prestart':
            return


    def check_for_hit(self, hitbox):
        if hitbox.hits():
            self.scoreHandler.change_score(10)
            self.multiplier.change_score(10)
            self.combo.addCombo()
        else:
            self.sounds_miss.play()
            self.scoreHandler.change_score(-5)
            self.multiplier.change_score(-5)
            self.combo.resetCombo()


    def add_gpio_pins(self, gpio_pins):
        for i in range(4):
            self.hitboxes[i].gpio_event_key = gpio_pins[i]