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
    return sqrt((x2-x1)**2 + (y2-y1)**2)

def orientation(x1,y1,x2,y2): # from 1 -> 2
    d_x = x2 - x1
    d_y = -y2 + y1
    theta = degrees(atan2(d_y, d_x))
    return theta

def circ_area(r):
    return pi*(r**2)

def circ_overlap(d, r1, r2): # Overlap of 2 circles- replace with diamond if time is costly
    return (r1**2)*acos((d**2 + r1**2 - r2**2)/(2*d*r1)) + (r2**2)*acos((d**2 + r2**2 - r1**2)/(2*d*r2)) - 0.5*sqrt((-d+r1+r2)*(d-r1+r2)*(d+r1-r2)*(d+r1+r2))

def start_border_x(settings, border):
    if border == 0:  # west border
        return settings['x_min']
        
    elif border == 1:  # east border
        return settings['x_max']

    elif border == 2 or border == 3:  # south/north borders
        return uniform(settings['x_min'], settings['x_max'])
    
    else:
        return 100000   # until better exception handling

def start_border_y(settings, border):
    if border == 0 or border == 1:  # west/east borders
        return uniform(settings['y_min'], settings['y_max'])
        
    elif border == 2:  # north border
        return settings['y_min']

    elif border == 3:  # south border
        return settings['y_max']
    
    else:
        return 100000   # until better exception handling, exile mistaken beasts to the harsh desert!        


def simulate_beasts(settings, screen, biome, beasts, foods, gen):

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
                # Distance to each border
                shelter.append(biome.x_max - beast.x)
                shelter.append(beast.x - biome.x_min)
                shelter.append(biome.y_max - beast.y)
                shelter.append(beast.y - biome.y_min)
                
                
                shelter_choice = shelter.index(min(shelter))
                
                beast.d_targ = shelter[shelter_choice]
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
        for beast in beasts:
            beast.update_vel(settings)
            beast.update_pos(settings)
        
        # DRAW SCREEN
        screen.fill((0,0,0))
        for food in foods:
            food.Draw(screen)
        for beast in beasts:
            beast.Draw(screen)
        pygame.display.update()
        pygame.time.delay(int(settings['dt']*1000))
        for event in pygame.event.get():
            pass


    #CHECK FOR FAILED TO SHELTER:
    for beast in beasts:
        if beast.d_targ > 0.075:
             del beasts[beasts.index(beast)]
    
    return beasts

def simulate_plants(settings, biome, plants, gen):

    total_time_steps = int(settings['gen_time'] / settings['dt'])

    #--- CYCLE THROUGH EACH TIME STEP ---------------------+
    for t_step in range(0, total_time_steps, 1):

        # CHECK FOR RIVALS
        for plant in plants:
            for rival in plants:
                if not plant == rival:
                    rival_dist = dist(plant.x, plant.y, rival.x, rival.y)

                    # UPDATE RIVALS
                    plant.sunRivals = []
                    plant.rootRivals = []
                    if plant.width + rival.width >= rival_dist and plant.height < rival.height:  # DUNK ON THE SHORT PLANTS!
                        plant.sunRivals.append([rival.height, plants.index(rival)])
                    if plant.rootWidth + rival.rootWidth >= rival_dist:
                        plant.rootRivals.append(plants.index(rival))
        
        # COMPETE FOR SUNLIGHT
        for plant in plants:
            available_energy = circ_area(plant.width)*settings['sunshine']
            for rival in plant.sunRivals:
                competition_area = circ_overlap(dist(plant.x, plant.y, rival.x, rival.y), plant.width, rival.width)
                fractional_area = competition_area/circ_area(plant.width)
                available_energy -= available_energy * fractional_area * rival.leaves * settings['absorption']
             
            plant.energy += available_energy * plant.leaves * settings['absorption']

        # COMPETE FOR NUTRIENTS
        for plant in plants:
            available_nutrients = circ_area(plant.rootWidth)*settings['nutrients']
            rival_root_factor = 0
            for rival in plant.rootRivals:
                competition_area = circ_overlap(dist(plant.x, plant.y, rival.x, rival.y), plant.rootWidth, rival.rootWidth)
                
                rival_root_factor += competition_area * rival.rootSize
             
            plant.nutrients += available_nutrients * plant.rootSize / rival_root_factor
        
        # ENERGY/NUTRIENT BUDGET
        for plant in plants:
            plant.energy -= plant.energy_need
            plant.nutrients -= plant.nutrient_need
            
            if plant.energy < 0 or plant.nutrients == 0:
                del plants[plants.index(plant)]
            
            else:
                plant.grow(settings)

    return plants

    
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
        
        self.color = (50,255,50)
    
    def ScreenX(self):
        return int((self.x + 2)*500/(4) + 10)
    def ScreenY(self):
        return int((self.y + 2)*500/(4) + 10)
    
    def Draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.ScreenX(), self.ScreenY()), 3)
        
