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


def simulate_beasts(settings, screen, biome, beasts, foods, gen):
    """Simulate beasts seeking nearest food and returning to shelter"""
    total_time_steps = int(settings['gen_time'] / settings['dt'])

    #--- CYCLE THROUGH EACH TIME STEP ---------------------+
    for t_step in range(0, total_time_steps, 1):
        # ASSUME THIS IS LAST STEP UNTIL PROVEN OTHERWISE
        complete = True
        
        for beast in beasts:
            # IF NOT SHELTERING, CONTINUE SIMULATION
            if complete and not beast.sheltering:
                complete = False

           # IF EATING
            if beast.eats < 2 and biome.food_left > 0:
                for food in foods:

                    # CALCULATE DISTANCE TO SELECTED FOOD PARTICLE
                    food_dist = dist(beast.x, beast.y, food.x, food.y)
                    
                    # EAT IF CLOSE
                    if food_dist <= 0.075:
                        beast.eats += food.energy
                        del foods[foods.index(food)]
                        biome.food_left -= 1
                    # RESET DISTANCE AND HEADING TO NEXT TARGET
                    beast.d_targ = 100
                    beast.r_targ = 0

            # IF SEEKING FOOD
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
        
        #END IF ALL BEASTS SHELTERED
        if complete:
            break


    #CHECK FOR FAILED TO SHELTER:
    for beast in beasts:
        if beast.d_targ > 0.075:
             del beasts[beasts.index(beast)]
    
    return beasts

def simulate_plants(settings, biome, plants, gen):
    """Simulate plant growth and competition"""
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
        
        # RESOURCES
        self.food_left = settings['food_num']  # food remaining

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
    
    # DRAWING
    def Draw(self, screen):
        """Draw to screen"""
        pygame.draw.circle(screen, self.color, (self.ScreenX(), self.ScreenY()), self.size)
    
class Plant():
    def __init__(self, settings):
        # POSITION
        self.x = uniform(settings['x_min'], settings['x_max'])
        self.y = uniform(settings['y_min'], settings['y_max'])
        
        # COUNTERS AND FLAGS
        self.energy = 0
        self.nutrients = 0
        
        # RIVAL LISTS
        self.sunRivals = []
        self.rootRivals = []
        
        # ABOVE GROUND STATS
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

         ##########################################
        #        ENTERING THE EYE PAIN ZONE        #
         ##########################################
        
        ## ENERGY/NUTRIENT REQUIREMENT CALCULATION
        # ENERGY
        def stemEnergy_need(self, settings):
            """Energy to maintain the flower/stem"""
            return self.height * settings['stem_height_cost'] + (self.width ** 2) * settings['stem_width_cost'] + (self.leaves ** 1.5) * settings['stem_leaf_cost']
        def rootEnergy_need(self, settings):
            """Energy to maintain the root system"""
            return (self.rootWidth ** 2) * settings['root_width_cost'] + (self.rootSize ** 1.5) * settings['root_size_cost']
        def energy_need(self, settings):
            """Total energy requirement to maintain plant"""
            return stemEnergy_need(settings) + rootEnergy_need(settings)

        # NUTRIENTS
        def stemNutrient_need(self, settings):
            """Nutrients to maintain the flower/stem"""
            return self.height * settings['stem_height_nutrient'] + (self.width ** 2) * settings['stem_width_nutrient'] + (self.leaves ** 1.5) * settings['stem_leaf_nutrient']
        def rootNutrient_need(self, settings):
            """Nutrients to maintain the root system"""
            return (self.rootWidth ** 2) * settings['root_width_nutrient'] + (self.rootSize ** 1.5) * settings['root_size_nutrient']
        def nutrient_need(self, settings):        
            """Total mutrients requirement to maintain plant"""
            return stemNutrient_need(settings) + rootNutrient_need(settings)
        
        #GROW CALCULATION
        #### WHAT DA FU--
        def grow(self, settings):
            """Tries to grow the plant, so that root/stem finish simulatenously"""
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
            