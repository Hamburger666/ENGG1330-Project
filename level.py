from enums import Directions
import curses
import random
import time
from tile import Tile
from enums import TileTypes

class Level:
    #constructor
    def __init__(self, size):
        self.size = size                                                #sets the size based on stage
        self.grid = [[0 for _ in range(size)] for _ in range (size)]    #initializes grid to be N*N non-traversed nodes
        self.path = []                                                  #initializes path to be an empty array
        self.generate_path(0,0)                                         #generates a path for the level
        self.generate_tile_map()                                        #converts the path into a tile map
        self.reference_map = self.tile_map.copy()
        self.randomize_tile_map()                                       #randomizes the tile map

    #method to generate a Hamiltonian path
    def generate_path(self, row, col) -> bool:
        #base case: path covered the whole map
        if len(self.path) == self.size ** 2:
            #check if end point is in a corner, currently depreciated
            return True #self.is_corner(self.path[-1][0], self.path[-1][1])
            
        #make a list of direcions and shuffles it for random generation
        moves = list(Directions)
        random.shuffle(moves)

        #try each move in the list
        for move in moves:
            #check if the current node is within grid bounds
            if self.is_out_of_bounds(row, col):
                return False
            #check if the current node is traversed
            elif self.grid[row][col]:
                return False

            #set current node to traversed and add it to the path array as a position
            self.grid[row][col] = 1
            self.path.append((row, col))
        
            #recursively edit the grid to generat a path
            if self.generate_path(row + move.value[0], col + move.value[1]):
                return True
            
            #undo path addition and reset current node for backtracking
            self.grid[row][col] = 0
            self.path.pop()
            
    #checks if the given coordinates is within grid bounds
    def is_out_of_bounds(self, row, col) -> bool:
        return row >= self.size or row < 0 or col >= self.size or col < 0
    
    #converts the generated path to a matrix of tiles (referred to as the tile map)
    def generate_tile_map(self):
        self.tile_map = [[None for _ in range(self.size)] for _ in range (self.size)]
        for i in range(len(self.path)):
            node = self.path[i]
            if i == 0:
                self.tile_map[node[0]][node[1]] = Tile(TileTypes.get_tile_type(node, self.path[i + 1]))
            elif i == len(self.path) - 1:
                self.tile_map[node[0]][node[1]] = Tile(TileTypes.get_tile_type(node, self.path[i - 1]))
            else:
                self.tile_map[node[0]][node[1]] = Tile(TileTypes.get_tile_type(node, self.path[i + 1], self.path[i - 1]))
    
    #randomize the tile map
    def randomize_tile_map(self):
        temp = [col for row in self.tile_map for col in row]
        random.shuffle(temp)
        for i in range(self.size):
            self.tile_map[i] = temp[i * self.size: (i+1) * self.size]
    
    #swaps 2 tiles
    def move(self, pos1, pos2):
        self.tile_map[pos1[0]][pos1[1]], self.tile_map[pos2[0]][pos2[1]] = self.tile_map[pos2[0]][pos2[1]], self.tile_map[pos1[0]][pos1[1]]

    #checks for level completion
    def is_complete(self):
        total_correct = 0
        for row in range(self.size):
            for col in range(self.size):
                if self.tile_map[row][col] == self.reference_map[row][col]:
                    total_correct += 1
        return total_correct == len(self.path)

    #draws the current level
    def draw(self, screen, highlighted, is_selected, blink):
        #screen.clear()
        for row in range(self.size):
            for col in range(self.size):
                is_correct = self.reference_map[row][col] == self.tile_map[row][col]
                is_highlighted = row == highlighted[0] and col == highlighted[1]
                self.tile_map[row][col].draw(screen, row, col, is_correct, is_highlighted, is_selected, self.size, blink)
        screen.refresh()
    
    #DEBUG
    def debug(self, scr, time):
        scr.addstr(" ", curses.color_pair(1))
        scr.refresh()
        scr.clear()
        for row in range(self.size):
            for col in range(self.size):
                self.tile_map[row][col].draw(scr, row, col, False, False, True, self.size, False)
        scr.refresh()
        scr.getch()
        scr.clear()
        for row in range(self.size):
            for col in range(self.size):
                self.reference_map[row][col].draw(scr, row, col, False, False, True, self.size, False)
        scr.refresh()
        scr.getch()
        scr.clear()
        scr.addstr(f"{str(round(time))} seconds")
        scr.refresh()
        scr.getch()


#DEBUG
def main(scr): 
    import time
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)     #background
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)     #walls
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_YELLOW)   #highlighted
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_WHITE)     #selected
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLUE)       #correct

    #generates a random level and sees if it's generated correctly and can display correctly
    start = time.time()
    test = Level(7)
    test.debug(scr, time.time() - start)


if __name__ == "__main__":
    curses.wrapper(main)


        
        
    
