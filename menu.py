import os
import subprocess
import time

import globals
from util import *
import value

class Item(object):
    """A generic menu item."""
    def __init__(self):
        self.flags = []

    def addFlag(self, flag):
        """Adds a flag to this menu item. An item will not appear unless all it's flags are valid."""
        self.flags.append(flag)

    def removeFlag(self, flag):
        """Removes a flag from this menu item."""
        self.flags.remove(flag)

    def isValid(self):
        """Returns True if the menu item is currently valid. False otherwise. A menu item will not be displayed if it is invalid."""
        for flag in self.flags:
            if not flag.isValid():
                return False
        return True

class Menu(Item):
    """A menu is a container for other items. It allows the user to select from it's children."""
    def __init__(self, name, description, children):
        super(Menu,self).__init__()
        self.children = children
        self.name = name
        assert(len(name) <= globals.MAX_ITEM_NAME_LEN)
        self.description = description
        self.returningHome = False
        self.parent = None
        self.location = None

    def execute(self, parent, location, commands=[]):
        """Display the menu, get the user's choice, and execute the chosen child."""
        self.parent = parent
        self.location = location

        choice = ""

        while choice != 0 and not self.returningHome:
            # Create the fake "Back" action to be displayed in the m.
            # In reality, this action is never executed, the 0 command
            # is handled specially.
            backAction = Menu("Back" if self.parent != None else "Exit", 
                              "Go up a self level" if self.parent != None else "Exit the self.", 
                              None)
            
            # Get a list of valid children to display. Invalid iteselfs are not even displayed.
            validChildren = [backAction] + [child for child in self.children if child.isValid()]        

            globals.DISPLAY.drawMenu(self, validChildren)

            # Get the user's selection.
            # The if test here prevents us from pausing for input if we are
            # evaluating a command chain.
            if len(commands) == 0:
                commands = getChoices()

            # If we got some commands, evalutate them.
            # If not, the loop will spin and the menu will be printed again.
            if len(commands) != 0:
                choice = commands[0]
                commands = commands[1:]

                # An = indicated we should return all the way to top level.
                # This signal will be propagated up to all parents, forcing them
                # to break their loops, except for the root menu.
                if choice == "=":
                    self.returnHome()
                elif choice != 0:
                    # Otherwise attempt to get the selected menu option.
                    try:
                        command = validChildren[choice]
                    except:
                        globals.DISPLAY.notice("Not a valid command.")
                        commands = []
                        command = None
                    else:
                        try:
                            # Execute the selected menu option.
                            # Note that this could be a further submenu, or an action
                            # This menu doesn't care which it is.
                            commands = command.execute(self, choice, commands)
                        except KeyboardInterrupt:
                            # Protect against keyboard interrupts.
                            # We don't want to menu to quit if the user hits Ctrl-C.
                            # Protecting here ensures it will only ever quit to the previous menu level.
                            commands = []

        self.returningHome = False
        return commands

    def returnHome(self):
        """Set ourselves to stop looping, and signal to our parent to do the same.
        This will cause the entire menu chain to unravel, ending with the user back at
        the top level."""
        if self.parent != None:
            self.parent.returnHome()

            self.returningHome = True 

    def locationString(self):
        """Build a string describing our numerical location by recursively building
        on top of all our parents."""
        if self.parent == None:
            return "="
        
        return self.parent.locationString() + " " + str(self.location)

    def path(self):
        """Build a string describing our path by name."""
        if self.parent == None:
            return self.name
        
        return self.parent.path() + "->" + self.name

class Action(Item):
    """A menu item which describes a command to be executed."""
    def __init__(self, name, description, script, params=[]):
        super(Action,self).__init__()
        self.name = name
        assert(len(name) <= globals.MAX_ITEM_NAME_LEN)
        self.description = description
        self.script = script
        self.requireConfirmation = False
        self.params = params

    def execute(self, parent, location, commands):
        """Execute the command."""
        input = None

        self.getParamValues()
        
        if globals.DISPLAY.confirmParams(self):
            globals.DISPLAY.printSeparator()
            self.runCommand()
        else:
            globals.DISPLAY.notice("Action cancelled.")

        self.resetParams()
        return []

    def getParamValues(self):
        """Get user input to evaluate all our parameters."""
        for param in self.params:
            param.evaluate()

    def resetParams(self):
        """Reset the values of all parameters so that next time
        this menu option is selected, all the default values are back."""
        for param in self.params:
            param.reset()

    def runCommand(self):
        """Actually run the command specified by the action, and the entered parameters."""

        # Build a list containing the command, followed by all the parameter values.
        systemString = self.script + [("%s %s" % (param.code,param.value)).strip() for param in self.params]

        message = "Action complete."
        process = None
        try:
            # Execute the command.
            process = subprocess.Popen(systemString, bufsize=-1)
            process.wait()
        except KeyboardInterrupt as e:
            message = "Action cancelled."
        except Exception as e:
            # For now display the error message. In future a generic message should be shown,
            # and the actual python error just logged.
            message = str(e)

        if process:
            # Ensure the process has terminated before continuing.
            # This prevents our output being overlapped by that of the process.
            process.wait()

        globals.DISPLAY.notice(message)

class Parameter(object):
    """A parameter represents one piece of input to a script."""
    def __init__(self, name, description, code="", default=None, choices=None):
        self.name = name
        self.description = description
        self.choices = choices
        self.code = code
        self.default = default
        self.value = None 

    def evaluate(self):
        """Evaluate the value of this parameter.
        Generally this means getting user input, but it doesn't have to."""
        globals.DISPLAY.evaluateParam(self)

    def reset(self):
        """Reset this parameter, so its default value will once again take precedent."""
        self.value = None
