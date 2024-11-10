#draws all animations
import curses
import time
from level import Level

class Animations:
    @staticmethod
    def draw_loading_screen(screen):
        screen.clear()
        text = "Loading..."
        screen.addstr(screen.getmaxyx()[0]//2, (screen.getmaxyx()[1] - len(text))//2, text, curses.color_pair(6) | curses.A_BOLD)
        screen.refresh()


    @staticmethod
    def draw_saving_screen(screen):
        screen.clear()
        text = "Saving..."
        screen.addstr(screen.getmaxyx()[0]//2, (screen.getmaxyx()[1] - len(text))//2, text, curses.color_pair(6) | curses.A_BOLD)
        screen.refresh()


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
            title_pad.refresh(0, 52//2 - (i+1), start_y + 2, x_shift + 52//2 - (i+1), start_y + 8, x_shift + 52//2 + i)
            time.sleep(0.05)

        #draw the whole thing moving to the top
        for i in range(start_y + 1):
            screen.clear()
            screen.refresh()
            line_pad.refresh(0, 0, start_y - i, 0, start_y - i, screen.getmaxyx()[1]-1)
            title_pad.refresh(0, 0, start_y + 2 - i, x_shift, start_y + 8 - i, x_shift + 52)
            line_pad.refresh(0, 0, start_y + 9 - i, 0, start_y + 9 - i, screen.getmaxyx()[1]-1)
            time.sleep(0.1)
        curses.flushinp()
        
    @staticmethod
    def draw_level_complete_animation(screen, level):
        pass

    @staticmethod
    def draw_credits(screen):
        text = [
            [
                "===  Gameplay Design  ===",
                "Arthur",
                ""
            ],[
                "=== Graphics Design  ==="
            ],
            "Graphics Design: Ruby, Lea",
            "Storywriting: Sky, Andrew",
            "Programmers: Arthur(Lead), "
        ]



    #display horizontally scrolling text centered at any position (default center of screen)
    @staticmethod
    def draw_scrolling_text(screen, text, pos = None, *, updates = 5, mirrored = False, clear_screen = False, bold = False):
        if pos == None:
            pos = (screen.getmaxyx()[0]//2, screen.getmaxyx()[1]//2)
        if clear_screen:
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
        curses.flushinp()


    @staticmethod
    def draw_level_cutscene(screen, level):
        screen.clear()
        text = f"--Level {level}--"
        screen.addstr(screen.getmaxyx()[0]//2, (screen.getmaxyx()[1] - len(text))//2, text, curses.color_pair(6) | curses.A_BOLD)
        screen.refresh()
        time.sleep(1.5)
