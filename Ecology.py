# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 18:59:44 2019

Author: S. Rose
@author: ZenthWolf

Simple Evolution Simulator in Python
"""

#--- Depencies ---------------------------------------------------------------+

import pygame


from random import randint
from random import uniform

from math import sqrt
from math import pi
from math import radians
from math import degrees
from math import sin
from math import cos
from math import acos
from math import atan2

#--- FUNCTIONS ---------------------------------------------------------------+

# Note use of screen coords (down is positive)

def dist(x1,y1,x2,y2):
    """"Distance calculation from 1->2"""
    return sqrt((x2-x1)**2 + (y2-y1)**2)

def orientation(x1,y1,x2,y2):
    """Angle from 1->2 in degrees for screen coords"""
    d_x = x2 - x1
    d_y = -y2 + y1
    theta = degrees(atan2(d_y, d_x))
    return theta

def circ_area(r):
    """Area of circle"""
    return pi*(r**2)

def circ_overlap(d, r1, r2):
    """Area of overlap of 2 circles"""
    return (r1**2)*acos((d**2 + r1**2 - r2**2)/(2*d*r1)) + (r2**2)*acos((d**2 + r2**2 - r1**2)/(2*d*r2)) - 0.5*sqrt((-d+r1+r2)*(d-r1+r2)*(d+r1-r2)*(d+r1+r2))

def start_border_x(settings, border):
    """Random x-position along each possible border"""
    if border == 0:  # west border
        return settings['x_min']
        
    elif border == 1:  # east border
        return settings['x_max']

    elif border == 2 or border == 3:  # south/north borders
        return uniform(settings['x_min'], settings['x_max'])
    
    else:
        return 100000   # until better exception handling

def start_border_y(settings, border):
    """Random y-position along each possible border"""
    if border == 0 or border == 1:  # west/east borders
        return uniform(settings['y_min'], settings['y_max'])
        
    elif border == 2:  # north border
        return settings['y_min']

    elif border == 3:  # south border
        return settings['y_max']
    
    else:
        return 100000   # until better exception handling, exile mistaken beasts to the harsh desert!        


def simulate_beasts(settings, screen, biome, gen):
    """Simulate beasts seeking nearest food and returning to shelter"""
    total_time_steps = int(settings['gen_time'] / settings['dt'])

    #--- CYCLE THROUGH EACH TIME STEP ---------------------+
    for t_step in range(0, total_time_steps, 1):
        # ASSUME THIS IS LAST STEP UNTIL PROVEN OTHERWISE
        complete = True
        
        for beast in biome.beasts:
            # IF NOT SHELTERING, CONTINUE SIMULATION
            if complete and not beast.sheltering:
                complete = False

            # IF SEEKING FOOD
            if beast.eats < 2 and len(biome.foods) > 0:
                beast.seek_food(biome.foods)

            # IF DYING
            elif beast.eats == 0 and len(biome.foods) == 0:
                del biome.beasts[biome.beasts.index(beast)]
            # SEEK SHELTER
            elif not beast.sheltering:
                shelter = []
                # Distance to each border
                shelter.append(biome.x_max - beast.x)
                shelter.append(beast.x - biome.x_min)
                shelter.append(biome.y_max - beast.y)
                shelter.append(beast.y - biome.y_min)
                
                shelter_choice = shelter.index(min(shelter))
                
                beast.d_targ = shelter[shelter_choice]
                if beast.d_targ == 0.0:
                    beast.sheltering = True
                    beast.v = 0
                
                if shelter_choice == 0:
                    beast.r_targ = 0
                elif shelter_choice == 1:
                    beast.r_targ = 180
                elif shelter_choice == 2:
                    beast.r_targ = 270
                elif shelter_choice == 3:
                    beast.r_targ = 90
                else:
                    beast.r_targ = 45

        # UPDATE ORGANISMS POSITION AND VELOCITY
        for beast in biome.beasts:
            beast.update_vel(settings)
            beast.update_pos(settings)
        
        # DRAW SCREEN
        screen.fill((0,0,0))
        for food in biome.foods:
            food.Draw(screen)
        for beast in biome.beasts:
            beast.Draw(screen)
        pygame.display.update()
        pygame.time.delay(int(settings['dt']*1000))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            else:
                pass
        
        #END IF ALL BEASTS SHELTERED
        if complete:
            break


    #CHECK FOR FAILED TO SHELTER:
    for beast in biome.beasts:
        if beast.d_targ > 0.075:
            print("BEAST EXPOSED!")
            del biome.beasts[biome.beasts.index(beast)]
    
    return biome.beasts

    
