import time
import curses

import settings
import menu

class Display(object):
    def __init__(self):
        self.window = curses.initscr()
        self.window.keypad(True)
        curses.noecho()
        curses.cbreak()
        self.currentOptions = []

    def teardown(self):
        self.window.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def drawMenu(self, m, validChildren):
        self.window.erase()
        self.printHeader(m)

        self.currentOptions = validChildren

        # Display all valid children.
        for i in range(len(validChildren)):
            self.window.addstr(4+i, 2, "    %d: %s %s %s" % (i, validChildren[i].name.ljust(settings.MAX_ITEM_NAME_LEN), 
                                        ">" if isinstance(validChildren[i], menu.Menu) else " ",
                                        validChildren[i].description))
        self.window.refresh()

    def getChoices(self):
        selected = 0
        c = None
        done = False
        while not done:
            self.window.chgat(4+selected, 5, 3+settings.MAX_ITEM_NAME_LEN, curses.A_STANDOUT)

            try:
                c = self.window.getch()
            except KeyboardInterrupt:
                pass

            self.window.chgat(4+selected, 5, 3+settings.MAX_ITEM_NAME_LEN, curses.A_NORMAL)

            if c == curses.KEY_UP or c == ord('k'):
                selected = max(0, selected - 1)
            elif c == curses.KEY_DOWN or c == ord('j'):
                selected = min(len(self.currentOptions) - 1, selected + 1)
            elif c >= ord('0') and c <= ord('9'):
                selected = c - ord('0')
                selected = min(len(self.currentOptions)-1, max(0, selected))
            elif c == ord('='):
                selected = '='
                done = True
            elif c == ord('q'):
                done = True

        return [selected]

    def printSeparator(self):
        """DIsplays an obvious visual separator designed to separate menu levels etc."""
        pass
     
    def enterToContinue(self):
        """Utility function to request the user press enter to continue."""
        print("")
        raw_input("Press Enter to Continue.")

    def notice(self, message):
        print("")
        print(message)
        self.enterToContinue()

    def printHeader(self, m):
        """Prints a standard menu header, common to all menus."""
        self.window.addstr(0, 0, time.strftime("%A, %d %b %Y %H:%M:%S %Z").rjust(settings.MENU_WIDTH))
        self.window.addstr(1, 0, "[%s] [%s]" % ((m.path(), m.locationString().strip())))
        self.window.addstr(2, 0, m.description)

    def confirmParams(self, a):
        """If necessary, request confirmation of the parameter values."""
        if a.requireConfirmation:
            self.printSeparator()
            print(a.description)
            print("")

            for param in a.params:
                print("%s: %s" % (param.name, param.value))

            if len(a.params) > 0:
                print("")

            input = raw_input("Are you sure?(y/n): ")
            return True if input == 'y' else False
        else:
            return True

    def evaluateParam(self, p):
        self.printSeparator()
        print("%s %s" % (p.name.ljust(settings.MAX_ITEM_NAME_LEN), p.description))
        print("Default is %s" % (p.default if p.value == None else p.value))
        print("")
     
        while p.value == None: 
            input = raw_input("Enter Choice: ")
            if len(input) > 0:
                p.value = input
            else:
                p.value = p.default

