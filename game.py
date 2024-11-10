import random
import curses
import time
import pickle
import os
from enums import Gamestates
from menus import Menus
from level import Level
from animations import Animations


class ScreenSizeError(Exception):
    def __init__(self):
        self.msg = "ERROR: Screen is smaller than 60 * 24."
        super().__init__(self.msg)
    
    def get_msg(self):
        return self.msg

class Game:
    def __init__(self, scr):
        self.screen = scr
        self.state = Gamestates.MAIN_MENU
        self.curses_loaded = False
        self.highlighted = (0,0)
        self.is_selected = False
        self.difficulty = 0

    #loads and initializes curses module
    def load_curses(self):
        self.check_screen_size()
        #init background color pairs
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)     #walls
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)     #background
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_WHITE)     #highlighted
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_YELLOW)   #selected
        curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLUE)       #correct
        curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK)     #default text 
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)     #highlighted text
        #make cursor invisible
        curses.curs_set(False)
        #init timeout
        self.screen.timeout(500)
        #init variables
        self.blink = False       

        self.flush_screen(True)                                   
        self.curses_loaded = True
                
    #loads a save file, returns true if successful
    def load_save(self):
        try:
            f_save = open("save.pickle", "rb")
            self.current_level, self.levels = pickle.load(f_save)
            f_save.close()
            return True
        except:
            return False

    #updates save file
    def update_save(self):
        try:
            f_save = open("save.pickle", "wb")
            pickle.dump((self.current_level, self.levels), f_save)
            f_save.close()
            return True
        except:
            return False

    #checks if a save exists
    def has_save(self):
        try:
            f_save = open("save.pickle", "rb")
            f_save.close()
            return True
        except:
            return False

    #makes a new save file when player starts a new game
    def new_save(self):
        self.levels = [Level(4), Level(5), Level(5), Level(6), Level(6)]
        self.current_level = 0
        try:
            f_save = open("save.pickle", "wb")
            pickle.dump((self.current_level, self.levels), f_save)
            f_save.close()
        except:
            pass
        self.reset_highlight()

    #clears screen
    def flush_screen(self, flag = False):
        self.screen.clear()
        if flag:
            self.screen.addstr(" ")
            self.screen.refresh()
            self.screen.clear()
        self.screen.refresh()

    def reset_highlight(self):
        self.highlighted = (0, 0)
        self.is_selected = False


    #gets and handles user input, returns the input key
    #if currently in a level, also edits the grid
    def handle_input(self, max_pos = -1, loop = True):
        key = self.screen.getch()
        if key == curses.KEY_RESIZE:
            self.check_screen_size()
            self.flush_screen()
        previous_highlight = self.highlighted
        if key in (curses.KEY_UP, ord("w")):
            self.highlighted = (self.highlighted[0] - 1, self.highlighted[1])
        elif key in (curses.KEY_DOWN, ord("s")):
            self.highlighted = (self.highlighted[0] + 1, self.highlighted[1])
        elif key in (curses.KEY_LEFT, ord("a")):
            self.highlighted = (self.highlighted[0], self.highlighted[1] - 1)
        elif key in (curses.KEY_RIGHT, ord("d")):
            self.highlighted = (self.highlighted[0], self.highlighted[1] + 1)
        elif key in (curses.KEY_ENTER, ord(" "), ord("\n")):
            self.is_selected = not self.is_selected
        if max_pos > 0: 
            if not loop:
                self.highlighted = (min(self.highlighted[0], max_pos-1), min(self.highlighted[1], max_pos-1))
            else:
                self.highlighted = (self.highlighted[0] % max_pos, self.highlighted[1] % max_pos)
        if not loop:
            self.highlighted = (max(self.highlighted[0], 0), max(self.highlighted[1], 0))
            

        if self.state == Gamestates.IN_LEVEL:
            if key == -1:
                self.blink = not self.blink
            else:
                self.blink = False
            return (key, previous_highlight)
        return key

    def check_screen_size(self):
        if (self.screen.getmaxyx()[0] < 24) or (self.screen.getmaxyx()[1] < 60):
            raise ScreenSizeError

    #called to run the game
    def run(self):
        if not self.curses_loaded:
            try:
                self.load_curses()
            except ScreenSizeError as err:
                Menus.draw_error_menu(self.screen, err.get_msg())
                return
        self.running = True
        self.paused = False
        Animations.draw_intro(self.screen)
        self.flush_screen()
        while self.running:
            match self.state:
                case Gamestates.MAIN_MENU:
                    Menus.draw_main_menu(self.screen, self.highlighted)
                    if self.is_selected:
                        match self.highlighted[0]:
                            case 0: #new game
                                self.paused = False
                                Animations.draw_loading_screen(self.screen)
                                self.new_save()
                                Animations.draw_level_cutscene(self.screen, 1)
                                self.state = Gamestates.IN_LEVEL
                            case 1: #continue
                                if self.load_save(): #only load the save if there is one
                                    self.flush_screen()
                                    Animations.draw_level_cutscene(self.screen, self.current_level)
                                    self.state = Gamestates.IN_LEVEL
                            case 2: #help
                                self.state = Gamestates.HELP_MENU
                            case 3: #exit
                                self.running = False
                        self.reset_highlight()
                        continue
                    try:
                        self.handle_input(4)
                    except ScreenSizeError as err:
                        Menus.draw_error_menu(self.screen, err.get_msg())
                        return
                    

                case Gamestates.HELP_MENU:
                    #the menu doesn't need to be refreshed, so there's no need for timout 
                    self.screen.timeout(-1)
                    #draws the menu
                    Menus.draw_help_menu(self.screen)
                    #wait for an input
                    try:
                        self.handle_input()
                    except ScreenSizeError as err:
                        Menus.draw_error_menu(self.screen, err.get_msg())
                        return
                    #after getting any input, we exit and go back to main menu/pause menu depends on where we came from
                    if self.paused:
                        self.state = Gamestates.PAUSED
                    else:
                        self.state = Gamestates.MAIN_MENU
                    self.reset_highlight()
                    self.flush_screen()
                    #reset timeout to default now that we exited the menu
                    self.screen.timeout(500)

                case Gamestates.IN_LEVEL:
                    #check if the player has completed all levels
                    if self.current_level >= len(self.levels):
                        self.state = Gamestates.MAIN_MENU
                        #remove the completed save
                        if os.path.exists("save.pickle"):
                            os.remove("save.pickle")
                        continue

                    self.in_level = True
                    level = self.levels[self.current_level] 
                    #draws Level 
                    max_size = self.screen.getmaxyx()
                    level_subwindow = self.screen.subwin(   level.size * 3 + 4, level.size * 6 + 4, 
                                                            (max_size[0] - level.size*3)//2 - 2, (max_size[1] - level.size*6)//2 - 2)
                    level.draw(level_subwindow, self.highlighted, self.is_selected, self.blink) 

                    #game logic:
                    #if player moves around while they haven't selected anything, changes the highlighted Tile
                    #if self.is_selected, then when the player moves around, swap blocks
                    #pauses game if player presses p

                    key_input, previous_highlight = (0, 0), (0, 0)
                    try:
                        key_input, previous_highlight = self.handle_input(self.levels[self.current_level].size, False)
                    except ScreenSizeError as err:
                        Menus.draw_error_menu(self.screen, err.get_msg())
                        return
                    
                    if key_input in (27, ord("p")):
                        self.state = Gamestates.PAUSED
                        self.paused = True
                        continue
    

                    #check if the player has completed the current level
                    #only checks when the player's not holding anything
                    if self.levels[self.current_level].is_complete() and not self.is_selected:
                        self.current_level += 1
                        Animations.draw_level_cutscene(self.screen, self.current_level + 1)
                    
                    #if the player has selected anything, move around
                    if self.is_selected:
                        self.levels[self.current_level].move(previous_highlight, self.highlighted)

                case Gamestates.PAUSED:
                    Menus.draw_pause_menu(self.screen, self.highlighted)
                    if self.is_selected:
                        match self.highlighted[0]:
                            case 0: #continue
                                self.flush_screen()
                                self.paused = False
                                self.state = Gamestates.IN_LEVEL
                            case 1: #new game
                                self.paused = False
                                Animations.draw_loading_screen(self.screen)
                                self.new_save()
                                Animations.draw_level_cutscene(self.screen, 1)
                            case 2: #help
                                self.state = Gamestates.HELP_MENU
                            case 3: #save & quit
                                self.paused = False
                                self.update_save()
                                Animations.draw_saving_screen(self.screen)
                                time.sleep(1)
                                self.flush_screen()
                                self.state = Gamestates.MAIN_MENU
                        self.reset_highlight()
                        continue
                    try:
                        if self.handle_input(4) in (27, ord("p")):
                            self.flush_screen()
                            self.paused = False
                            self.state = Gamestates.IN_LEVEL
                            self.reset_highlight()
                    except ScreenSizeError as err:
                        Menus.draw_error_menu(self.screen, err.get_msg())
                        return
        #this is when the game stops 
        Animations.draw_scrolling_text(self.screen, "Thank You For Playing!", bold=True, clear_screen=True, updates = 20)
        time.sleep(1)
        text = "Press any key to exit..."
        self.screen.addstr(self.screen.getmaxyx()[0]//2, (self.screen.getmaxyx()[1] - len(text))//2, text, curses.color_pair(6))
        self.screen.timeout(-1)
        self.screen.getch()
                    

#driver code        
def main(stdscr):
    game_instance = Game(stdscr)
    game_instance.run()

if __name__ == "__main__":
    curses.wrapper(main)
