from re import A
from turtle import color
import pyautogui
import time
from tkinter import *
from tkinter import filedialog
import os

def saveCommands():
    filePath = filedialog.asksaveasfilename()
    file = open(filePath,"w")
    file.write(textField.get(1.0,"end-1c"))
    file.close()

def loadCommands():
    filePath = filedialog.askopenfilename()
    file = open(filePath,"r")
    textField.insert("1.0",file.read())
    file.close()

def getColorAtPos():
    time.sleep(2.5)
    colorLabel.config(text="color at pos = " + str(pyautogui.pixel(pyautogui.position().x, pyautogui.position().y)))

#given a command list, go through them step by step and execute the appropriate command
def parseCommandList(list):

    #goes through each command in the list
    for command in list:

        command = command.split(":")

        #when code reaches repeat start statement
        if "--" in command[0] and command[0] != "----":
            command[0] = command[0].replace("--","")
            repeatTimes = int(command[0])
            onRepeatFlag = True
            repeatLines = []
            continue
        
        if 'onRepeatFlag' in locals():
            if onRepeatFlag and command[0] != "----":
                repeatLines.append(command)
        
        #end repeat statment
        if command[0] == "----":
            if 'repeatTimes' in locals():
                if repeatTimes > 1:
                    repeatTimes -= 1
                    repeatLines *= repeatTimes
                    for innerCommand in repeatLines:
                        parseCommand(innerCommand)

        parseCommand(command)

def parseCommand(command):
    if command[0] == "MOVE":
        coorList = command[1].split("x")
        pyautogui.moveTo(int(coorList[0]), int(coorList[1]))

    if command[0] == "WAIT":
        time.sleep(float(command[1]))
    if command[0] == "CLICK":
        pyautogui.click()
    if command[0] == "TYPE":
        pyautogui.write(command[1])
    if command[0] == "PRESS":
        pyautogui.press(command[1])
    if command[0] == "RIGHT CLICK":
        pyautogui.rightClick()
    if command[0] == "KEY DOWN":
        pyautogui.keyDown(command[1])
    if command[0] == "KEY UP":
        pyautogui.keyUp(command[1])
    if command[0] == "MOUSE DOWN":
        pyautogui.mouseDown()
    if command[0] == "MOUSE UP":
        pyautogui.mouseUp()
    if command[0] == "DOUBLE CLICK":
        pyautogui.doubleClick()
    if command[0] == "KILL":
        exit(0)
    if command[0] == "EXECUTE":
        os.system(command[1].strip())

    #structure:
    #WAIT FOR (R,G,B) AT (x,y)
    if "WAIT FOR" in command[0]:
        # list of RGB values where index[0] == R, index[1] == G, index[2] == B
        colorRGBList = command[0][command[0].index("(")+1:command[0].index(")")].strip().split(",")
        
        # [0] val in list = X coor, [1] == Y coor
        coordinateList = command[0][command[0].index("AT") + 4:].replace(')','').split(",")
        
        # while there isn't the specified color at specified coordinate, sleep and wait for color to show up
        while pyautogui.pixel(int(coordinateList[0]), int(coordinateList[1])).red != int(colorRGBList[0]) and pyautogui.pixel(int(coordinateList[0]), int(coordinateList[1])).green != int(colorRGBList[1]) and pyautogui.pixel(int(coordinateList[0]), int(coordinateList[1])).blue != int(colorRGBList[2]):
            time.sleep(0.1)

#returns a list of commands from the text box
def getTextBox():
    txt = textField.get(1.0,"end-1c")
    parseCommandList(txt.split("\n"))


#in specified seconds, gets mouse pos
def getMousePos():
    time.sleep(2.5)
    mousePosLabel.config(text="mouse pos = " + str(pyautogui.position().x) + "x" + str(pyautogui.position().y))

infoTxt = """MOVE: (posX)x(posY)
WAIT: (X, in seconds) OR ((R,G,B)) to wait for color to appear
WAIT FOR (R,G,B) AT (X,Y): waits for R,G,B value at X,Y coor
CLICK
RIGHT CLICK
DOUBLE CLICK
TYPE: (word(s) to type)
PRESS: (key to press, see allowed keys below)
KEY DOWN: (key to press, see allowed keys below)
KEY UP: (key to press, see allowed keys below)
MOUSE DOWN (similar to holding the right mouse button down)
MOUSE UP (release right mouse button)
KILL: exits program with 0 exit status
EXECUTE: (shell), executes a line in the terminal  
--(#)-- = repeat code # of times
---- = end repeat (must have started it)
"""

#load text file containing instructions from argument list
window = Tk()

window.title("Action automater")
window.geometry("1000x600")

#text field to type stuff
textField = Text(window,bg="white",width=70,height=20)
textField.place(in_=window,relx=0,rely=0)

#button to execute written code
executeButton = Button(window,text="Execute",padx=20,pady=5,command=getTextBox)
executeButton.place(in_=textField,relx=0,rely=1.0,y=10)

#button to get mouse position on screen
mousePosButton = Button(window,text="Get Mouse Position",padx=20,pady=5,command=getMousePos)
mousePosButton.place(in_=executeButton,relx=1.0,rely=0,x=5,y=-2)

#button to get color on screen
colorButton = Button(window,text="Get Color at Position",padx=20,pady=5,command=getColorAtPos)
colorButton.place(in_=mousePosButton,relx=1.0,rely=0,x=5,y=-2)

#button to save commands to a commands file
saveCommandsButton = Button(window,text="Save Commands",padx=20,pady=5,command=saveCommands)
saveCommandsButton.place(in_=colorButton,relx=1.0,rely=0,x=50,y=-2)

#button to load commands into text field
loadCommandsButton = Button(window,text="Load Commands",padx=20,pady=5,command=loadCommands)
loadCommandsButton.place(in_=saveCommandsButton,relx=1.0,rely=0,x=5,y=-2)

#label that shows mouse position (after pressing button)
mousePosLabel = Label(window,text="mouse pos = ???")
mousePosLabel.config(bg="lightgray")
mousePosLabel.place(in_=window,relx=0.45,rely=0.9)

#label that shows color at position (after pressing button)
colorLabel = Label(window,text="color at pos = ???")
colorLabel.config(bg="lightgray")
colorLabel.place(in_=window,relx=0.45,rely=0.95)

#label to show available commands and proper syntax
textLabel = Label(window,text="Available commands:",font=("Arial",15))
textLabel.config(bg="lightgray")
textLabel.place(in_=textField,relx=1.0,rely=0,x=20)

availCommandsText = Label(window,text=infoTxt,font=("Arial",11))
availCommandsText.config(bg="lightgray")
availCommandsText.place(in_=textLabel,relx=0,rely=1.0,y=10)

window.configure(bg='lightgray')
window.mainloop()
