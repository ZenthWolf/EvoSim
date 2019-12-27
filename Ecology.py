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

from math import radians
from math import sin
from math import cos

from Evo_Functions import (dist, orientation, circ_area, circ_overlap,
                           start_border_x, start_border_y)

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
    
    # MANAGE ECOSYSTEM ENTITIES
    def populate_foods(self, settings, num_foods):
        for i in range(0, num_foods):
            self.foods.append(Food(settings))
    
    def populate_beasts(self, settings, num_beasts):
        for i in range(0, num_beasts):
            self.beasts.append(Beast(settings))
    
    def consume_food(self, food):
        self.foods.remove(food)
    
    def kill_beast(self, beast):
        self.beasts.remove(beast)
    
    # SIMULATION METHODS
    def time_step_beasts(self,settings):
        """Calculate next timestep for beasts"""
        for beast in self.beasts:
            
            if beast.eats < 2 and len(self.foods) > 0:
                beast.seek_food(self)
            elif beast.eats == 0 and len(self.foods) == 0:
                self.kill_beast(beast)
            elif not beast.sheltering:
                beast.seek_shelter(self)
            
            beast.update_vel(settings)
            beast.update_pos(settings)
    
    def check_beast_exposure(self):
        for beast in self.beasts:
            if beast.d_targ > 0.075:
                self.kill_beast(beast)
    
    def all_beasts_sheltered(self):
        sheltered = True
        for beast in self.beasts:
            if not beast.sheltering:
                sheltered = False
                break
        
        return sheltered
    
    def draw_biome(self, screen):
        screen.fill((0,0,0))
        for food in self.foods:
            food.Draw(screen)
        for beast in self.beasts:
            beast.Draw(screen)
        pygame.display.update()
    
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            else:
                pass
    
    
    def simulate_beasts(self, settings, screen):
        """Simulate beasts seeking nearest food and returning to shelter"""
        total_time_steps = int(settings['gen_time'] / settings['dt'])
        
        for t_step in range(0, total_time_steps, 1):
            if not self.all_beasts_sheltered():
                self.time_step_beasts(settings)
                self.draw_biome(screen)
                self.handle_events()
                pygame.time.delay(int(settings['dt']*1000))
            else:
                break
        
        self.check_beast_exposure()
    
    # NEW GENERATION
    
    def breed_beasts(self, settings):
        """Create the next generation of beasts and re-init"""
        _new_beasts = 0
        for beast in self.beasts:
            if beast.eats >= 2:
                _new_beasts += 1
            
            beast.d_targ = 100       # distance to nearest food/shelter
            beast.r_targ = 0         # orientation to nearest food/shelter (degrees)
            beast.eats = 0           # food eaten this generation
            beast.sheltering = False # Going out into the world again
        self.populate_beasts(settings, _new_beasts)
        
        print("IT IS A GOOD DAY TO DIE\n")
        print("Ending Food  : " + str( len(self.foods)) )
        print("Ending beasts : " + str( len(self.beasts)) + "\n")
        print("===========================================================")
    
    def grow_food(self, settings):
        """Set food for next generation"""
        self.foods = []
        self.populate_foods(settings, settings['food_num'])
    
    def next_season(self, settings):
        self.breed_beasts(settings)
        self.grow_food(settings)


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
        small_step_speed = self.d_targ/settings['dt']
        
        self.v= min(small_step_speed, self.v_max)
    
    # UPDATE POSITION
    def update_pos(self, settings):
        """The beast walks!"""
        dx = self.v * cos(radians(self.r_targ)) * settings['dt']
        dy = self.v * sin(radians(self.r_targ)) * settings['dt']
        self.x += dx
        self.y -= dy
    
    # FIND FOOD
    def seek_food(self, biome):
        self.d_targ = 100
        self.r_targ = 0
        for food in biome.foods:
            food_dist = dist(self.x, self.y, food.x, food.y)
            
            if food_dist <= 0.075:
                self.eats += food.energy
                biome.consume_food(food)
#                biome.food_left -= 1
            
            elif food_dist < self.d_targ:
                self.d_targ = food_dist
                self.r_targ = orientation(self.x, self.y, food.x, food.y)
    
    def seek_shelter(self, biome):
        """Go to the nearest point on border and shelter there"""
        shelter = []
        # Distance to each border
        shelter.append(biome.x_max - self.x)
        shelter.append(self.x - biome.x_min)
        shelter.append(biome.y_max - self.y)
        shelter.append(self.y - biome.y_min)
        
        shelter_choice = shelter.index(min(shelter))
        
        self.d_targ = shelter[shelter_choice]
        if self.d_targ == 0.0:
            self.sheltering = True
            self.v = 0
        
        elif shelter_choice == 0:
            self.r_targ = 0
        elif shelter_choice == 1:
            self.r_targ = 180
        elif shelter_choice == 2:
            self.r_targ = 270
        elif shelter_choice == 3:
            self.r_targ = 90
        else:
            self.r_targ = 45
    
    # DRAWING
    def Draw(self, screen):
        """Draw to screen"""
        pygame.draw.circle(screen, self.color,
                           (self.ScreenX(), self.ScreenY()), self.size)


