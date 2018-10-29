#!/usr/bin/python3
"""

"""


from tkinter import *
import guideInfoStrings as gis


def addTextToTextBox(inputText):
    """ this function upates the text area when called with the required parameter """

    output.config(state="normal")
    output.delete(1.0, END)
    output.insert(INSERT, inputText)
    output.config(state="disabled")


def insertCommandOutputBox(program):

    global output

    scrolTextBox = Scrollbar(program, orient=VERTICAL)


    output = Text(program, width=75, height=38, wrap=WORD, background=gis.__color_lightgrey__, yscrollcommand=scrolTextBox.set)
    output.grid(row=2, column=1, columnspan=2, sticky=W)

    addTextToTextBox('')

    scrolTextBox.grid(row=2, column=4, sticky=N+S+W)
    scrolTextBox.config(command=output.yview)
