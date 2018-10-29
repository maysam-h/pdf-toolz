#!/usr/bin/python3

"""

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

""" **************************** | Helper functions and variables | **************************** """
__loadedFileName__ = ""


def askPrompt(title, promptText):
    """ this function when called, prompts the user for a text """
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
        if(disarmStatus):
            messagebox.showinfo(gis.__disarm_title__, "The PDF file (" + __loadedFileName__ + ") is disarmed. The Javascript (if any) in PDF file is removed and a copy of the file is saved in the same path.")
        return str(outputResult)
    else:
        return gis.__pdf_not_selected__


def isVariableBlank(str):

    if (str == None):
        return ""
    else:
        return " " + str


def createTab(tabName, frameName):
    """ This function after creating the notebook, creates a tab """

    tabVariable = ttk.Frame(frameName)
    frameName.add(tabVariable, text=tabName)

    return tabVariable


def createChkBox(location, textString, variableName, fontLabel, rowLabel, columnLabel, stickyLabel):
    """ this function creates a checkbox using the given information """
    # TODO remove the extra parameter " variableName "

    variableName = BooleanVar()
    variableName.set(False)
    Checkbutton(location, text=textString, var=variableName, wraplength=300, justify=LEFT, padx=5, pady=5, font=fontLabel).grid(row=rowLabel, column=columnLabel, sticky=stickyLabel)
    return variableName


""" **************************** | Make Command ready functions | **************************** """

def makeThePDFIdCommandReady(nbr):
    """ This function makes the PDF ID command ready and prints the result to the textbox """

    #{"allNames": allNames, "extraData": extraData, "noZero": noZero, "noJavascript": noJavascript, "fileScan": fileScan,
     #"outputLogFile": outputLogFile}

    switchesList = []
    programName = gis.__pdf_id_name__


    if(nbr["allNames"].get() == True):
        switchesList.append("-a")

    if (nbr["extraData"].get() == True):
        switchesList.append("-e")

    if (nbr["noZero"].get() == True):
        switchesList.append("-n")

    if (nbr["noJavascript"].get() == True):
        switchesList.append("-d")

    if (nbr["fileScan"].get() == True):
        switchesList.append("-s")

    if (nbr["outputLogFile"].get() == True):
        outfileName = askPrompt(gis.__file_prompt_title__, gis.__output_file_text__)
        switchesList.append("-o " + outfileName + ".txt")
    else:
        switchesList.append("")

    result = excuteCommand(programName, switchesList, gis.__loaded_file_path__)
    outputFunctions.addTextToTextBox(result)


def makeThePDFParseCommandReady(nbr):
    """ This function makes the PDF parser command ready and prints the result to the textbox """

    #optionsArr = {"objectId": objectId, "displayHash": displayHash, "pythonFromObjID": pythonFromObjID,
    # "pythonFromParsedPDF": pythonFromParsedPDF, "rawOutput": rawOutput, "displayStats": displayStats, "displayDebug": displayDebug}

    switchesList = []
    programName = gis.__pdf_parser_name__

    if (nbr["objectId"].get() == True):
        objectId = askPrompt(gis.__object_id_title__, gis.__object_id_text__)
        switchesList.append("-o" + objectId)

    if (nbr["displayHash"].get() == True):
        switchesList.append("-H")

    if (nbr["pythonFromObjID"].get() == True):
        outputfilename = askPrompt(gis.__object_id_title__, gis.__generateembedded_text__)
        switchesList.append("--generateembedded=" + outputfilename)

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


def makePDFCreationCommandReady(nbr, embedStatus):
    """ This function prepares the PDF embedded and javascript to pd command ready and prints the result in textbox """

    # optionsArr = {"openAutomatically": openAutomatically, "buttonToLaunch": buttonToLaunch,
    #               "hideEmbededFile": hideEmbededFile, "textToDisplay": textToDisplay,
    #               "fileNameInPDFObj": fileNameInPDFObj, "javascriptCode": javascriptCode,
    #               "javascriptFile": javascriptFile}

    #./PDF-Tools/makepdf/make-pdf-embedded.py --name=testEmbed.txt --message='_a test message for embeding in pdf file_' -b -a ./PDF-Tools/myfile.txt ./PDF-Tools/mypdf.pdf


    switchesList = []
    programName = ""

    if(embedStatus):
        # ******************** for embedding ********************

        if (nbr["openAutomatically"].get() == True):
            switchesList.append("-a")

        if (nbr["buttonToLaunch"].get() == True):
            switchesList.append("-b")

        if (nbr["hideEmbededFile"].get() == True):
            switchesList.append("-s")

        if (nbr["textToDisplay"].get() == True):
            msgText = askPrompt(gis.__type_message_title__, gis.__type_display_text)
            switchesList.append("-m '" + msgText + "'")

        if (nbr["fileNameInPDFObj"].get() == True):
            displayfilename = askPrompt(gis.__display_file_name__, gis.__display_file_text__)

            displayfilename = isVariableBlank(displayfilename)

            switchesList.append("-n" + displayfilename)

        else:
            switchesList.append("")

        programName = gis.__make_pdf_embedded_name__

    else:
        # ******************** for JS ********************

        if (nbr["javascriptCode"].get() == True):
            jsCode = askPrompt(gis.__javascript_title__, gis.__javascript_msg__)

            jsCode = isVariableBlank(jsCode)
            switchesList.append("-j" + jsCode)

        if (nbr["javascriptFile"].get() == True):
            jsFile = askPrompt(gis.__javascript_title__, gis.__javascript_file__)
            jsFile = isVariableBlank(jsFile)
            switchesList.append("-f" + jsFile)

        else:
            switchesList.append("")

        programName = gis.__make_pdf_javascript_name__


    result = excuteCommand(programName, switchesList, gis.__loaded_file_path__)
    outputFunctions.addTextToTextBox(result)


""" **************************** | Creaet content for tabs functions | **************************** """

def createPDFidContent(pdfIDTab):
    """ function creates the content of the PDF ID tab and add its options """

    allNames = createChkBox(pdfIDTab, "Display all the names", "allNames", "none 10", 2, 0, W)
    extraData = createChkBox(pdfIDTab, "Display extra data", "extraData", "none 10", 3, 0, W)
    noZero = createChkBox(pdfIDTab, "No zeros (supress output for counts equal to zero)", "noZero", "none 10", 4, 0, W)
    noJavascript = createChkBox(pdfIDTab, "Disable JavaScript and auto launch", "noJavascript", "none 10", 5, 0, W)
    fileScan = createChkBox(pdfIDTab, "force the scan of the file, even without proper %PDF header", "fileScan", "none 10", 6, 0, W)
    outputLogFile = createChkBox(pdfIDTab, "Output to log file", "outputLogFile", "none 10", 7, 0, W)

    optionsArr = {"allNames": allNames, "extraData": extraData, "noZero": noZero, "noJavascript": noJavascript, "fileScan": fileScan, "outputLogFile": outputLogFile}
    Button(pdfIDTab, text="OK", width=14, command= lambda: makeThePDFIdCommandReady(optionsArr)).grid(row=9, column=0, sticky=W)


def createPDFParserContent(pdfParseTab):
    """ function creates the content of PDF parser tab and add its options """

    objectId = createChkBox(pdfParseTab, "Object ID", "objectId", "none 10", 0, 0, W)
    displayHash = createChkBox(pdfParseTab, "Display Hash", "displayHash", "none 10", 1, 0, W)
    pythonFromObjID = createChkBox(pdfParseTab, "Generate Python program from object ID", "pythonFromObjID", "none 10", 2, 0, W)
    pythonFromParsedPDF = createChkBox(pdfParseTab, "Generate Python program from parsed PDF file", "pythonFromParsedPDF", "none 10", 3, 0, W)
    rawOutput = createChkBox(pdfParseTab, "Raw output for data and filters", "rawOutput", "none 10", 4, 0, W)
    displayStats = createChkBox(pdfParseTab, "Display stats for pdf document", "displayStats", "none 10", 5, 0, W)
    displayDebug = createChkBox(pdfParseTab, "Display debug info", "displayDebug", "none 10", 6, 0, W)

    optionsArr = {"objectId": objectId, "displayHash": displayHash, "pythonFromObjID": pythonFromObjID, "pythonFromParsedPDF": pythonFromParsedPDF, "rawOutput": rawOutput, "displayStats": displayStats, "displayDebug": displayDebug}
    Button(pdfParseTab, text="Ok", width=14, command= lambda: makeThePDFParseCommandReady(optionsArr)).grid(row=8, column=0, sticky=W)


def createMakePDFContent(makePDFTab):
    """ function creates the content of the make PDF tab and add its options """

    Label(makePDFTab, text="Embed to PDF", font="none 10").grid(row=8, column=0, sticky=W)
    openAutomatically = createChkBox(makePDFTab, "Open the embedded file automatically", "openAutomatically", "none 10", 0, 0, W)
    buttonToLaunch = createChkBox(makePDFTab, "Add a 'button' to launch the embedded file", "buttonToLaunch", "none 10", 1, 0, W)
    hideEmbededFile = createChkBox(makePDFTab, "Hide the embedded file", "hideEmbededFile", "none 10", 2, 0, W)
    textToDisplay = createChkBox(makePDFTab, "Text to display in the PDF document", "textToDisplay", "none 10", 3, 0, W)
    fileNameInPDFObj = createChkBox(makePDFTab, "Filename to use in PDF objects or none for default one", "fileNameInPDFObj", "none 10", 4, 0, W)

    optionsArrEmbed = {"openAutomatically": openAutomatically, "buttonToLaunch": buttonToLaunch, "hideEmbededFile": hideEmbededFile, "textToDisplay": textToDisplay, "fileNameInPDFObj": fileNameInPDFObj}
    Button(makePDFTab, text="Embed", width=14, command=lambda: makePDFCreationCommandReady(optionsArrEmbed, True)).grid(row=5, column=0, sticky=W)


    Label(makePDFTab, text="", font="none 10").grid(row=6, column=0, sticky=W)
    Label(makePDFTab, text="", font="none 10").grid(row=7, column=0, sticky=W)
    Label(makePDFTab, text="Add Javascript to PDF", font="none 10").grid(row=8, column=0, sticky=W)
    javascriptCode = createChkBox(makePDFTab, "Type Javascript to embed or none for default code", "javascriptCode", "none 10", 9, 0, W)
    javascriptFile = createChkBox(makePDFTab, "Select Javascript file to embed or none for default", "javascriptFile", "none 10", 10, 0, W)

    optionsArrJavascript = {"javascriptCode": javascriptCode, "javascriptFile": javascriptFile}
    Button(makePDFTab, text="Add", width=14, command=lambda: makePDFCreationCommandReady(optionsArrJavascript, False)).grid(row=11, column=0, sticky=W)


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
    createPDFidContent(pdfIDTab)


    #  ------------ Add the content of the PDF parser (tab) here -------------
    createPDFParserContent(pdfParseTab)

    #  ------------ Add the content of the PDF embedded (tab) here -------------
    createMakePDFContent(makePDFTab)

    #  ------------ Add the content of the PDF Hash (tab) here -------------
    createPDFInfoContent(pdfInfoTab)