class Plant():
    def __init__(self, settings, _init_energy = 10, _init_nutrients = 10):
        # POSITION
        self.x = uniform(settings['x_min'], settings['x_max'])
        self.y = uniform(settings['y_min'], settings['y_max'])
        
        # COUNTERS AND FLAGS
        self.energy = _init_energy
        self.nutrients = _init_nutrients
        
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
        
        # GROWTH RATIO - BOTH MATURE AT FULL ENERGY
        self._stemRatio = self.stemEnergyNeed(settings, self.height_max,
                                              self.width_max, self.leaves_max) \
                                            / self.energyNeedMax(settings)
            
        self._rootRatio = 1 - self._stemRatio
        
        ## ENERGY/NUTRIENT REQUIREMENT CALCULATION
        # STEM ENERGY
        def heightEnergyCost(self, settings, _height):
            return _height*settings['stem_height_cost']
        
        def widthEnergyCost(self, settings, _width):
            return (_width**2)*settings['stem_width_cost']
        
        def leafEnergyCost(self, settings, _leaves):
            return (_leaves**1.5)*settings['stem_leaf_cost']
        
        def stemEnergyNeed(self, settings, _height = self.height,
                           _width = self.width, _leaves = self.leaves):
            """Energy to maintain the flower/stem"""
            return heightEnergyCost(settings, _height) \
                  *widthEnergyCost(settings, _width)   \
                  *leafEnergyCost(settings, _leaves)
        
        # ROOT ENERGY
        def rootWidthEnergyCost(self, settings, _width):
            return (_width**2)*settings['root_width_cost']
        
        def rootEnergyCost(self, settings, _rootSize):
            return (_rootSize**1.5)*settings['root_size_cost']
        
        def rootEnergyNeed(self, settings, _width = self.rootWidth,
                           _rootSize = self.rootSize):
            return rootWidthEnergyCost(self, settings, _width) \
                  *rootEnergyCost(self, settings, _rootSize)
        
        def energyNeed(self, settings):
            return ( self.stemEnergyNeed(settings)
                   + self.rootEnergyNeed(settings) )
        
        def energyNeedMax(self, settings):
            return ( self.stemEnergyNeed(settings, self.height_max,
                                         self.width_max, self.leaves_max)
                   + self.rootEnergyNeed(settings, self.rootWidth_max,
                                          self.rootSize_max) )
        
        # STEM NUTRIENTS
        def heightNutrientCost(self,settings, _height):
            return _height*settings['stem_height_nutrient']
        
        def widthNutrientCost(self,settings, _width):
            return (_width**2)*settings['stem_width_nutrient']
        
        def leafNutrientCost(self,settings, _leaves):
            return (_leaves**1.5)*settings['stem_leaf_nutrient']
        
        def stemNutrientNeed(self,settings, _height = self.height,
                             _width = self.width, _leaves = self.leaves):
            return heightNutrientCost(settings, _height) \
                  *widthNutrientCost(settings, _width)   \
                  *leafNutrientCost(settings, _leaves)
        
        # ROOT NUTRIENTS
        def rootWidthNutrientCost(self, settings, _width = self.rootWidth):
            return (_width**2)*settings['root_width_nutrient']
        
        def rootNutrientCost(self, settings, _rootSize = self.rootSize):
            return (_rootSize**1.5)*settings['root_size_nutrient']
        
        def rootNutrientNeed(self, settings, _width = self.rootWidth,
                             _rootSize = self.rootSize):
            return rootWidthNutrientCost(self, settings, _width) \
                  *rootNutrientCost(self, settings, _rootSize)
        
        def nutrientNeed(self, settings):
            return ( self.stemNutrientNeed(settings)
                   + self.rootNutrientNeed(settings) )
        
        def nutrientNeedMax(self, settings):
            return ( self.stemNutrientNeed(settings, self.height_max,
                                         self.width_max, self.leaves_max)
                   + self.rootNutrientNeed(settings, self.rootWidth_max,
                                          self.rootSize_max) )
        
        # GROWING METHODS
        def findGrowRate(self):
            """Balances energy and nutrients for growth"""
            _growRate = self.energy/(self.energyNeedMax(settings) - self.energyNeed(settings))
            
            _nutrientNeed = _growRate*(self.nutrientNeedMax(settings) - self.nutrientNeed(settings))
                
            if _nutrientNeed > self.nutrients:
                _growRate = _growRate*(self.nutrients/_nutrientNeed)
            
            return _growRate
        
        def growHeight(self, _growRate):
            self.height += _growRate*(self.height_max - self.height)
        
        def growWidth(self, _growRate):
            self.width += _growRate*(self.width_max - self.width)
        
        def growLeaves(self, _growRate):
            self.leaves += _growRate*(self.leaves_max - self.leaves)
        
        def growStem(self, _growRate):
            self.growHeight(_growRate)
            self.growWidth(_growRate)
            self.growLeaves(_growRate)
        
        def growRootWidth(self, _growRate):
            self.rootWidth += _growRate*(self.rootWidth_max - self.rootWidth)
        
        def growRootSize(self, _growRate):
            self.rootSize += _growRate*(self.rootSize_max - self.rootSize)
        
        def growRoot(self, _growRate):
            self.growRootWidth(_growRate)
            self.growRootSize(_growRate)
        
        def grow(self, settings):
            # All parameters reach max at same time
            if self.height < self.height_max :
                # Energy inefficiency in growth
                self.energy = self.energy*settings['growth_efficiency']
                
                _growRate = self.findGrowRate()
                
                self.growStem(_growRate)
                self.growRoot(_growRate)
