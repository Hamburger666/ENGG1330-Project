import curses
import time
from level import Level
from enums import Directions

class Animations:
    
    @staticmethod
    def draw_loading_screen(screen):
        screen.clear()

        text = [
            "Generating Levels...", 
            "(This may take a while)"]
        for i in range(2):
            screen.addstr(  screen.getmaxyx()[0]//2 + i * 2, (screen.getmaxyx()[1] - len(text[i]))//2, 
                            text[i], curses.color_pair(6) | curses.A_BOLD)
        screen.refresh()
        time.sleep(1)

    @staticmethod
    def draw_saving_screen(screen):
        screen.clear()
        text = "Saving..."
        screen.addstr(  screen.getmaxyx()[0]//2, (screen.getmaxyx()[1] - len(text))//2, 
                        text, curses.color_pair(6) | curses.A_BOLD)
        screen.refresh()

    #3 part animation that plays when the game is launched
    @staticmethod
    def draw_intro(screen):
        screen.clear()
        screen.refresh()
        Animations.draw_scrolling_text(screen, "Presented by Group M2-2...", updates = 20)
        time.sleep(0.5)
        title = [
                " _______ _    _ ______        _               ____  ",
                "|__   __| |  | |  ____|      | |        /\\   |  _ \\ ",
                "   | |  | |__| | |__         | |       /  \\  | |_) |",
                "   | |  |  __  |  __|        | |      / /\\ \\ |  _ < ",
                "   | |  | |  | | |____       | |____ / ____ \\| |_) |",
                "   |_|  |_|  |_|______|      |______/_/    \\_\\____/ "]
        start_y = (screen.getmaxyx()[0]-10)//2
        x_len, x_mod = divmod(screen.getmaxyx()[1], 2) #variables to reduce the number of operations
        title_pad, line_pad = curses.newpad(9, 52), curses.newpad(2, (x_len * 2 + x_mod))
        line_pad.addstr("=" * (x_len * 2 + x_mod), curses.color_pair(6))
        for row in title:
            title_pad.addstr(row, curses.color_pair(6))

        #draw bars
        for i in range(x_len + x_mod):
            line_pad.refresh(   0, x_len - (i+1) + x_mod, 
                                start_y, x_len - (i+1) + x_mod, 
                                start_y, x_len + i)
            line_pad.refresh(   0, x_len - (i+1) + x_mod, 
                                start_y + 9, x_len - (i+1) + x_mod, 
                                start_y + 9, x_len + i)
            time.sleep(0.02)

        logo_subwin = screen.subwin(8, screen.getmaxyx()[1], start_y + 1, 0)
        #draw scanning effect
        x_shift = (screen.getmaxyx()[1]-52)//2
        for i in range(52//2-2):
            logo_subwin.clear()
            logo_subwin.refresh()
            title_pad.refresh(0, i, start_y + 2, x_shift + i, start_y + 8, x_shift + i)
            title_pad.refresh(0, 51 - i, start_y + 2, x_shift + 51 - i, start_y + 8, x_shift + 51 - i)
            time.sleep(0.05)
        
        #draw logo expansion
        for i in range(3, 52//2):
            title_pad.refresh(  0, 52//2 - (i+1), start_y + 2, x_shift + 52//2 - (i+1), 
                                start_y + 8, x_shift + 52//2 + i)
            time.sleep(0.05)

        #draw the whole thing moving to the top
        for i in range(start_y + 1):
            screen.clear()
            screen.refresh()
            line_pad.refresh(0, 0, start_y - i, 0, start_y - i, screen.getmaxyx()[1]-1)
            title_pad.refresh(0, 0, start_y + 2 - i, x_shift, start_y + 8 - i, x_shift + 52)
            line_pad.refresh(0, 0, start_y + 9 - i, 0, start_y + 9 - i, screen.getmaxyx()[1]-1)
            screen.refresh()
            time.sleep(0.1)
        curses.flushinp()
    
    #draws the game over icon with a semi-scanning effect
    @staticmethod
    def draw_game_over_animation(screen):
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        image = [
            "  ___   __   _  _  ____ "
            " / __) / _\\ ( \\/ )(  __)",
            "( (_ \\/    \\/ \\/ \\ ) _) ",
            " \\___/\\_/\\_/\\_)(_/(____)",
            "",
            "  __   _  _  ____  ____ ",
            " /  \\ / )( \\(  __)(  _ \\"
            "(  O )\\ \\/ / ) _)  )   /",
            " \\__/  \\__/ (____)(__\\_)"]

        #initialize pad
        pad = curses.newpad(10, 24)
        for row in image:
            pad.addstr(row, curses.color_pair(1) | curses.A_BOLD)
        
        #draw increasing area of the pad from the center
        for i in range(24//2):
            pad.refresh(0, 24//2 - (i+1), 
                        (screen.getmaxyx()[0]-9)//2, screen.getmaxyx()[1]//2 - (i+1), 
                        (screen.getmaxyx()[0]-9)//2 + 9, screen.getmaxyx()[1]//2 + i)
            time.sleep(0.1)
        time.sleep(1)
        curses.flushinp()
        

    #draws the level slowly dissolving
    @staticmethod
    def draw_level_complete_animation(screen, level):
        eraser = curses.newpad(2, 2)
        eraser.addstr("__", curses.color_pair(1))
        grid_pos = level.path[0]
        pos =   ((screen.getmaxyx()[0] - level.size * 3)//2 + 1 + grid_pos[0] * 3, 
                (screen.getmaxyx()[1] - level.size * 6)//2 + 2 + grid_pos[1] * 6)
        eraser.refresh(0, 0, pos[0], pos[1], pos[0], pos[1] + 1)
        for i in range(1, len(level.path)):
            move = Directions((level.path[i][0] - grid_pos[0], level.path[i][1] - grid_pos[1]))
            grid_pos = level.path[i]
            for j in range(3):
                pos = pos[0] + move.value[0], pos[1] + move.value[1] * 2
                eraser.refresh(0, 0, pos[0], pos[1], pos[0], pos[1] + 1)
                time.sleep(0.05)
        curses.flushinp()


    #display horizontally scrolling text centered at any position (default center of screen)
    #can scroll from either direction
    @staticmethod
    def draw_scrolling_text(screen, text, pos = None, *, 
                            updates = 5, mirrored = False, flush_screen = False, bold = False):
        if pos == None:
            pos = screen.getmaxyx()[0]//2, screen.getmaxyx()[1]//2
        if flush_screen:
            screen.clear()
            screen.refresh()
        pad = curses.newpad(10, 100)  
        start_x = pos[1] - len(text)//2
        pad.addstr(text, curses.color_pair(6) | curses.A_BOLD if bold else curses.color_pair(6))
        for i in range(len(text)):
            pad.refresh(0, 0, 
                        pos[0], start_x if not mirrored else start_x + len(text) - i, 
                        pos[0], start_x + i if not mirrored else start_x + len(text))
            time.sleep(1/updates)
        screen.addstr(pos[0], pos[1], text, curses.color_pair(6) | curses.A_BOLD if bold else curses.color_pair(6))
        curses.flushinp()


    @staticmethod
    def draw_level_cutscene(screen, level):
        Animations.draw_scrolling_text(screen, f"-- Level {level} --", updates = 10, flush_screen=True)
        time.sleep(1)
        screen.clear()
        screen.refresh()


#tells players how to correctly launch the game should they try to open this file instead
if __name__ == "__main__":
    print("Please launch the game with the command 'python game.py'.")