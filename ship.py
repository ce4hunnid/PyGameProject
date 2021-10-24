import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    #A class to manage the ship

    def __init__(self,ai_game):
        #Initialize the ship and set its starting position         #ship has access to all the games resources defined in AlienInvasion class
        super().__init__()
        self.screen = ai_game.screen #assign the screen to an attribute of the ship
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()  #allows us to place the ship in the correct location on screen

        #Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect() #gets the images rectangle location to place the ship later

        #Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        #Store a  decimal value for the ship's horizontal position
        self.x = float(self.rect.x)
        #movement flag
        self.moving_right = False
        self.moving_left = False

       
    def update(self):
        #update the ship's position based on the movemen flag
        #now update the ship's x value not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:   #if self.rect.right is less than, it is not at end of right screen and can continue
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:                          #if value of left side of rect is greater than 0 then ship hasnt met edge of screen yet
            self.x -= self.settings.ship_speed

        #update rect object from self.x       #Only the integer portion of self.x will be stored in self.rect.x which is ok for displaying the ship
        self.rect.x = self.x             
    def blitme(self):
        #Draw the ship at its current location
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        #Center the ship on the screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)   #allows us to track ship's exact location