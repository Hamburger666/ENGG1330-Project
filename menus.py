import curses


class Menus:
    #draws a top-down menu (or any text from top-down)
    @staticmethod
    def draw_menu(screen, menu_elements, highlighted = (), *, brackets = False):
        Menus.draw_logo(screen)
        for i in range(len(menu_elements)):
            element = f" <{menu_elements[i]}> " if brackets else f"  {menu_elements[i]}  "
            if i == highlighted[0]:
                element = f"< {menu_elements[i]} >"
            screen.addstr(  max((screen.getmaxyx()[0] - len(menu_elements))//2, 11) + i,
                            (screen.getmaxyx()[1] - len(element))//2, element,
                            curses.color_pair(7) if i == highlighted[0] else curses.color_pair(6) | curses.A_BOLD) 
        screen.refresh()

    #draws logo with 2 bars on top and bottom
    @staticmethod
    def draw_logo(screen):
        logo = [
            " _______ _    _ ______        _               ____  ",
            "|__   __| |  | |  ____|      | |        /\\   |  _ \\ ",
            "   | |  | |__| | |__         | |       /  \\  | |_) |",
            "   | |  |  __  |  __|        | |      / /\\ \\ |  _ < ",
            "   | |  | |  | | |____       | |____ / ____ \\| |_) |",
            "   |_|  |_|  |_|______|      |______/_/    \\_\\____/ "]

        #draws the bars and logo in top-down order
        screen.addstr(0, 0, "=" * (screen.getmaxyx()[1] - 1), curses.color_pair(6))
        for i in range(len(logo)):              
            screen.addstr(  2+i, (screen.getmaxyx()[1]-len(logo[i]))//2, 
                            logo[i], curses.color_pair(6) | curses.A_BOLD)
        screen.addstr(9, 0, "=" * (screen.getmaxyx()[1] - 1), curses.color_pair(6))

    @staticmethod
    def draw_main_menu(screen, highlighted):
        options = [
            "New Game",
            "Continue",
            "Help",
            "Story",
            "Quit"
        ]
        Menus.draw_menu(screen, options, highlighted, brackets = True)

    @staticmethod
    def draw_help_menu(screen):
        text = [
            "=====  HOW TO PLAY  =====",
            "",
            "Choose circuit parts with WASD or Arrow keys",
            "Press ENTER or SPACE to select a part",
            "Move the selected part with WASD or Arrow Keys",
            "Parts with the correct shape in a position will appear blue",
            "Red crosses will apear on parts at incorrect positions",
            "Reconstruct a complete circuit to complete the level",
            "However, if any circuit part is in the wrong position, the circuit explodes.",
            "You can press P or ESC while in game to pause"
            "",
            "",
            "Press any key to go back"
        ]
        Menus.draw_menu(screen, text, (-1, -1))

    @staticmethod
    def draw_story_menu(screen):
        text = [
            "===== BACKGROUND STORY =====",
            "",
            "You are a researcher working at an advanced materials lab.",
            "Just a week ago,",
            "And you are "
        ]
        
    @staticmethod
    def draw_pause_menu(screen, highlighted):
        options = [
            "Continue",
            "New Game",
            "Help",
            "Save and Quit"
        ]
        text = "=====  PAUSED  ====="
        Menus.draw_menu(screen, options, highlighted, brackets = True)
        screen.addstr(  screen.getmaxyx()[0]//2-4, (screen.getmaxyx()[1] - len(text))//2, 
                        text, curses.color_pair(6) | curses.A_BOLD)
        screen.refresh()

    @staticmethod
    def draw_game_over_menu(screen, highlighted):
        options = [
            "Restart",
            "Quit"
        ]
        Menus.draw_menu(screen, options, highlighted, True)

    @staticmethod
    def draw_error_menu(screen, error_msg):
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        screen.timeout(-1)
        screen.clear()
        text = "Press any key to exit..."
        screen.addstr(  screen.getmaxyx()[0]//2 - 1, (screen.getmaxyx()[1] - len(error_msg))//2, 
                        error_msg, curses.color_pair(1) | curses.A_BOLD)
        screen.addstr(  screen.getmaxyx()[0]//2 + 1, (screen.getmaxyx()[1]-len(text))//2, 
                        text, curses.color_pair(1) | curses.A_BOLD)
        screen.refresh()
        screen.getch()


    



            
        
