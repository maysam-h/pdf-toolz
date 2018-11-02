#!/usr/bin/python3

"""
"""


from tkinter import *
import tabs
import guideInfoStrings as gis
import outputFunctions
import menubar


def updateVariableText(thisTab, returnString):
    """ This function updates the label when called """
    change = StringVar(thisTab)
    change.set(returnString)
    return Label(thisTab, textvar=change, fg="black", font="bold").grid(row=0, column=0, sticky=W+E)


def main():
    """ everything begins from here """


    program = Tk()
    program.title(gis.__app_name__)
    #program.configure(background=gis.__color_darkgrey__)
    program.geometry(gis.__app_width_height__)
    program.resizable(0,0)

    """ creating the menubar and menus """
    menubar.createMenu(program)

    """ Createing the first label on the page """
    updateVariableText(program, "")


    Button(program, text="Unload PDF file", width=10, command= lambda: menubar.closeTheFile(program)).grid(row=0, column=1, sticky=W+E)
    Button(program, text="Exit", width=3, command=program.quit).grid(row=0, column=2, sticky=E+W)


    """ creating the tabs """
    tabs.createTabframeAndTab(program)

    """ creating the output box """
    outputFunctions.insertCommandOutputBox(program)

    program.mainloop()


if __name__ == '__main__':
    main()