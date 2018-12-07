#!/usr/bin/python3

"""
    __Reference:


    #TODO:
        * the 'make*commandready() funtions can be added to an key value array and if the key was not in array return false

        * for PDFiD:
                . Scan Directory
                . Select Plugins
                . Output CSV data
                . Selection expression
                . Plugin Options
                . Literal file names (no wildcards)

        * for PDF-Parser
                . type of elements to select (cxtsi)
                . type of indirect object to select
                . filename to extract malformed content to
                . filename to dump stream content to
                . display the content for objects without streams or with streams without filters
                . string to search in streams
                . search in unfiltered streams
                . string to search in indirect objects (except streams)
                . pass stream object through filters (FlateDecode, ASCIIHexDecode, ASCII85Decode, LZWDecode and RunLengthDecode only)
                . id of indirect object being referenced (version  independent)
                . YARA rule (or directory or @file) to check streams (can be used with option --unfiltered)
                . Print YARA strings
                . key to search in dictionaries
                . use regex to search in streams
                . case sensitive search in streams

        * for make-pdf-embedded
                . filters to apply, f for FlateDecode (default), h for ASCIIHexDecode
                . don't add the comment for binary format

"""


from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import os
import outputFunctions
import guideInfoStrings as gis
import run

""" **************************** | Helper functions and variables | **************************** """
__loadedFileName__ = ""


def askPrompt(title, promptText):
    """ this function prompts the user for a text """
    userInput = simpledialog.askstring(title, promptText)
    return userInput


def excuteCommand(command, switchesList, targetFile):
    """ This function receives the complete command in three parameters (program [options] pdf-file) and after running the command returns the result as a string """
    disarmStatus = False

    if(targetFile != ""):
        stringOfSwitches = ""
        for i in range(len(switchesList)):
            stringOfSwitches += switchesList[i] + " "
            if(switchesList[i] == "-d"):
                disarmStatus = True

        commandStr = command + " " + stringOfSwitches + targetFile

        outputResult = os.popen(commandStr).read()


        """ subprocess does not work here with 3 argument """
        #import subprocess
        #commandStr = stringOfSwitches + targetFile
        #commandResult = subprocess.run([command, commandStr], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #outputResult = commandResult.stdout.decode('utf-8')

        if(disarmStatus):
            messagebox.showinfo(gis.__disarm_title__, "The PDF file (" + __loadedFileName__ + ") is disarmed. The Javascript (if any) in PDF file is removed and a copy of the file is saved in the same path.")
        return str(outputResult)
    else:
        return gis.__pdf_not_selected__



def createTab(tabName, frameName):
    """ This function after creating the notebook, creates a tab """

    # Adds tab of the notebook
    tabVariable = ttk.Frame(frameName)
    frameName.add(tabVariable, text=tabName)

    return tabVariable


def createChkBox(location, textString, fontLabel, rowLabel, columnLabel, stickyLabel):
    """ this function creates a checkbox using the given information """

    variableName = BooleanVar()
    variableName.set(False)
    Checkbutton(location, text=textString, var=variableName, wraplength=300, justify=LEFT, padx=5, pady=5, font=fontLabel).grid(row=rowLabel, column=columnLabel, sticky=stickyLabel)
    return variableName


def isInteger(char):
    try:
        int(char)
        return True
    except ValueError:
        return False



""" **************************** | Make Command ready functions | **************************** """

def makeThePDFIdCommandReady(program, nbr):
    """ This function makes the PDF ID command ready and prints the result to the textbox """

    switchesList = []
    programName = gis.__pdf_id_name__
    outFileStatus = False
    outFileNameStr = ""


    if(nbr["allNames"].get() == True):
        switchesList.append("-a")

    if (nbr["extraData"].get() == True):
        switchesList.append("-e")

    if (nbr["noZero"].get() == True):
        switchesList.append("-n")

    if (nbr["noJavascript"].get() == True):
        switchesList.append("-d")

    if (nbr["fileScan"].get() == True):
        switchesList.append("-f")

    if (nbr["outputLogFile"].get() == True):
        outfileName = askPrompt(gis.__file_prompt_title__, gis.__output_file_text__)
        if(outfileName == '' or outfileName == None):
            messagebox.showerror(gis.__noOutPutName_title__, gis.__noOutPutName_text__)
        else:
            outFileStatus = True
            outFileNameStr = outfileName + ".txt"
            switchesList.append("-o " + outFileNameStr)

    if (nbr["scanADirectory"].get() == True):
        directoryPath = askPrompt(gis.__directorypath_title__, gis.__directorypath_text__)
        if(directoryPath == '' or directoryPath == None):
            messagebox.showinfo(gis.__directorypath_NO_title__, gis.__directorypath_NO_text__)
            return
        else:
            gis.__loaded_file_path__ = directoryPath
            run.updateVariableText(program, "Directory: " + directoryPath)
            switchesList.append("-s")

    else:
        switchesList.append("")


    result = excuteCommand(programName, switchesList, gis.__loaded_file_path__)
    # if an output file name was provided this check will print a line on screen
    if(outFileStatus):
        result += "This output is also saved in the choosen file (" + outFileNameStr + ")"
        outputFunctions.addTextToTextBox(result)
    else:
        outputFunctions.addTextToTextBox(result)


