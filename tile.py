from enums import TileTypes
import curses

class Tile:
    def __init__(self, tile_type, number):
        self.tile_type = tile_type
        self.number = number

    #overrides default == sign comparison
    def __eq__(self, other):
        if isinstance(other, Tile):
            return self.tile_type == other.tile_type
        return False

    #displays the tile at the given position
    def draw(self, screen, row, col, is_correct_pos, is_correct_order, is_highlighted, is_selected, size, blink):
        color = [curses.color_pair(1), curses.color_pair(2)]
        if is_highlighted and not blink:
            color[1] = curses.color_pair(3)
            if is_selected:
                color[1] = curses.color_pair(4) 
        elif is_correct_pos:
            color[1] = curses.color_pair(8) | curses.A_BOLD
            if is_correct_order:
                color[1] = curses.color_pair(5)
        for i in range(3):
            for j in range(3):
                megapixel = "++" if i == 1 and j == 1 else "  " 
                screen.addstr(  (screen.getmaxyx()[0] - size * 3)//2 + row * 3 + i, 
                                (screen.getmaxyx()[1] - size * 6)//2 + (col * 3 + j) * 2, 
                                megapixel, color[self.tile_type.value[i][j]])
