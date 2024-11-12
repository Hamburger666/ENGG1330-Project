import curses
import random
from tile import Tile
from enums import TileTypes
from enums import Directions

class Level:
    def __init__(self, size):
        self.size = size
        #initialize grid to be N*N unexplored nodes and path to be empty array
        self.grid = [[0 for _ in range(size)] for _ in range (size)] 
        self.path = []
        #generates the circuit using a wrapper function
        self.generate_path_safe(size)
        self.generate_tile_map()
        self.reference_map = self.tile_map.copy()
        self.randomize_tile_map()
    
    #wrapper for path generation, solves edge cases
    #note: 
    def generate_path_safe(self, n):
        start_y, start_x = random.randint(0, n-1), random.randint(0, n-1)
        if n % 2 == 1:
            start_x = start_y
        self.generate_path(start_y, start_x)

    #recursive function to generate a Hamiltonian path
    #Warning: time complexity is O(n^2)
    def generate_path(self, row, col) -> bool:
        #base case: path covered the whole map
        if len(self.path) == self.size ** 2:
            return True 

        #create list of directions in random order
        moves = list(Directions)
        random.shuffle(moves)

        #check if the current node is explored or out of bounds
        if self.is_out_of_bounds(row, col):
            return False
        elif self.grid[row][col] == 1:
            return False    

        #try all directions to see which leads to an unexplored node
        for move in moves:
            #set current node to traversed and add it to path to record
            self.grid[row][col] = 1
            self.path.append((row, col))
        
            #try to continue generating the path after moving
            if self.generate_path(row + move.value[0], col + move.value[1]):
                #current move leads to unexplored node
                return True
            
            #move does not lead to unexplored node
            #undo traversal and remove last node from path (backtrack)
            self.grid[row][col] = 0
            self.path.pop()
            
    #checks if the given coordinates is within grid bounds
    def is_out_of_bounds(self, row, col) -> bool:
        return row >= self.size or row < 0 or col >= self.size or col < 0
    
    #converts the generated path to a 2D array of tiles
    def generate_tile_map(self):
        self.tile_map = [[None for _ in range(self.size)] for _ in range (self.size)]
        for i in range(len(self.path)):
            node = self.path[i]
            new_tile = None
            if i == 0:
                #start tile
                new_tile = Tile(TileTypes.get_tile_type(node, self.path[i + 1]), i + 1)
            elif i == len(self.path) - 1:
                #end tile
                new_tile = Tile(TileTypes.get_tile_type(node, self.path[i - 1]), i + 1)
            else:
                new_tile = Tile(TileTypes.get_tile_type(node, self.path[i + 1], self.path[i - 1]), i + 1)
            self.tile_map[node[0]][node[1]] = new_tile
    
    #shuffle the entire tile map
    def randomize_tile_map(self):
        temp = [col for row in self.tile_map for col in row]
        random.shuffle(temp)
        for i in range(self.size):
            self.tile_map[i] = temp[i * self.size: (i+1) * self.size]
    
    #swaps 2 tiles
    def move(self, pos1, pos2):
        self.tile_map[pos1[0]][pos1[1]], self.tile_map[pos2[0]][pos2[1]] = self.tile_map[pos2[0]][pos2[1]], self.tile_map[pos1[0]][pos1[1]]

    #check if the level is completed, and if tiles are in correct order
    #returns a tuple of (bool, bool)
    def is_complete(self):
        total_correct, is_order_correct = 0, True
        for row in range(self.size):
            for col in range(self.size):
                if self.tile_map[row][col] == self.reference_map[row][col]:
                    total_correct += 1
                if self.tile_map[row][col].number != self.reference_map[row][col].number:
                    is_order_correct = False
        return (total_correct == len(self.path), is_order_correct)

    #displays the level
    def draw(self, screen, highlighted, is_selected, blink):
        for row in range(self.size):
            for col in range(self.size):
                is_correct_pos = self.reference_map[row][col] == self.tile_map[row][col]
                is_correct_order = self.reference_map[row][col].number == self.tile_map[row][col].number
                is_highlighted = row == highlighted[0] and col == highlighted[1]
                self.tile_map[row][col].draw(   screen, row, col, is_correct_pos, is_correct_order, 
                                                is_highlighted, is_selected, self.size, blink)
        screen.refresh()

    #DEBUG draws the level after & before shuffle, also displays path
    def debug(self, screen):

        screen.clear()
        for i in range(len(self.path)):
            screen.addstr(i, 0, str(self.path[i]))
        screen.refresh()
        screen.getch()
        screen.refresh()
        for row in range(self.size):
            for col in range(self.size):
                self.tile_map[row][col].draw(screen, row, col, False, False, False, False, self.size, False)
        screen.refresh()
        screen.getch()
        screen.clear()
        for row in range(self.size):
            for col in range(self.size):
                self.reference_map[row][col].draw(screen, row, col, False, False, False, False, self.size, False)
        screen.refresh()
        screen.getch()


#DEBUG driver code
def main(scr):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)     #background
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)     #incorrect position & order
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_WHITE)     #highlighted
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_YELLOW)   #selected
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLUE)       #correct position & order
    curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK)     #default text 
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)     #highlighted text
    curses.init_pair(8, curses.COLOR_RED, curses.COLOR_BLUE)        #correct position, wrong order

    test = Level(5)
    test.debug(scr)

#tells players how to correctly launch the game should they open this file
#also lets devs debug by writing an extra command line argument
if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2 and sys.argv[2].lower() == "debug":
        curses.wrapper(main)
    else:
        print("Please launch the game with the command 'python game.py'.")


