#!/usr/bin/python3

"""
# TODO: filemenu.add_command(label = "Save as...", command = donothing) This function will be implemented later to save the puur pdf and without its attached files
# TODO: keep the 'unload the file' button disabled until a PDF file is added
"""

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import guideInfoStrings as gis
import tabs
import outputFunctions
import os
import run


def openDocumentPage():
    print("")

def goToTab(number):
    """ when this function is called it will set the specified tab active """

    tabs.frameN.select(number)


def loadFile(program):
    """ This function will open a browse box from where the user can select a pdf file to load it to the program """

    gis.__loaded_file_path__ = filedialog.askopenfilename(initialdir="./", title="Choose a PDF file to analyse", filetypes=[("PDF files", "*.pdf"),("All files","*.*")])
    gis.__loaded_file_name__ = os.path.split(gis.__loaded_file_path__)[1]
    tabs.__loadedFileName__ = gis.__loaded_file_name__
    run.updateVariableText(program, "File: " + tabs.__loadedFileName__)
    outputFunctions.addTextToTextBox("The PDF file '" + gis.__loaded_file_name__ + "' is loaded.")


def closeTheFile(program):
    """ This function will unload the loaded file """

    if(gis.__loaded_file_name__ != ""):
        outputFunctions.addTextToTextBox("The PDF file '" + gis.__loaded_file_name__ + "' is unloaded.")
        gis.__loaded_file_path__ = ""
        gis.__loaded_file_name__ = ""
        run.updateVariableText(program, "")


def aboutInfo():
    """ This function will load the about dialog box """
    messagebox.showinfo(gis.__about_title__, gis.__about_message__)


def createMenu(program):
    """ This function creates the menus and this is the main function of this page """

    menubar = Menu(program)
    filemenu = Menu(menubar, tearoff = 0)

    # .................. the file menu begins here
    filemenu.add_command(label="   Load   ", command = lambda: loadFile(program))
    filemenu.add_command(label = "   Close   ", command = lambda: closeTheFile(program))
    filemenu.add_separator()
    filemenu.add_command(label = "   Exit   ", command = program.quit)

    menubar.add_cascade(label = "File", menu = filemenu)

    # .................. the tools menu begins here
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="   PDF id   ", command= lambda: goToTab(0))
    filemenu.add_command(label="   PDF Parser   ", command= lambda: goToTab(1))
    filemenu.add_command(label="   Make PDF   ", command= lambda: goToTab(2))

    menubar.add_cascade(label="Tools", menu=filemenu)

    # .................. the help menu begins here
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="   Info   ", command= lambda: goToTab(3))
    helpmenu.add_separator()
    helpmenu.add_command(label="   About   ", command=aboutInfo)

    menubar.add_cascade(label="Help", menu=helpmenu)

    program.config(menu=menubar)

