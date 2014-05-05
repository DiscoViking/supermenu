import time

import settings
import menu

class Display(object):
    def drawMenu(self, m, validChildren):
        self.printSeparator()
        self.printHeader(m)

        # Display all valid children.
        for i in range(len(validChildren)):
            print("    %d: %s %s %s" % (i, validChildren[i].name.ljust(settings.MAX_ITEM_NAME_LEN), 
                                        ">" if isinstance(validChildren[i], menu.Menu) else " ",
                                        validChildren[i].description))

    def teardown(self):
        pass

    def getChoices(self):
        """Get a valid command string from the user.
        A valid command string consists of some number of valid commands (numbers or =)
        separated by whitespace.
        If the input string is invalid, returns an empty command list."""
        input = ""
        while input == "":
            try:
                input = raw_input("Enter Choice: ")
            except KeyboardInterrupt:
                print("")
                return []
        try:
            commands = [int(command) if command != "=" else command for command in input.split()]
        except:
            print("Not a valid command string.")
            enterToContinue()
            commands = []

        return commands

    def printSeparator(self):
        """DIsplays an obvious visual separator designed to separate menu levels etc."""
        if settings.CLEAR_SCREEN:
            os.system("clear")
        else:
            print("\n%s\n" % ("-" * settings.MENU_WIDTH))
     
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
        print(time.strftime("%A, %d %b %Y %H:%M:%S %Z").rjust(settings.MENU_WIDTH))
        print("[%s] [%s]" % ((m.path(), m.locationString().strip())))
        print(m.description)

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

