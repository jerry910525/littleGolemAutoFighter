import pyautogui
import win32gui
import win32com.client
import time
from os import listdir
from os.path import isfile, join
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
import re
from datetime import datetime
import subprocess
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
from time import sleep
from selenium import webdriver
from pyvirtualdisplay.smartdisplay import SmartDisplay
import requests
pyautogui.FAILSAFE = False
options = webdriver.ChromeOptions()
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])

# little golem information
username = "abc"
userpwd = "def"


# to transform move denotation from little golem to CGI deonations(ex: A1 -> aa)
def transform_string(input_code):
    if(input_code=="X"):
        return input_code
    first_letter = input_code[0].lower()
    digit_to_letter = {
        '1': 'a',
        '2': 'b',
        '3': 'c',
        '4': 'd',
        '5': 'e',
        '6': 'f',
        '7': 'g',
        '8': 'h',
        '9': 'i',
        '10': 'j',
        '11': 'k',
        '12': 'l',
        '13': 'm'
    }
    converted_code = first_letter + digit_to_letter.get(input_code[1:]) 
    return converted_code

# the primary object
class autoLG:
    # variables
    current_match  = None
    size =13
    shell = None
    moba = None
    lg = None
    input = None
    regex = r"=\S*., \S*, \S*" #change this for different game.
    chrome = None

    #open local files to extract move from terminal output
    def getMove(self):
        with open("./moba/temp.txt", 'r') as f1:
            mes = f1.read()
            mes = mes.split("Number of Tree Node:")[-1]
            if re.search(self.regex,mes):
                match  = re.search(self.regex,mes)
                # print(match.group(0))
                mes = match.group(0)
                mes = mes[1:].split(",")
                print(mes)
                return mes
            else:
                print("test")
            
    def sendMove(self):
        s = self.chrome.find_element(By.NAME, "submit").click()

    # sending result from little golem to CGI server and save it as an file.
    def uploadByEcho(self,content):
        self.SetAsForegroundWindow(self.moba)
        self.writeInMoba("echo \""+content+"\">temp.sgf\n")
    

    def activate(self):
        print("__________start running______________")
        while 1:
            self.chrome = webdriver.Chrome()
            self.lg = win32gui.FindWindowEx(None, None, None, "Little Golem - Google Chrome")            
            self.trackLG()
            self.chrome.close()
            print("end of the turn")
            time.sleep(5)
    
    def winEnumHandler( self, hwnd, ctx ):
        if win32gui.IsWindowVisible( hwnd ):
            pass

    # function that make things easier
    def writeInMoba(self,s):
        self.SetAsForegroundWindow(self.moba)
        pyautogui.write(s+"\n")
        # time.sleep(10)

    # enhanced "SetForegroundWindow" that put your cursor at the center of your screen
    def SetAsForegroundWindow(self,w):
        self.shell.SendKeys('%')
        win32gui.SetForegroundWindow(w)
        time.sleep(0.5)
        pyautogui.moveTo(pyautogui.size()[0]/2, pyautogui.size()[1]/2) 
        pyautogui.click() 

    # send moves with html
    def clickByElement(self,pos):
        self.chrome.get("https://www.littlegolem.net/jsp/game/game.jsp?gid="+self.current_match+"&move="+pos)
        time.sleep(1)
    
    # interpret input from server and sent the corresponding moves to little golem server     
    def playMove(self,input):
        h = []
        self.SetAsForegroundWindow(self.lg)
        for i in range(len(input)):
            input[i] = input[i].strip()
            h.append(transform_string(input[i].strip()))
        print(h)
        self.SetAsForegroundWindow(self.lg)
        if input[0] == "X":
            self.clickByElement(h[2])
        else:
            self.clickByElement(h[0]+h[1]+h[2])
        time.sleep(1)
    
    # enhanced "locateOnScreen" (change "c" if it could not locate the possition correctly)
    def getLocationByPNG(self,image,c = 0.9):
        a = pyautogui.center(pyautogui.locateOnScreen('./images/'+image,confidence=c))
        return None if a ==0 else a
    
    #save terminal outputs from mobaXterm
    def saveNewest(self):   
        self.SetAsForegroundWindow(self.moba)
        pyautogui.moveTo(self.getLocationByPNG("tab.png",c = 0.5))
        pyautogui.rightClick()
        x, y = pyautogui.position()
        pyautogui.moveTo(x+20, y + 190) #change this magic number if you are using different resolution
        pyautogui.leftClick()
        pyautogui.write("temp.txt")
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(5)

    # create webdriver and locate the position of MobaXterm window.
    def __init__(self):
        win32gui.EnumWindows( self.winEnumHandler, None )
        self.shell = win32com.client.Dispatch("WScript.Shell")
        self.moba = win32gui.FindWindowEx(None, None, None, "MobaXterm")
        if self.moba==None:
            raise ValueError("could not find MobaXterm window!")
            
        self.chrome = webdriver.Chrome()
        self.lg = win32gui.FindWindowEx(None, None, None, "Little Golem - Google Chrome")
        self.SetAsForegroundWindow(self.moba)

    # the main code that keep looping to track if there's new game to be played
    def trackLG(self):
        self.chrome.get("https://www.littlegolem.net/jsp/game/index.jsp")
        self.chrome.maximize_window()
        self.lg = win32gui.FindWindowEx(None, None, None, "Little Golem - Google Chrome")
        time.sleep(5)
        email = self.chrome.find_element(By.NAME, "login")
        password = self.chrome.find_element(By.NAME, "password")
        email.send_keys(username)
        password.send_keys(userpwd)
        self.SetAsForegroundWindow(self.lg)
        password.submit()
        time.sleep(3)
        self.chrome.get("https://www.littlegolem.net/jsp/game/index.jsp")
        time.sleep(10)
        # using HTML to find games to be played
        body = self.chrome.find_element(By.CLASS_NAME, "portlet-body")
        html = body.get_attribute("innerHTML")
        matches = re.findall(r'\?gid=\d+', html)
        for i in range(len(matches)):
            matches[i] = matches[i].split("=")[1]
        print("matches in queue:")
        print(matches)
        # play them one by one
        for match in matches:
            self.current_match = match
            self.chrome.get("https://www.littlegolem.net/servlet/sgf/"+match+"/game"+match+".txt")
            url = "https://www.littlegolem.net/servlet/sgf/"+match+"/game"+match+".txt"
            response = requests.get(url)
            if response.status_code == 200:
                content = response.text
                pattern = r'\[(\d+)\]'
                match1 = re.search(pattern, content)
                if match1:
                    size = int(match1.group(0)[1:len(match1.group(0))-1])  
                    print("size:",size) #print board size
                self.size = size
                content = content.replace("W[swap]", "")
                content = content.replace("B[swap]", "")
                self.SetAsForegroundWindow(self.moba)
                self.writeInMoba("\n")
                time.sleep(3)
                print("game:",content)
                self.writeInMoba("reset\n")
                time.sleep(1)
                self.writeInMoba("load "+content)
                time.sleep(5)
                self.writeInMoba("gen\n")
                time.sleep(20)
                self.saveNewest()
                move = self.getMove()
                self.playMove(move)
                self.sendMove()
            time.sleep(1)

if __name__=="__main__":
    auto = autoLG()
    auto.activate()