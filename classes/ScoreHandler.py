from pygame import sprite, font
from utils import load_font

class ScoreHandler(sprite.Sprite):
    def __init__(self, allsprites, game_state, song, posx, posy, text=None, fontSize=None):
        sprite.Sprite.__init__(self, allsprites)
        self.game_state = game_state

        self.font_size = 18
        if fontSize:
            self.font_size = fontSize

        self.font = load_font(song.get_font_filename(), self.font_size)

        self.score = 0
        self.combo = 0

        # Feel free to play around with these variables
        # Currently they are not used anywhere in the code
        self.score_streak = 0
        self.score_multiplier = 1

        # Required to make sure the first note hits correctly
        self.played_once = False

        # Flag to see when a score should be saved after an update
        self.score_is_saved = True
        self.text = text
        self.image = self.font.render(text, 1, (10, 10, 10))

        # Required Sprite attributes
        self.pos = (posx, posy)  # Set the location of the text
        self.rect = (self.pos, self.image.get_size())


    def restart(self):
        self.score = 0
        self.score_streak = 0
        self.score_multiplier = 1
        self.combo = 0
        self.score_is_saved = False


    def blit_score_text(self, pause_string=""):
        # Very roundabout way to do this, but after spending way too long digging in
        # the code trying to figure out how to add an extra image I just gave up on that
        # Is self.image even referenced anywhere? How is it drawn?
        if self.text:
            text = self.text
        else:
            if pause_string:
                self.image = self.font.render(pause_string, True, (10, 10, 10))
                return

            
            text = f"Score: {str(self.score)}"

            # if self.score_multiplier > 1:
            #     text += padding * " " + f"Multiplier: {str(self.score_multiplier)}"

        self.image = self.font.render(text, True, (10, 10, 10))
        


    # This is called every frame
    def update(self, pause_string=""):
        if pause_string:
            self.blit_score_text(pause_string)
            return
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
        # print('Your score is', self.score, '- See ScoreHandler.py for new implementation')'
    
    def change_text(self, text):
        if self.text:
            self.text = text
    
    def get_text_width(self):
        return self.image.get_width()

    def change_pos(self,pos):
        self.rect = ((pos, self.pos[1]), self.image.get_size())
    
    def updateMulitplier(self):
        self.text = f"{self.score_multiplier}x"
    
    def addCombo(self):
        self.combo = self.combo + 1

    def resetCombo(self):
        self.combo = 0

    def getCombo(self):
        return self.combo