def newgen(settings, beasts):
    """Create the next generation of beasts"""
    for beast in beasts:
        if beast.eats >= 2:
            beasts.append(Beast(settings))
        
        beast.d_targ = 100   # distance to nearest food/shelter
        beast.r_targ = 0     # orientation to nearest food/shelter (degrees)
        beast.eats = 0       # food eaten this generation
        beast.sheltering = False # Going out into the world again

    return beasts
    
def newseason(settings, biome):
    """Sets next generation environment - resets food to max"""
    biome.food_left = settings['food_num']
#    biome.food_left += 10
    return biome

#--- CLASSES -----------------------------------------------------------------+

class Biome:
    """Biome of ecosystem"""
    def __init__(self, settings):
        # BORDER
        self.x_min = settings['x_min']         # west border
        self.x_max = settings['x_max']         # east border
        self.y_min = settings['y_min']         # south border
        self.y_max = settings['y_max']         # north border
        
        # ENTITIES
        self.foods = []     # list of food
        self.populate_foods(settings, settings['food_num'])
        self.beasts = []    #list of beasts
        self.populate_beasts(settings, settings['init_beasts'])
        
    def populate_beasts(self, settings, num_beasts):
        for i in range(0, num_beasts):
            self.beasts.append(Beast(settings))
    
    def populate_foods(self, settings, num_foods):
        for i in range(0, num_foods):
            self.foods.append(Food(settings))
            
class Food():
    """Abstract 'food' particle"""
    def __init__(self, settings):
        # POSITION
        self.x = uniform(settings['x_min'], settings['x_max'])
        self.y = uniform(settings['y_min'], settings['y_max'])
        
        # VALUE
        self.energy = 1
        
        # GRAPHICS
        self.color = (50,255,50)
        self.size = 3
    
    # SCREEN MAPPING FUNCTIONS
    def ScreenX(self):
        """Identifies x-position on screen"""
        return int((self.x + 2)*500/(4) + 10)
    def ScreenY(self):
        """Identifies y-position on screen"""
        return int((self.y + 2)*500/(4) + 10)
    
    # DRAWING
    def Draw(self, screen):
        """Draw to screen"""
        pygame.draw.circle(screen, self.color, (self.ScreenX(), self.ScreenY()), self.size)
        
class Beast():
    """Beasts that seek food"""
    def __init__(self, settings):
        # POSITION AND MOVEMENT
        start = randint(0,3)
        self.x = start_border_x(settings, start)       # position (x)
        self.y = start_border_y(settings, start)       # position (y)
        self.v = settings['v_max']
        self.v_max = settings['v_max']
        
        # COUNTERS AND FLAGS
        self.eats = 0              # food eaten this generation
        self.sheltering = False    # beast is finished this generation

        # GOAL TARGETTING
        self.d_targ = 100   # distance to nearest food/shelter
        self.r_targ = 0     # orientation to nearest food/shelter (degrees)

        # GRAPHICS
        self.color = (255,155,50)
        self.size = 3
        
    # SCREEN MAPPING FUNCTIONS    
    def ScreenX(self):
        """Identifies x-position on screen"""
        return int((self.x + 2)*500/(4) + 10)
    def ScreenY(self):
        """Identifies x-position on screen"""
        return int((self.y + 2)*500/(4) + 10)
    
    ## ACTIONS
    # UPDATE VELOCITY
    def update_vel(self, settings):
        """Sets velocity so that target is not overshot"""
        small_step_speed = self.d_targ/settings['dt'] # speed to take one step to target
        
        self.v= min(small_step_speed, self.v_max)
        
    # UPDATE POSITION
    def update_pos(self, settings):
        """The beast walks!"""
        dx = self.v * cos(radians(self.r_targ)) * settings['dt']
        dy = self.v * sin(radians(self.r_targ)) * settings['dt']
        self.x += dx
        self.y -= dy
        
    # FIND FOOD
    def seek_food(self, foods):
        self.d_targ = 100
        self.r_targ = 0
        for food in foods:
            food_dist = dist(self.x, self.y, food.x, food.y)

            if food_dist <= 0.075:
                self.eats += food.energy
                del foods[foods.index(food)]
#                biome.food_left -= 1
                    
            elif food_dist < self.d_targ:
                self.d_targ = food_dist
                self.r_targ = orientation(self.x, self.y, food.x, food.y)
    
    # DRAWING
    def Draw(self, screen):
        """Draw to screen"""
        pygame.draw.circle(screen, self.color, (self.ScreenX(), self.ScreenY()), self.size)
    
