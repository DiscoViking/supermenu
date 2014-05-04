import os
import subprocess
import time

import globals
from util import *
import value


class Item(object):
  def __init__(self):
    self.flags = []

  def addFlag(self, flag):
    self.flags.append(flag)

  def removeFlag(self, flag):
    self.flags.remove(flag)

  def isValid(self):
    for flag in self.flags:
      if not flag.isValid():
        return False
    return True

class Menu(Item):
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
    self.parent = parent
    self.location = location

    choice = ""

    while choice != 0 and not self.returningHome:
      printSeparator()
      self.printHeader()
 
      backAction = Menu("Back" if parent != None else "Exit", 
                        "Go up a menu level" if parent != None else "Exit the menu.", 
                        None)
      
      validChildren = [backAction] + [child for child in self.children if child.isValid()]    

      for i in range(len(validChildren)):
	print("  %d: %s %s %s" % (i, validChildren[i].name.ljust(globals.MAX_ITEM_NAME_LEN), 
                                  ">" if isinstance(validChildren[i], Menu) else " ",
                                  validChildren[i].description))

      if len(commands) == 0:
        commands = getChoices()

      if len(commands) != 0:
        choice = commands[0]
        commands = commands[1:]
        if choice == "=":
          self.returnHome()
        elif choice != 0:
          try:
            command = validChildren[choice]
          except:
            print("Not a valid command.")
            enterToContinue()
            commands = []
            command = None
          else:
            try:
              commands = command.execute(self, choice, commands)
            except KeyboardInterrupt:
              commands = []

    self.returningHome = False
    return commands

  def printHeader(self):
    print(time.strftime("%A, %d %b %Y %H:%M:%S %Z").rjust(globals.MENU_WIDTH))
    print("[%s] [%s]" % ((self.path(), self.locationString().strip())))
    print(self.description)

  def returnHome(self):
    if self.parent != None:
      self.parent.returnHome()

      self.returningHome = True 

  def locationString(self):
    if self.parent == None:
      return "="
    
    return self.parent.locationString() + " " + str(self.location)

  def path(self):
    if self.parent == None:
      return self.name
    
    return self.parent.path() + "->" + self.name

class Action(Item):
  def __init__(self, name, description, script, params=[]):
    super(Action,self).__init__()
    self.name = name
    assert(len(name) <= globals.MAX_ITEM_NAME_LEN)
    self.description = description
    self.script = script
    self.requireConfirmation = False
    self.params = params

  def execute(self, parent, location, commands):
    input = None

    self.getParamValues()
    
    if self.confirmParams():
      printSeparator()
      self.runCommand()
    else:
      print("Action cancelled.")

    self.resetParams()

    enterToContinue()
    return []

  def getParamValues(self):
    for param in self.params:
      param.evaluate()

  def resetParams(self):
    for param in self.params:
      param.reset()

  def confirmParams(self):
    if self.requireConfirmation:
      printSeparator()
      print(self.description)
      print("")

      for param in self.params:
        print("%s: %s" % (param.name, param.value))

      if len(self.params) > 0:
        print("")

      input = raw_input("Are you sure?(y/n): ")
      return True if input == 'y' else False
    else:
      return True

  def runCommand(self):
    systemString = self.script + [("%s %s" % (param.code,param.value)).strip() for param in self.params]
    message = "Action complete."

    process = None
    try:
      process = subprocess.Popen(systemString)
      process.wait()
    except KeyboardInterrupt as e:
      message = "Action cancelled."
    except Exception as e:
      message = str(e)

    if process:
      process.wait()
    print("")
    print(message)

class Parameter(object):
  def __init__(self, name, description, code="", default=None, choices=None):
    self.name = name
    self.description = description
    self.choices = choices
    self.code = code
    self.default = default
    self.value = None 

  def evaluate(self):
    printSeparator()
    print("%s %s" % (self.name.ljust(globals.MAX_ITEM_NAME_LEN), self.description))
    print("Default is %s" % (self.default if self.value == None else self.value))
    print("")
   
    while self.value == None: 
      input = raw_input("Enter Choice: ")
      if len(input) > 0:
        self.value = input
      else:
        self.value = self.default

  def reset(self):
    self.value = None
