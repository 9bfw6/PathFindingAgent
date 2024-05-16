Program Name: Path Finder in Grid World
Author: Brooks Forrest Woelfel


Program files:
search.py
searcher.py 
node.py
utils.py
grid.py
world1_enclosures.txt
world1_turfs.txt
world2_enclosures.txt
world2_turfs.txt

Driver file: 
search.py

Modules imported:
MatPlotLib
Shapely 


To run this program:
First, ensure that you have python 3.11 installed on your machine.
Next, ensure that the numpy, matplotlib, time, grid, utils, shapely, math, and 
heapq modules are all installed for your python interpretter.


Open a new terminal shell and clone this repository locally.
Next, change to the directory of this project and then type python followed by search.py. 
The default world is set to the polygons in world1_enclosures.txt and world1_turfs.txt.
The set of polygons I created are in world2_enclosures.txt and world2_turfs.txt. 
To use those worlds, navigate to search.py and change the file path when calling the gen_polygons method.
The default res_path that is drawn is for A* Search. To show a different path,
change res_path to be equal to a different Search algorithm.

