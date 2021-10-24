import pygame.font
from pygame.sprite import Group

from ship import Ship
class Scoreboard:
    #A class to report scoring info

    def __init__(self,ai_game):
        #Initialize scorekeeping attributes
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #Font settings for scoring info
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        #Prepare the initial score images
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        #Turn the score into a rendered image
        rounded_score = round(self.stats.score, -1)   #tells python to round value of stats.score to nearest 10
        score_str = "{:,}".format(rounded_score) #Turn the numerical value stats.score into a string then pass that string to render() for image
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        #Display the score at the top right of the screnn
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20    #set it this way so the score is always right aligned and 20 pizels down from the top of screen

        self.score_rect.top = 20

    def prep_high_score(self):
        #Turn the high score into a rendered image
        high_score = round(self.stats.high_score, -1)   #round high score to nearest 10 and add commas
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color) #create image from high score

        #Center the high score at the top fo the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx     #center the image horizontally
        self.high_score_rect.top = self.score_rect.top              #Set its top attribute to match the top of the score image

    def show_score(self):
        #Draw scores, levels, and ships to screen
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
        
    def check_high_score(self):
        #Check to see if there is a new high score
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        #Turn the level into a rendered image
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)  #creates an image from value stored in stats.level

        #Position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10  #sets the top attribute 10 pixels beneath the btotom of the score iomage to leave space between score and level

    def prep_ships(self):     #creates an empty group (self.ships) to hold the ship instances
        #How many ships are left
        self.ships = Group()                 
        for ship_number in range(self.stats.ships_left): #this loop runs for every ship the player has left
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width #create a new ship and set each ship's x coordinate so the ships appear next to each other, 10 pixel margins on left side 
            ship.rect.y = 10 #Set y coordinate value 10 pixels down from the top of the screen
            self.ships.add(ship)
