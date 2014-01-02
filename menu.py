import os
import subprocess
import time

from globals import *
from util import *


class Menu(object):
  def __init__(self, name, description, children):
    self.children = children
    self.name = name
    self.description = description
    self.returningHome = False
    self.parent = None
    self.location = None

  def execute(self, parent, location, commands=[]):
    self.parent = parent
    self.location = location

    choice = ""

    while choice != 0 and not self.returningHome:
      printSeparator()
      print(time.asctime(time.localtime()).rjust(MENU_WIDTH))
      print("%s [%s]" % ((self.name, self.locationString().strip())))
      print(self.description)
 
      backAction = Action("Back", "Go up a menu level", None)
      
      validChildren = [backAction] + [child for child in self.children if self.isValid(child)]    

      for i in range(len(validChildren)):
	      print("  %d: %s %s" % (i, validChildren[i].name.ljust(MAX_ITEM_NAME_LEN)[:MAX_ITEM_NAME_LEN], validChildren[i].description))

      if len(commands) == 0:
        commands = getChoices()

      if len(commands) != 0:
        choice = commands[0]
        commands = commands[1:]
        if choice == "=":
          self.returnHome()
        elif choice != 0:
          commands = validChildren[choice].execute(self,choice,commands)

    self.returningHome = False
    printSeparator()
    return commands

  def isValid(self, item):
    return True

  def returnHome(self):
    if self.parent != None:
      self.parent.returnHome()

    self.returningHome = True 

  def locationString(self):
    if self.parent == None:
      return "="
    
    return self.parent.locationString() + " " + str(self.location)

class Action(object):
  def __init__(self, name, description, script):
    self.name = name
    self.description = description
    self.script = script
    self.requireConfirmation = False

  def execute(self, parent, location, commands):
    input = None

    if self.requireConfirmation:
      printSeparator()
      print(self.description)
      print("")
      input = raw_input("Are you sure?(y/n): ")
    else:
      input = 'y'
    
    if input == 'y':
      printSeparator()
      subprocess.call(self.script)
    else:
      print("Action cancelled.")

    enterToContinue()
    return []
