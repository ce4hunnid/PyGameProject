import pygame.font    #allows us to put text on game screen

class Button:
    def __init__(self,ai_game,msg):
        #Initialize button attributes
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #Set the dimensions and properites of the button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)             #bright green
        self.text_color = (255, 255, 255)           #white text
        self.font = pygame.font.SysFont(None,48)    #prepare a font attribute for rendering text... None means default pygame text

        #Build the button's rect object and center it
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #The button message needs to be prepped only once
        self._prep_msg(msg)

    def _prep_msg(self,msg):
        #Turn the msg into a rendered image and center text on the button
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)     #turns the text strored in msg into an image and store in self.msg_image
      
        self.msg_image_rect = self.msg_image.get_rect() #center the text image on the button
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #Draw blank button and then draw the message
        self.screen.fill(self.button_color, self.rect)         #draws the rectangular portion of button
        self.screen.blit(self.msg_image, self.msg_image_rect)  #draws the text image to the screen