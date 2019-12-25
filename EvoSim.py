# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 18:59:44 2019

Author: S. Rose
@author: ZenthWolf

Simple Evolution Simulator in Python
"""
#--- DEPENDANCIES ------------------------------------------------------------+

import pygame


#--- Graphics Parameters -----------------------------------------------------+
graphic_settings = {}

graphic_settings['screen_size'] = (1024, 768)
graphic_settings['window_title'] = "Ecosim"

#--- Init Screen -------------------------------------------------------------+
pygame.init()
screen = pygame.display.set_mode(graphic_settings['screen_size'])
pygame.display.set_caption(graphic_settings['window_title'])
from Ecology import (Food, Beast, Biome, simulate_beasts, newgen, newseason)

#--- Ecology Parameters ------------------------------------------------------+


#Put this in text file?
settings = {}

# FIELD PARAMETERS
# BORDERS (SCREEN COORDS)
settings['x_min'] = -2.0        # west
settings['x_max'] =  2.0        # east
settings['y_min'] = -2.0        # north
settings['y_max'] =  2.0        # south

# SUN AND SOIL
settings['sunshine'] = 10       # Sunlight energy density
settings ['nutrients'] = 10     # Soil nutrient density

# EVOLUTION SETTINGS
settings['food_num'] = 50       # number of food particles (for beast sim)
settings['gens'] = 10           # number of generations

# SIMULATION SETTINGS
settings['gen_time'] = 10       # generation length         (seconds)
settings['dt'] = 0.04           # simulation time step      (dt)

# BEAST PARAMETERS
settings['init_beasts'] = 1     #starting population
settings['v_max'] = 0.5         # max velocity              (units per second)


#--- MAIN --------------------------------------------------------------------+


def run(settings, biome):
    """Beasts seek a set amount of food per generation"""
    #--- POPULATE THE ENVIRONMENT WITH FOOD ---------------+
    foods = []
    for i in range(0,biome.food_left):
        foods.append(Food(settings))

    #--- POPULATE THE ENVIRONMENT WITH ORGANISMS ----------+
    beasts = []
    for i in range(0,settings['init_beasts']):
        beasts.append(Beast(settings))

    #--- CYCLE THROUGH EACH GENERATION --------------------+
    for gen in range(0, settings['gens']):
        
        print("GEN: " + str(gen) + "\n")
        print("Starting Food: " + str( len(foods)) )
        
        print("Starting beasts : " + str( len(beasts) ) + "\n")
        print("-----------------------------------------------------------")
        # SIMULATE
        beasts = simulate_beasts(settings, screen, biome, beasts, foods, gen)

        # EVOLVE
        beasts = newgen(settings, beasts)
        print("IT IS A GOOD DAY TO DIE\n")

        print("Ending Food  : " + str( len(foods)) )
        
        print("Ending beasts : " + str( len(beasts)) + "\n")
        
        print("===========================================================")
        

        biome = newseason(settings, biome)
        
        foods = []
        for i in range(0,biome.food_left):
#        for i in range(0,10):
            foods.append(Food(settings))
            


#--- RUN ----------------------------------------------------------------------+
biome = Biome(settings);
run(settings, biome)


waiting = True
print("Press enter to end")

#pygame.draw.circle(screen, (255,255,255), (400,300),50,100)
#pygame.display.update()
#circle(surface, color, center, radius) -> Rect
#circle(surface, color, center, radius, width=0) -> Rect
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            waiting = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                pygame.quit()
                waiting = False

#--- END ----------------------------------------------------------------------+