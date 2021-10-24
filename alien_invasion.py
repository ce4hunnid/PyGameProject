import sys   #use tools in the sys module to exit the game when the player quits

from time import sleep #import the sleep function from time module so we can pause game for moment when ship is hit

import pygame #contains the functionality we need to make a game

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    #Overall class to manage game assets and behavior... will add rest of code to this program at end

    def __init__(self):
        #Initialize the game and create game resources
        pygame.init()  #Function initializes the background settings

        self.settings = Settings() #creates settings instance


        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN) #Create a display window where we draw the game's graphical elements.
                                                           #(1200,800) argument is a tuple that defines the dimensions of game window (pixels wide, pixels high)
                                                           #Assigned display window to attribute self.screen so it is available in all methods in class
                                                           #self.screen is a surface where a game element is displayed
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')

        #Create an instance to store game statistics and create the scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)


        self.ship = Ship(self)   #creates instance of ship after screen is created
        #Set the background color
        #self.bg_color = (230,230,230) #red,green,blue shade mixture to create light grey color, used as argument for background
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #Make the play button
        self.play_button = Button(self,"Play")

    def run_game(self):
        #This will start the main loop for the game, while loop runs continuously
        while True:
            self._check_events()   #still need to check events even if user is no longer playing
            
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _update_bullets(self):
        #update position of bullets and get rid of old bullets

        self.bullets.update()

        #Get rid of bullets that have disappeared by detecting when bottom value of a bullet's rect has a value of 0 (passed top of screen)
        for bullet in self.bullets.copy():    #copy allows us to modify bullets inside the loop
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

        #Check for any bultets that have hit aliens
        #If so, get rid of the bullet and the alien
             

    def _check_bullet_alien_collisions(self):
        #Respond to bullet-alien collisions
        #Remove any bullets and alines that have collided
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)  #The two true arguments tells code to delete bullets and aliens that have collided
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:                                          #this checks to see if aliens group is empty
            #Destroy existing bullets and create a new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed() 

            #Increase level
            self.stats.level += 1
            self.sb.prep_level()
    
    def _update_aliens(self):
        #Check if fleet is at an edge
        #Then, update the positions of all aliens in the fleet
        self._check_fleet_edges()
        self.aliens.update() #This update method calls each alien's update

        #Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        #Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _ship_hit(self):
        #Respond to the ship being hit by an alien
        
        if self.stats.ships_left > 0:
            #Decrement ships left and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()  #displays correct number of ship lives

            #Get rid of any remaining alines and bullets
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #Pause it
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_events(self):

        #Watch for keyboard and mouse events
        for event in pygame.event.get():         #an event is anything the user does (shoot, move, select, quit)... event loop
                                                    #If player hits quit, the event loop will track it and sys.exit()
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:    #detects when mouse is clicked
                mouse_pos = pygame.mouse.get_pos()        #we want to know WHERE the mouse is clicked though

                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
   
    def _check_play_button(self,mouse_pos):
        #Start a new game when the player clicks Play!
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:   #checks to see if click's rect is same coordinates as play button's rect
            #Reset the game stats
            self.settings.initialize_dynamic_settings()  #slows game back down
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()  #This sets  score back to 0
            self.sb.prep_level()
            self.sb.prep_ships()

            #Get rid of any remaing aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #Hide the mouse cursor
            pygame.mouse.set_visible(False)
    def _check_keydown_events(self,event):    #responds to key down events
            if event.key == pygame.K_RIGHT:
                #MOVE THE SHIP TO THE RIGHT
                self.ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = True
            elif event.key == pygame.K_q:
                sys.exit()
            elif event.key == pygame.K_SPACE:
                self._fire_bullet()
    def _check_keyup_events(self,event):      #responds to key up events                
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = False

    def _fire_bullet(self):
        #Create a new bullet and add it to the bullet group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _create_fleet(self):
        #Create the fleet of aliens
        #Create an alien and find the numbe of aliens in a row
        #Spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size                       
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #Determine the number of rows of aliens that fit on then screen

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3*alien_height)-ship_height)          #calculates num rows that can fit on the screen
        number_rows = available_space_y // (2 * alien_height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)
            #Create an alien and place it in the row
            
            

    def _create_alien(self,alien_number,row_number):
        #Create an alien and place it in the row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        #Respond appropriately if aliens have reached an edge
        for alien in self.aliens.sprites():                   #loop through the fleet and call check_edges() on each alien... if True, alien is at edge and needs to change directions
            if alien.check_edges():
                self._change_fleet_direction()               #this breaks the loop
                break

    def _change_fleet_direction(self):
        #Drop the entire fleet and change the fleet's direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed     #then loop through all the aliens and drop each one using the settting fleet_drop_speed()
        self.settings.fleet_direction *= -1   #this is out of the loop because we want to bring the aliens down vertically constantly but change direction of fleet once


    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)  #fills screen with grey color variable 
        self.ship.blitme() #draw the ship on screen, infront of background

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        #Draw the score info
        self.sb.show_score()

        #Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
        #Make the most recently drawn screen visible
        pygame.display.flip() #continually updates the display to show the new positions of game elements/hides old ones, creating illusion of smooth moving

        

    def _check_aliens_bottom(self):
        #Check if any aliens have reached the bottom of the screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Treat this the same as if the ship got hit
                self._ship_hit()
                break

if __name__ == '__main__':
    #Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game() #run_game() is in if block that only runs if the file is called directly
