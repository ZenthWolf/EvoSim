# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 18:59:44 2019

Author: S. Rose
@author: ZenthWolf

Simple Evolution Simulator in Python
"""
#--- DEPENDANCIES ------------------------------------------------------------+

from random import randint
from random import uniform

from math import sqrt
from math import radians
from math import degrees
from math import sin
from math import cos
from math import atan2

#--- CONSTANTS ---------------------------------------------------------------+

#Put this in text file?
settings = {}

# FIELD BORDERS
settings['x_min'] = -2.0        # west
settings['x_max'] =  2.0        # east
settings['y_min'] = -2.0        # south
settings['y_max'] =  2.0        # north

# EVOLUTION SETTINGS
settings['init_pop'] = 1        #starting population
settings['food_num'] = 50      # number of food particles
settings['gens'] = 10            # number of generations

# SIMULATION SETTINGS
settings['gen_time'] = 30       # generation length         (seconds)
settings['dt'] = 0.04           # simulation time step      (dt)
settings['v_max'] = 0.5         # max velocity              (units per second)

#--- FUNCTIONS ---------------------------------------------------------------+

def dist(x1,y1,x2,y2):
    return sqrt((x2-x1)**2 + (y2-y1)**2)

def orientation(x1,y1,x2,y2): # from 1 -> 2
    d_x = x2 - x1
    d_y = y2 - y1
    theta = degrees(atan2(d_y, d_x))
    return theta

def start_border_x(border):
    if border == 0:  # west border
        return settings['x_min']
        
    elif border == 1:  # east border
        return settings['x_max']

    elif border == 2 or border == 3:  # south/north borders
        return uniform(settings['x_min'], settings['x_max'])
    
    else:
        return 100000   # until better exception handling

def start_border_y(border):
    if border == 0 or border == 1:  # west/east borders
        return uniform(settings['y_min'], settings['y_max'])
        
    elif border == 2:  # south border
        return settings['y_min']

    elif border == 3:  # north border
        return settings['y_max']
    
    else:
        return 100000   # until better exception handling        


def simulate(settings, biome, beasts, foods, gen):

    total_time_steps = int(settings['gen_time'] / settings['dt'])

    #--- CYCLE THROUGH EACH TIME STEP ---------------------+
    for t_step in range(0, total_time_steps, 1):

        # CHECK FOR GOALS
        for beast in beasts:
            if beast.eats < 2 and biome.food_left > 0:
                for food in foods:
                    food_dist = dist(beast.x, beast.y, food.x, food.y)

                    # UPDATE FOOD
                    if food_dist <= 0.075:
                        beast.eats += food.energy
                        del foods[foods.index(food)]
                        biome.food_left -= 1

                    # RESET DISTANCE AND HEADING TO NEXT TARGET
                    beast.d_targ = 100
                    beast.r_targ = 0

        # CALCULATE HEADING TO NEAREST GOAL
        for beast in beasts:
            # IF FEEDING
            if beast.eats < 2 and biome.food_left > 0:
                for food in foods:

                    # CALCULATE DISTANCE TO SELECTED FOOD PARTICLE
                    food_dist = dist(beast.x, beast.y, food.x, food.y)

                    # DETERMINE IF THIS IS CLOSER THAN CURRENT TARGET
                    if food_dist < beast.d_targ:
                        beast.d_targ = food_dist
                        beast.r_targ = orientation(beast.x, beast.y, food.x, food.y)
            # IF DYING
            elif beast.eats == 0 and biome.food_left == 0:
                del beasts[beasts.index(beast)]
            # IF SHELTERING
            else:
                shelter = []
                shelter.append(beast.x - biome.x_min)
                shelter.append(biome.x_max - beast.x)
                shelter.append(beast.y - biome.y_min)
                shelter.append(biome.y_max - beast.y)
                
                shelter_choice = shelter.index(min(shelter))
                
                beast.d_targ = shelter[shelter_choice]
                if shelter_choice == 0:
                    beast.r_targ = 0
                elif shelter_choice == 1:
                    beast.r_targ = 180
                elif shelter_choice == 2:
                    beast.r_targ = 270
                else:
                    beast.r_targ = 90

        # UPDATE ORGANISMS POSITION AND VELOCITY
        for beast in beasts:
            beast.update_vel(settings)
            beast.update_pos(settings)

    #CHECK FOR FAILED TO SHELTER:
    for beast in beasts:
        if beast.d_targ > 0.075:
             del beasts[beasts.index(beast)]
    
    return beasts

def newgen(settings, beasts):
    for beast in beasts:
        if beast.eats >= 2:
            beasts.append(Beast(settings))
        
        beast.d_targ = 100   # distance to nearest food/shelter
        beast.r_targ = 0     # orientation to nearest food/shelter (degrees)
        beast.eats = 0       # food eaten this generation

    return beasts
    
def newseason(settings, biome):
    biome.food_left = settings['food_num']
    
    return biome
    

#--- CLASSES -----------------------------------------------------------------+
class Biome:

    def __init__(self, settings):
        self.food_left = settings['food_num']  # food remaining
        self.x_min = settings['x_min']         # west border
        self.x_max = settings['x_max']         # east border
        self.y_min = settings['y_min']         # south border
        self.y_max = settings['y_max']         # north border

class Food():
    def __init__(self, settings):
        self.x = uniform(settings['x_min'], settings['x_max'])
        self.y = uniform(settings['y_min'], settings['y_max'])
        self.energy = 1
        
class Beast():
    def __init__(self, settings):

        start = randint(0,3)
        
        self.x = start_border_x(start)          # position (x)
        self.y = start_border_y(start)          # position (y)

        self.v = settings['v_max']
        self.v_max = settings['v_max']

        self.d_targ = 100   # distance to nearest food/shelter
        self.r_targ = 0     # orientation to nearest food/shelter (degrees)
        self.eats = 0       # food eaten this generation
    
    # UPDATE VELOCITY
    def update_vel(self, settings):
        small_step_speed = self.d_targ/settings['dt']
        
        self.v= min(small_step_speed, self.v_max)
        
    # UPDATE POSITION
    def update_pos(self, settings):
        dx = self.v * cos(radians(self.r_targ)) * settings['dt']
        dy = self.v * sin(radians(self.r_targ)) * settings['dt']
        self.x += dx
        self.y += dy

#--- MAIN --------------------------------------------------------------------+


def run(settings, biome):

    #--- POPULATE THE ENVIRONMENT WITH FOOD ---------------+
    foods = []
    for i in range(0,biome.food_left):
        foods.append(Food(settings))

    #--- POPULATE THE ENVIRONMENT WITH ORGANISMS ----------+
    beasts = []
    for i in range(0,settings['init_pop']):
        beasts.append(Beast(settings))

    #--- CYCLE THROUGH EACH GENERATION --------------------+
    for gen in range(0, settings['gens']):
        
        print("GEN: " + str(gen) + "\n")
        print("Starting Food: " + str( len(foods)) )
        print("food_num     : " + str( settings['food_num']) )
        print("food_left    : " + str( biome.food_left ) + "\n")
        
        print("Starting beasts : " + str( len(beasts) ) + "\n")
        print("-----------------------------------------------------------")
        # SIMULATE
        beasts = simulate(settings, biome, beasts, foods, gen)

        # EVOLVE
        beasts = newgen(settings, beasts)
        print("IT IS A GOOD DAY TO DIE\n")

        print("Ending Food  : " + str( len(foods)) )
        print("food_left    : " + str( biome.food_left ) + "\n")
        
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