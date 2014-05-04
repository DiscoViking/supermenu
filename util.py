import os
from globals import *

def getChoice(items):
    """Get a single input value from the user."""
    input = raw_input("Enter Choice: ")
    textItems = [str(i) for i in items] + ["="]

    while input not in textItems:
        print("Not a valid choice.")
        input = raw_input("Enter Choice: ")

    return items[textItems.index(input)]

def getChoices():
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
        
def printSeparator():
    """DIsplays an obvious visual separator designed to separate menu levels etc."""
    if CLEAR_SCREEN:
        os.system("clear")
    else:
        print("\n%s\n" % ("-" * MENU_WIDTH))
 
def enterToContinue():
    """Utility function to request the user press enter to continue."""
    print("")
    raw_input("Press Enter to Continue.")
