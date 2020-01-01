# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 18:59:44 2019

Author: S. Rose
@author: ZenthWolf

Simple Evolution Simulator in Python
"""
#--- DEPENDANCIES ------------------------------------------------------------+

import pygame

from Ecology import Biome

#--- Graphics Parameters -----------------------------------------------------+
graphic_settings = {}

graphic_settings['screen_size'] = (1024, 768)
graphic_settings['window_title'] = "Ecosim"

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
settings['sunshine'] = 10        # Sunlight energy density
settings ['nutrients'] = 8      # Soil nutrient density

# EVOLUTION SETTINGS
settings['food_num'] = 5        # number of food particles (for beast sim)
settings['gens'] = 200

# SIMULATION SETTINGS
settings['gen_time'] = 10       # generation length         (seconds)
settings['dt'] = 0.04           # simulation time step      (seconds)

# BEAST PARAMETERS
settings['init_beasts'] = 1
settings['v_max'] = 0.5         # max velocity              (units per second)


# PLANT PARAMETERS
settings['init_plants'] = 1
settings['absorption'] = 0.7        # Max efficiency of sunlight absoption
settings['growth_efficiency'] = 0.7 #Growing costs more energy than maintaining
settings['init_energy'] = .1
settings['init_nutrients'] = .1
# Energy Costs
settings['stem_height_cost'] = 3.5
settings['stem_width_cost'] = 1.5
settings['stem_leaf_cost'] = 0.75

settings['root_width_cost'] = 1.5
settings['root_size_cost'] = 1

#Nutrient Costs
settings['stem_height_nutrient'] = 3.5
settings['stem_width_nutrient'] = 1.25
settings['stem_leaf_nutrient'] = 1

settings['root_width_nutrient'] = 1
settings['root_size_nutrient'] = 0.

# FLAGS
settings['rand_survival'] = True
settings['rand_kill'] = True

#--- MAIN --------------------------------------------------------------------+


def run(settings, biome):
    """Beasts seek a set amount of food per generation"""
    #--- CYCLE THROUGH EACH GENERATION --------------------+
    for gen in range(0, settings['gens']):
        biome.plotBeast()
        
        print("GEN: " + str(gen) + "\n")
        print("Starting Food: " + str( len(biome.foods)) )
        
        print("Starting beasts : " + str( len(biome.beasts)) )
        
        print("Starting plants : " + str( len(biome.plants) ) + "\n")
        print("-----------------------------------------------------------")
        # SIMULATE
        biome.simulateBeasts(settings, screen)
        #biome.simulatePlants(settings, screen)
        
        biome.nextSeason(settings)


#--- Init Screen -------------------------------------------------------------+
pygame.init()
screen = pygame.display.set_mode(graphic_settings['screen_size'])
pygame.display.set_caption(graphic_settings['window_title'])


#--- RUN ---------------------------------------------------------------------+

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

#--- END ---------------------------------------------------------------------+