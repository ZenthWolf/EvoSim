# EvoSim
Evolution Simulator written in Python

Current operation:

    1. Biome generates a set amount of food each generation.
    2. Beasts roam for up to 2 food - seek nearest food
    3. After all food is eaten, or a beast eats 2 food, they return to the border to "shelter"
    4. Any beast that fails to eat at least 1 food or fails to reach shelter (the border) in time dies.
    5. Each beast that eats 2 food adds a new beast to the next generation.
    
    Current output:
    1. Text output of some information
    2. Inoperoble pygame window for future visualization
    
Completed tasks:
    - Basic population growth
    
Current priority:
    - (short term) Graph statistics
    - (short term) Alternative food search? (forced interractions)
    - (mid term)   Live plotting of generations in development
    - (mid term)   Allow for more interesting plant populations (food sources)
    - (long term)  Real time visualization of a generation
    - (long term)  Simulation controls while running
        - print statistics on demand
        - speed up/skip live visualization
        - manual injection of mutations or environmental changes

Code goals:
Various evolution simulation tests (single pop evolution, pred-prey models, etc)

Personal Development goals:
Using Git with commandline (vs integrated as in Visual Studio)
Familiarity with Python
Familiarity with Spyder IDE

Specific Development Targets:
For sim:
Simple populations
   1. Simple pop growth (complete)
   2. Simple competition

Energy System
    1. Energy -> survival/reproduction chances
    2. Trophic inefficiencies
    3. Seasonal/weather variation on energy usage

Simple Graphics
   - Need pygame?

For self:
2D Plotting in python
   - Plotting should be easy, but...
   - real time anims will require pygame
   
3D Plottingg in python
   - These plots are for graphs only, visualization is to be 2D


Acknowledgements:

    - Code inspiration from Nathan Rooy's 'evolving-simple-organisms' repository
        - GitHub: https://github.com/nathanrooy/evolving-simple-organisms
        - Usage: Began by tearing apart code to bare bones, basic functions and classes were reduced to the simplest case for inspiration
        - Divergences: removed neural net, starting with different survival rules, plan to implement multiple organisms
        
    - Alternative set ups inspire by primer (on youtube)/Justin Helps (github)
        - Github: https://github.com/Helpsypoo/primer
        - Youtube: https://www.youtube.com/channel/UCKzJFdi57J53Vr_BkTfN3uQ
        - No code referenced, but background discussion may inform different versions
        - Less natural starting condition for animals (at boundary) example of inspiration taken