def makeThePDFParseCommandReady(nbr):
    """ This function makes the PDF parser command ready and prints the result to the textbox """

    switchesList = []
    programName = gis.__pdf_parser_name__

    if (nbr["objectId"].get() == True):
        objectId = askPrompt(gis.__object_id_title__, gis.__object_id_text__)
        if (objectId == '' or objectId == None):
            messagebox.showerror(gis.__noObjectId_title__, gis.__noObjectId_text__)
        else:
            # checks whether the input is an integer or not
            if (isInteger(objectId)):
                switchesList.append("-o" + objectId)
            else:
                messagebox.showerror(gis.__noObjectId_title__, gis.__noObjectId_2_text__)

    if (nbr["displayHash"].get() == True):
        switchesList.append("-H")

    if (nbr["pythonFromObjID"].get() == True):
        outputfilename = askPrompt(gis.__object_id_title__, gis.__generateembedded_text__)
        if(outputfilename == '' or outputfilename == None):
            messagebox.showerror(gis.__noObjectId_title__, gis.__noPythonObjectId_text__)
            switchesList.append("--generateembedded=1")
        else:
            # checks whether the input is an integer or not
            if(isInteger(outputfilename)):
                switchesList.append("--generateembedded=" + outputfilename)
            else:
                messagebox.showerror(gis.__noObjectId_title__, gis.__noPythonObjectId_text__)
                switchesList.append("--generateembedded=1")

    if (nbr["pythonFromParsedPDF"].get() == True):
        switchesList.append("-g")

    if (nbr["rawOutput"].get() == True):
        switchesList.append("-w")

    if (nbr["displayStats"].get() == True):
        switchesList.append("-a")

    if (nbr["displayDebug"].get() == True):
        switchesList.append("-D")

    else:
        switchesList.append("")

    result = excuteCommand(programName, switchesList, gis.__loaded_file_path__)
    outputFunctions.addTextToTextBox(result)


def makePDFCreationCommandReady(nbr):
    """ This function prepares the PDF embedded and javascript to pd command ready and prints the result in textbox """

    switchesList = []
    programName = ""


    payloadFilePath = askPrompt(gis.__enter_embedding_file_path_title__, gis.__enter_embedding_file_path_text__)

    if(payloadFilePath != '' and payloadFilePath != None):
        # file name of the file to be embedded is provided

        if (nbr["openAutomatically"].get() == True):
            switchesList.append("-a")

        if (nbr["buttonToLaunch"].get() == True):
            switchesList.append("-b")

        if (nbr["hideEmbededFile"].get() == True):
            switchesList.append("-s")

        if (nbr["textToDisplay"].get() == True):
            msgText = askPrompt(gis.__type_message_title__, gis.__type_message_text)
            if (msgText == '' or msgText == None):
                # no message given
                messagebox.showerror(gis.__type_message_error_title__, gis.__type_message_error_text__)
            else:
                # print this msg
                switchesList.append("-m '" + msgText + "'")

        if (nbr["fileNameInPDFObj"].get() == True):
            displayfilename = askPrompt(gis.__display_file_name__, gis.__display_file_text__)
            if (displayfilename == '' or displayfilename == None):
                # cancelled or left blank
                messagebox.showerror(gis.__javascript_file_add_error_title__, gis.__javascript_file_add_error_text__)
            else:
                # file name provided
                switchesList.append("-n " + displayfilename)

        else:
            switchesList.append("")

        switchesList.append(payloadFilePath)
        programName = gis.__make_pdf_embedded_name__

        newPDFfilename = askPrompt(gis.__new_file_name_title__, gis.__new_file_name_text__)
        if (newPDFfilename == '' or newPDFfilename == None):
            # if user left blank or cancelled
            messagebox.showerror(gis.__no_new_file_name_title__, gis.__no_new_file_name_text__)
            gis.__loaded_file_path__ = "javascriptCodePDF.pdf"
        else:
            gis.__loaded_file_path__ = newPDFfilename + ".pdf"

        result = excuteCommand(programName, switchesList, gis.__loaded_file_path__)
        # its a string
        print("S.......................................")
        print(type(result))
        print(result)
        print(".......................................E")
        outputFunctions.addTextToTextBox(result)

    else:
        # file name not provided
        messagebox.showerror(gis.__no_payload_file_selected_title__, gis.__no_payload_file_selected_text__)
        outputFunctions.addTextToTextBox(" ")



