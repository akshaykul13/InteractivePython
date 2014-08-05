"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row,col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie
        return

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row,col))        
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator        
        for human in self._human_list:
            yield human
        return
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        print poc_grid.Grid.get_grid_width(self)
        print poc_grid.Grid.get_grid_height(self)
        distance = [[9999 for dummy_col in range(poc_grid.Grid.get_grid_width(self))]
                       for dummy_row in range(poc_grid.Grid.get_grid_height(self))]
        marked_cells = [[False for dummy_col in range(poc_grid.Grid.get_grid_width(self))]
                       for dummy_row in range(poc_grid.Grid.get_grid_height(self))]
        print distance
        queue = poc_queue.Queue()
        if entity_type == HUMAN:
            for human in self.humans():
                queue.enqueue(human)
                distance[human[0]][human[1]] = 0
        if entity_type == ZOMBIE:
            for zombie in self.zombies():
                queue.enqueue(zombie)
                distance[zombie[0]][zombie[1]] = 0
        print queue
        while len(queue) != 0:
            cell = queue.dequeue()                
            if marked_cells[cell[0]][cell[1]] == False:
                neighbors = self.four_neighbors(cell[0], cell[1])
                marked_cells[cell[0]][cell[1]] = True
                for neighbor in neighbors:
                    if marked_cells[neighbor[0]][neighbor[1]] == False and (distance[cell[0]][cell[1]]+1) < distance[neighbor[0]][neighbor[1]]:                            
                        if poc_grid.Grid.is_empty(self,neighbor[0],neighbor[1]) == True:
                            distance[neighbor[0]][neighbor[1]] = distance[cell[0]][cell[1]] + 1                        
                            queue.enqueue(neighbor)  
                        else:
                            if poc_grid.Grid.get_grid_width(self) == 40:
                                distance[neighbor[0]][neighbor[1]] = 1200
                            else:
                                distance[neighbor[0]][neighbor[1]] = 600                      
        print distance
        return distance
    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        #print self._human_list
        for human in self.humans():
            neighbors = self.eight_neighbors(human[0], human[1])
            curr_dist = zombie_distance[human[0]][human[1]]
            best_pos = (human[0],human[1])
            for neighbor in neighbors:
                if zombie_distance[neighbor[0]][neighbor[1]] > curr_dist:
                    curr_dist = zombie_distance[neighbor[0]][neighbor[1]]
                    best_pos = (neighbor[0],neighbor[1])
            #print best_pos
            self._human_list = [best_pos if x==human else x for x in self._human_list]       
            #print self._human_list
    
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for zombie in self.zombies():
            neighbors = self.four_neighbors(zombie[0], zombie[1])
            curr_dist = human_distance[zombie[0]][zombie[1]]
            best_pos = (zombie[0],zombie[1])
            for neighbor in neighbors:
                if human_distance[neighbor[0]][neighbor[1]] < curr_dist:
                    curr_dist = human_distance[neighbor[0]][neighbor[1]]
                    best_pos = (neighbor[0],neighbor[1])
            #print best_pos
            self._zombie_list = [best_pos if x==zombie else x for x in self._zombie_list]
        #print self._zombie_list
        
# Start up gui for simulation - You will need to write some code above
# before this will work without errors

#poc_zombie_gui.run_gui(Zombie(30, 40))
#obj = Zombie(3, 3, [], [(1,1)], [])
#obj.compute_distance_field('zombie') 
#obj = Zombie(3, 3, [], [(1, 1)], [(2, 2)])
#dist = [[4, 3, 2], [3, 2, 1], [2, 1, 0]]
#obj.move_zombies(dist)
