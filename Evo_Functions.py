# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 22:34:29 2019

@author: Zenth
"""
#--- Depencies ---------------------------------------------------------------+

from random import uniform

from math import sqrt
from math import pi
from math import degrees
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
    return ( (r1**2)*acos((d**2 + r1**2 - r2**2)/(2*d*r1))
           + (r2**2)*acos((d**2 + r2**2 - r1**2)/(2*d*r2))
           - 0.5*sqrt((-d+r1+r2)*(d-r1+r2)*(d+r1-r2)*(d+r1+r2)) )

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
        return 100000   # exile mistaken beasts to the harsh desert!  