def makeJavascriptPDFCommandReady(nbr):

    # TODO: the program does not return shell errors like " /bin/sh: 1: Syntax error: "(" unexpected " that is why the program can't inform the user that the pdf is saved successfully
    # TODO: beccause when it causes a shell error or when it successfully executes the command, it always returns empty string
    # TODO: alert the user if the command successfully created the file

    switchesList = []
    programName = ""

    if (nbr["javascriptCode"].get() == True):
        jsCode = askPrompt(gis.__javascript_title__, gis.__javascript_msg__)
        if (jsCode == '' or jsCode == None):
            # cancelled or left blank
            messagebox.showerror(gis.__no_javascript_title__, gis.__no_javascript_text__)
        else:
            # js code provided
            switchesList.append("-j" + jsCode)

    if (nbr["javascriptFile"].get() == True):
        jsFile = askPrompt(gis.__javascript_title__, gis.__javascript_file__)
        if (jsFile == '' or jsFile == None):
            # cancelled or left blank
            messagebox.showerror(gis.__no_javascript_file_title__, gis.__no_javascript_file_text__)
        else:
            # js file provided
            switchesList.append("-f" + jsFile)

    else:
        switchesList.append("")


    programName = gis.__make_pdf_javascript_name__
    newPDFname = askPrompt(gis.__new_file_name_title__, gis.__new_file_name_text__)
    if (newPDFname == '' or newPDFname == None):
        # if user left blank or cancelled
        messagebox.showerror(gis.__no_new_file_name_title__, gis.__no_new_file_name_text__)
        gis.__loaded_file_path__ = "javascriptembeddedPDF.pdf"
    else:
        gis.__loaded_file_path__ = newPDFname + ".pdf"


    result = excuteCommand(programName, switchesList, gis.__loaded_file_path__)
    # its a string .......... see todo for more info
    outputFunctions.addTextToTextBox(result)


""" **************************** | Creaet content for tabs functions | **************************** """

def createPDFidContent(program, pdfIDTab):
    """ function creates the content of the PDF ID tab and add its options """

    allNames = createChkBox(pdfIDTab, "Display all the names", "none 10", 2, 0, W)
    extraData = createChkBox(pdfIDTab, "Display extra data", "none 10", 3, 0, W)
    noZero = createChkBox(pdfIDTab, "No zeros (supress output for counts equal to zero)", "none 10", 4, 0, W)
    noJavascript = createChkBox(pdfIDTab, "Disable JavaScript and auto launch", "none 10", 5, 0, W)
    fileScan = createChkBox(pdfIDTab, "force the scan of the file, even without proper %PDF header", "none 10", 6, 0, W)
    outputLogFile = createChkBox(pdfIDTab, "Output to log file", "none 10", 7, 0, W)
    scanADirectory = createChkBox(pdfIDTab, "Scan a directory", "none 10", 8, 0, W)

    optionsArr = {"allNames": allNames, "extraData": extraData, "noZero": noZero, "noJavascript": noJavascript, "fileScan": fileScan, "outputLogFile": outputLogFile, "scanADirectory": scanADirectory}
    Button(pdfIDTab, text="OK", width=14, command= lambda: makeThePDFIdCommandReady(program, optionsArr)).grid(row=9, column=0, sticky=W)


def createPDFParserContent(pdfParseTab):
    """ function creates the content of PDF parser tab and add its options """

    objectId = createChkBox(pdfParseTab, "Object ID", "none 10", 0, 0, W)
    displayHash = createChkBox(pdfParseTab, "Display Hash", "none 10", 1, 0, W)
    pythonFromObjID = createChkBox(pdfParseTab, "Generate Python program from object ID", "none 10", 2, 0, W)
    pythonFromParsedPDF = createChkBox(pdfParseTab, "Generate Python program from parsed PDF file", "none 10", 3, 0, W)
    rawOutput = createChkBox(pdfParseTab, "Raw output for data and filters", "none 10", 4, 0, W)
    displayStats = createChkBox(pdfParseTab, "Display stats for pdf document", "none 10", 5, 0, W)
    displayDebug = createChkBox(pdfParseTab, "Display debug info", "none 10", 6, 0, W)

    optionsArr = {"objectId": objectId, "displayHash": displayHash, "pythonFromObjID": pythonFromObjID, "pythonFromParsedPDF": pythonFromParsedPDF, "rawOutput": rawOutput, "displayStats": displayStats, "displayDebug": displayDebug}
    Button(pdfParseTab, text="Ok", width=14, command= lambda: makeThePDFParseCommandReady(optionsArr)).grid(row=8, column=0, sticky=W)