class Beast():
    def __init__(self, settings):

        start = randint(0,3)
        
        self.x = start_border_x(settings, start)       # position (x)
        self.y = start_border_y(settings, start)       # position (y)

        self.v = settings['v_max']
        self.v_max = settings['v_max']

        self.d_targ = 100   # distance to nearest food/shelter
        self.r_targ = 0     # orientation to nearest food/shelter (degrees)
        self.eats = 0       # food eaten this generation
        self.color = (255,155,50)
        
    def ScreenX(self):
        return int((self.x + 2)*500/(4) + 10)
    def ScreenY(self):
        return int((self.y + 2)*500/(4) + 10)
    
    # UPDATE VELOCITY
    def update_vel(self, settings):
        small_step_speed = self.d_targ/settings['dt'] # speed to take one step to target
        
        self.v= min(small_step_speed, self.v_max)
        
    # UPDATE POSITION
    def update_pos(self, settings):
        dx = self.v * cos(radians(self.r_targ)) * settings['dt']
        dy = self.v * sin(radians(self.r_targ)) * settings['dt']
        self.x += dx
        self.y -= dy
    
    def Draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.ScreenX(), self.ScreenY()), 3)
    
class Plant():
    def __init__(self, settings):
        self.x = uniform(settings['x_min'], settings['x_max'])
        self.y = uniform(settings['y_min'], settings['y_max'])
        
        self.energy = 0
        self.nutrients = 0
        
        self.sunRivals = []
        self.rootRivals = []
        
        # ABOVE GROUND
        self.height = 0
        self.height_max = 10
        self.width = 0
        self.width_max = 0.5
        self.leaves = 0
        self.leaves_max = 1
        
        # BELOW GROUND
        self.rootWidth = 0
        self.rootWidth_max = 0.5
        self.rootSize = 0
        self.rootSize_max = 1
        
        def stemEnergy_need(self, settings):
            return self.height * settings['stem_height_cost'] + (self.width ** 2) * settings['stem_width_cost'] + (self.leaves ** 1.5) * settings['stem_leaf_cost']
        
        def rootEnergy_need(self, settings):
            return (self.rootWidth ** 2) * settings['root_width_cost'] + (self.rootSize ** 1.5) * settings['root_size_cost']
        
        def energy_need(self, settings):
            return stemEnergy_need(settings) + rootEnergy_need(settings)
        
        
        def stemNutrient_need(self, settings):
            return self.height * settings['stem_height_nutrient'] + (self.width ** 2) * settings['stem_width_nutrient'] + (self.leaves ** 1.5) * settings['stem_leaf_nutrient']
            
        def rootNutrient_need(self, settings):
            return (self.rootWidth ** 2) * settings['root_width_nutrient'] + (self.rootSize ** 1.5) * settings['root_size_nutrient']
        
        def nutrient_need(self, settings):            
            return stemNutrient_need(settings) + rootNutrient_need(settings)
        
        
        def grow(self, settings):
            # Energy costs for growing are increased, nutrient costs are flat
            self.energy = self.energy*settings['growth_efficiency']
            
            # Energy to maintain the maximum plant            
            stemEnergy_max = self.height_max * settings['stem_height_cost'] + (self.width_max ** 2) * settings['stem_width_cost'] + (self.leaves_max ** 1.5) * settings['stem_leaf_cost']
            rootEnergy_max = (self.rootWidth_max ** 2) * settings['root_width_cost'] + (self.rootSize_max ** 1.5) * settings['root_size_cost']

            # Nutrients to maintain the maximum plant
            stemNutrient_max = self.height_max * settings['stem_height_nutrient'] + (self.width_max ** 2) * settings['stem_width_nutrient'] + (self.leaves_max ** 1.5) * settings['stem_leaf_nutrient']
            rootNutrient_max = (self.rootWidth_max ** 2) * settings['root_width_nutrient'] + (self.rootSize_max ** 1.5) * settings['root_size_nutrient']
            
            # Growth ratios are determined by available energy, such that both mature at same rate
            stemRatio = stemEnergy_max / (stemEnergy_max + rootEnergy_max)
            rootRatio = rootEnergy_max / (stemEnergy_max + rootEnergy_max)
            
            stemGrowthRate = 0;
            rootGrowthRate = 0;
            
            while True: # do-loop emulation to balance nutrient and energy costs both
                #Nutrient cost has different weights
                #Energy growth can cover the remaining fractional development
                stemGrowthRate = stemRatio * self.energy / (stemEnergy_max - self.stemEnergy_need(settings))
                rootGrowthRate = rootRatio * self.energy / (rootEnergy_max - self.rootEnergy_need(settings))

                #Nutrient costs with that development rate are:
                stemNutrientRequired = stemGrowthRate * (stemNutrient_max - stemNutrient_need)
                rootNutrientRequired = rootGrowthRate * (rootNutrient_max - rootNutrient_need)
            
                
                if(stemNutrientRequired + rootNutrientRequired < self.nutrients):
                    # if sufficient nutrients to utilize all energy, proceed
                    break
                else:
                    # if insufficient nutrients, use 10% less energy
                    self.energy = self.energy*0.9
            
            ### Grow stem and root by similar division
            ### Worry intensely about not escaping the do loop
            