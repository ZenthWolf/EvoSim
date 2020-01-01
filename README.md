# EvoSim
Evolution Simulator written in Python

Current operation:

    BEAST SIMULATION
    1. Biome grows food from previous generations starting population (with crowding factor).
    2. Beasts roam for up to 2 food - seek nearest food
    3. After all food is eaten, or a beast eats 2 food, they return to the border to "shelter"
    4. Calculate casualties:
        - Any beast that does not eat, has a 50% chance of gaining 1 food
        - Any beast with 0 food, dies.
        - Any beast with 1 food, has a 50% chance to die.
    5. Each beast that eats 2 food adds a new beast to the next generation.
    
    PLANT SIMULATION
    NOTE: Logic not fully implemented
    1. Each plant absorbs sunlight based on size and overlap of taller competitors
    2. Each plant absorbs nutrients based on root rize and overlap with competitors
    3. Each time step, energy is used to survive, then to grow.
        - Survival costs based on current size
    
    Current output:
    1. Text output of some information
    2. Realtime visualization of beast movement and food placement.
    3. Realtime visualization of plant size
    4. Graph representation of population (line chart and stacked area)
        - Currently only displayed, saving not implemented
    
Completed tasks:
    - Basic population growth
    - Simple food growth has a crowding factor
    - Simple plant growth and competition (no reproduction)
    - Real time visualization and graphing.
    
Current priority:
    - (short term) Alternative food search? (forced interractions)
    - (mid term) Basic neural network decision making for beasts
    - (mid term) Implement plants as food source
    - (long term) Real time energy budget
        - Requires different biology, search strategy, or neural network implementation first
    - (long term)  Simulation controls while running
        - print statistics on demand
        - speed up/skip live visualization
        - manual injection of mutations or environmental changes

Code goals:
Various evolution simulation tests (single pop evolution, pred-prey models, etc)

Personal Development goals:
MET Using Git with commandline (vs integrated as in Visual Studio)
MET Familiarity with Python
MET Familiarity with Spyder IDE

Implement basic neural network
Search/pathfinding algorithm implementation
    - First need to be able to draw/generate natural barriers to movement


Specific Development Targets:
For sim:
Simple populations
   1. Simple pop growth (complete)
   2. Simple competition

Energy System
    1. Energy -> survival/reproduction chances
    2. Trophic inefficiencies
    3. Seasonal/weather variation on energy usage

MET Simple Graphics

For self:
MET 2D Plotting in python
   
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
    
    - Matplot integration with pygame: http://www.pygame.org/wiki/MatplotlibPygame