def createMakePDFContent(makePDFTab):
    """ function creates the content of the make PDF tab and add its options """

    Label(makePDFTab, text="Embed to PDF", font="none 10").grid(row=8, column=0, sticky=W)
    openAutomatically = createChkBox(makePDFTab, "Open the embedded file automatically", "none 10", 0, 0, W)
    buttonToLaunch = createChkBox(makePDFTab, "Add a 'button' to launch the embedded file", "none 10", 1, 0, W)
    hideEmbededFile = createChkBox(makePDFTab, "Hide the embedded file", "none 10", 2, 0, W)
    textToDisplay = createChkBox(makePDFTab, "Text to display in the PDF document", "none 10", 3, 0, W)
    fileNameInPDFObj = createChkBox(makePDFTab, "Filename to use in PDF objects or none for default one", "none 10", 4, 0, W)

    optionsArrEmbed = {"openAutomatically": openAutomatically, "buttonToLaunch": buttonToLaunch, "hideEmbededFile": hideEmbededFile, "textToDisplay": textToDisplay, "fileNameInPDFObj": fileNameInPDFObj}
    Button(makePDFTab, text="Embed", width=14, command=lambda: makePDFCreationCommandReady(optionsArrEmbed)).grid(row=5, column=0, sticky=W)


    Label(makePDFTab, text="", font="none 10").grid(row=6, column=0, sticky=W)
    Label(makePDFTab, text="", font="none 10").grid(row=7, column=0, sticky=W)
    Label(makePDFTab, text="Add Javascript to PDF", font="none 10").grid(row=8, column=0, sticky=W)
    javascriptCode = createChkBox(makePDFTab, "Type Javascript to embed or none for default code", "none 10", 9, 0, W)
    javascriptFile = createChkBox(makePDFTab, "Select Javascript file to embed or none for default", "none 10", 10, 0, W)

    optionsArrJavascript = {"javascriptCode": javascriptCode, "javascriptFile": javascriptFile}
    Button(makePDFTab, text="Add", width=14, command=lambda: makeJavascriptPDFCommandReady(optionsArrJavascript)).grid(row=11, column=0, sticky=W)


def createLabel(aboutPage, title, text, row):
    """ this function creates two labels, first the title and the seond is the text """
    Label(aboutPage, text=title, wraplength=300, justify=LEFT, font="bold 9").grid(row=row, column=0, padx=(10, 10), sticky=W)
    Label(aboutPage, text=text, wraplength=300, justify=LEFT, font="none 9").grid(row=row+1, column=0, padx=(10, 10), sticky=W)


def createPDFInfoContent(pdfInfoTab):
    """ this function add the content of the info tab """

    createLabel(pdfInfoTab, gis.__app_name__, gis.__aboutPage_about_text__, 0)
    createLabel(pdfInfoTab, gis.__aboutPage_PDFiD_title__, gis.__aboutPage_PDFiD_text__, 2)
    createLabel(pdfInfoTab, gis.__aboutPage_PDFParser_title__, gis.__aboutPage_PDFParser_text__, 4)
    createLabel(pdfInfoTab, gis.__aboutPage_PDFEmbedded_title__, gis.__aboutPage_PDFEmbedded_text__, 8)
    createLabel(pdfInfoTab, gis.__aboutPage_PDFJavascript_title__, gis.__aboutPage_PDFJavascript_text__, 10)


""" **************************** | main function of this page | **************************** """

def createTabframeAndTab(program):
    """ function creates the tabs """
    global frameN

    frameN = ttk.Notebook(program, width=350, height=513)
    frameN.grid(row=2, column=0, sticky=N)

    pdfIDTab = createTab('PDF Id', frameN)
    pdfParseTab = createTab('PDF Parser', frameN)
    makePDFTab = createTab('Make PDF', frameN)
    pdfInfoTab = createTab('Info', frameN)


    #  ------------ Add the content of the PDF Id (tab) here -------------
    createPDFidContent(program, pdfIDTab)


    #  ------------ Add the content of the PDF parser (tab) here -------------
    createPDFParserContent(pdfParseTab)

    #  ------------ Add the content of the PDF embedded (tab) here -------------
    createMakePDFContent(makePDFTab)

    #  ------------ Add the content of the PDF Hash (tab) here -------------
    createPDFInfoContent(pdfInfoTab)