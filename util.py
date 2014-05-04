import os
from globals import *

def getChoice(items):
  input = raw_input("Enter Choice: ")
  textItems = [str(i) for i in items] + ["="]

  while input not in textItems:
    print("Not a valid choice.")
    input = raw_input("Enter Choice: ")

  return items[textItems.index(input)]

def getChoices():
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
  if CLEAR_SCREEN:
    os.system("clear")
  else:
    print("\n%s\n" % ("-" * MENU_WIDTH))
 
def enterToContinue():
  print("")
  raw_input("Press Enter to Continue.")
