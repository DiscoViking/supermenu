import os

CLEAR_SCREEN = True 

def getChoice(items):
  input = raw_input("Enter Choice: ")
  textItems = [str(i) for i in items] + ["="]

  while input not in textItems:
    print("Not a valid choice.")
    input = raw_input("Enter Choice: ")

  return items[textItems.index(input)]

def getChoices():
  input = raw_input("Enter Choice: ")
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
    print("")
 
def enterToContinue():
  print("")
  raw_input("Press Enter to Continue.")
