import menu

option1 = menu.Action("Print Hello Print Hello","Prints 'Hello' to the screen.",["/bin/echo","Hello"])
option1.requireConfirmation = True
option2 = menu.Action("Print Goodbye","Prints 'Goodbye' to the screen.",["/bin/echo","Hello"])
subMenu = menu.Menu("Submenu", "More stuff.", [option1,option2])

topMenu = menu.Menu("A Menu","Some stuff to do.",[subMenu])

topMenu.execute(None,None);
