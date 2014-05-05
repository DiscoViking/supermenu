import os
from settings import *

def getChoice(items):
    """Get a single input value from the user."""
    input = raw_input("Enter Choice: ")
    textItems = [str(i) for i in items] + ["="]

    while input not in textItems:
        print("Not a valid choice.")
        input = raw_input("Enter Choice: ")

    return items[textItems.index(input)]
        
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
