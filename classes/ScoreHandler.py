from pygame import sprite, font
from utils import load_font

class ScoreHandler(sprite.Sprite):
    def __init__(self, allsprites, game_state, song):
        sprite.Sprite.__init__(self, allsprites)
        self.game_state = game_state
        self.font = load_font(song.get_font_filename(), 36)

        self.score = 0

        # Feel free to play around with these variables
        # Currently they are not used anywhere in the code
        self.score_streak = 0
        self.score_multiplier = 1

        # Required to make sure the first note hits correctly
        self.played_once = False

        # Flag to see when a score should be saved after an update
        self.score_is_saved = True

        # Required Sprite attributes
        self.image = self.font.render("", 1, (10, 10, 10))
        self.pos = (420, 50)  # Set the location of the text
        self.rect = (self.pos, self.image.get_size())


    def restart(self):
        self.score = 0
        self.score_streak = 0
        self.score_multiplier = 1
        self.score_is_saved = False


    def blit_score_text(self):
        # Very roundabout way to do this, but after spending way too long digging in
        # the code trying to figure out how to add an extra image I just gave up on that
        # Is self.image even referenced anywhere? How is it drawn?
        text = f"Score: {str(self.score)}"
        padding = 19 - 2*len(str(self.score))
        if self.score_multiplier > 1:
            text += padding * " " + f"Multiplier: {str(self.score_multiplier)}"
        self.image = self.font.render(text, True, (10, 10, 10))

    # This is called every frame
    def update(self):
        if self.game_state.state == 'playing':
            self.blit_score_text()
        # elif self.played_once == True:
        #     # print('Your final score: ' + str(self.score))
        #     pass
        if not self.game_state.state == 'playing' and not self.score_is_saved:
            self.save_score()

    def change_score(self, score_difference):
        # add to score streak with positive score
        if score_difference > 0:
            self.score_streak += 1
        # else reset streak and multiplier
        else:
            self.score_streak = 0
            self.score_multiplier = 1
        # change multiplier based on how many notes were hit in succession
        if self.score_streak >= 75:
            self.score_multiplier = 8
        elif self.score_streak >= 50:
            self.score_multiplier = 4
        elif self.score_streak >= 25:
            self.score_multiplier = 2
        else:
            self.score_multiplier = 1
        self.score += score_difference * self.score_multiplier
        
    def get_high_score(self):
        played_song = self.game_state.song.get_notes_filename()
        best_score = None
        with open('scores.txt', 'r') as f:
            scores = f.read().splitlines(False)
            for score in scores:
                songdata = score.split(' ')
                songname = songdata[0]
                songscore = int(songdata[1])
                if songname == played_song and (best_score == None or songscore > best_score):
                    best_score = songscore
        return best_score
    
    def save_score(self):
        self.score_is_saved = True
        self.played_once = True
        with open('scores.txt', 'a') as f:
            text = self.game_state.song.get_notes_filename() + ' ' + str(self.score) + '\n'
            f.write(text)
        # print('The highscore is', self.get_high_score(), '- See ScoreHandler.py for new implementation')
        # print('Your score is', self.score, '- See ScoreHandler.py for new implementation')
