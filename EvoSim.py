# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 18:59:44 2019

Author: S. Rose
@author: ZenthWolf

Simple Evolution Simulator in Python
"""
#--- DEPENDANCIES ------------------------------------------------------------+

from Ecology import *

#--- CONSTANTS ---------------------------------------------------------------+

#Put this in text file?
settings = {}

# FIELD PARAMETERS
# BORDERS
settings['x_min'] = -2.0        # west
settings['x_max'] =  2.0        # east
settings['y_min'] = -2.0        # south
settings['y_max'] =  2.0        # north

# SUN AND SOIL
settings['sunshine'] = 10       # Sunlight energy density
settings ['nutrients'] = 10     # Soil nutrient density

# EVOLUTION SETTINGS
settings['food_num'] = 50       # number of food particles (for beast sim)
settings['gens'] = 10           # number of generations

# SIMULATION SETTINGS
settings['gen_time'] = 30       # generation length         (seconds)
settings['dt'] = 0.04           # simulation time step      (dt)

# BEAST PARAMETERS
settings['init_beasts'] = 1     #starting population
settings['v_max'] = 0.5         # max velocity              (units per second)

# PLANT PARAMETERS
settings['absorption'] = 0.85   # Max efficiency of sunlight absoption
settings['growth_efficiency'] = 0.8 #Growing costs more energy than maintaining
# Energy Costs
settings['stem_height_cost'] = 0.5
settings['stem_width_cost'] = 0.25
settings['stem_leaf_cost'] = 0.1

settings['root_width_cost'] = 0.25
settings['root_size_cost'] = 0.1

#Nutrient Costs
settings['stem_height_nutrient'] = 0.5
settings['stem_width_nutrient'] = 0.25
settings['stem_leaf_nutrient'] = 0.1

settings['root_width_nutrient'] = 0.1
settings['root_size_nutrient'] = 0.05 

#--- MAIN --------------------------------------------------------------------+


def run(settings, biome):

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
        beasts = simulate_beasts(settings, biome, beasts, foods, gen)

        # EVOLVE
        beasts = newgen(settings, beasts)
        print("IT IS A GOOD DAY TO DIE\n")

        print("Ending Food  : " + str( len(foods)) )
        
        print("Ending beasts : " + str( len(beasts)) + "\n")
        
        print("===========================================================")
        

        biome = newseason(settings, biome)
        
        foods = []
        for i in range(0,biome.food_left):
            foods.append(Food(settings))
            

    pass


#--- RUN ----------------------------------------------------------------------+

biome = Biome(settings);
run(settings, biome)

#--- END ----------------------------------------------------------------------+