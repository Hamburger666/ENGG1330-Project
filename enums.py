from enum import Enum

class Gamestates(Enum):
    MAIN_MENU = 0
    HELP_MENU = 1
    IN_LEVEL = 2
    PAUSED = 3
    GAME_OVER = 4
    STORY_MENU = 5


class Directions(Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    EAST = (0, 1)
    WEST = (0, -1)


class TileTypes(Enum):
    TOP_LEFT = [[0,0,0],[0,1,1],[0,1,0]]
    TOP_RIGHT = [[0,0,0],[1,1,0],[0,1,0]]
    BOTTOM_LEFT = [[0,1,0],[0,1,1],[0,0,0]]
    BOTTOM_RIGHT = [[0,1,0],[1,1,0],[0,0,0]]
    VERTICAL = [[0,1,0],[0,1,0],[0,1,0]]
    HORIZONTAL = [[0,0,0],[1,1,1],[0,0,0]]
    LEFT = [[0,0,0],[1,1,0],[0,0,0]]
    RIGHT = [[0,0,0],[0,1,1],[0,0,0]]
    UP = [[0,1,0],[0,1,0],[0,0,0]]
    DOWN = [[0,0,0],[0,1,0],[0,1,0]]

    @classmethod
    def get_tile_type(cls, current, *adj:tuple):
        base = [[0,0,0],[0,1,0],[0,0,0]]
        for edge in adj:
            dy, dx = edge[0] - current[0], edge[1] - current[1]
            base[1 + dy][1 + dx] = 1
        return cls(base)



    
