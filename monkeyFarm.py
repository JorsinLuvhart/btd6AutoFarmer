#############################################################
# Things to note:
# Resolution should be set to 1680x1050 (mostly cause I can see the console while testing)
# Use the default dart monkey icon, that is the default anchorpoint of the code
# Turn off HDR/AutoHDR, it fucks with the images and breaks them
#############################################################

import pydirectinput as pdi
import pyautogui as pag
import time
import asyncio

#############################################################
# Window Functions
#############################################################

def active_window():
    '''
    Make BloonsTD6 the active window
    '''
    print("Finding Bloons Window...")

    try:
        bloons_window = pag.getWindowsWithTitle("BloonsTD6")[0]
        print("Bloons Window Found...")
    except:
        print("Cannot Find Bloons Window... Program Terminating")
        exit(1)

    if bloons_window.isActive == False:
        pag.click("BloonsIcon.PNG")

    pag.click(bloons_window.box)

    print("Bloons Window Activation Successful")

def get_window_coordinates():
    bloons_window = pag.getWindowsWithTitle("BloonsTD6")[0]
    return bloons_window.box

#############################################################
# Async Function to catch level ups
#############################################################

async def levelups():
    if pag.locateOnScreen("Levelup.PNG", region=(x+600,y+825,200,200)):
        pag.click()
        time.sleep(0.3)
        pag.click()

#############################################################
# Monkey Functions
#############################################################

def play(x,y):
    while True:
        if pag.locateOnScreen("Play.PNG", region=(x+600,y+825,200,200)):
            pag.click("Play.PNG")
            print("Found play button")
            return
        if pag.locateOnScreen("Play2.PNG", region=(x+1475,y+800,200,200)):
            pag.click("Play2.PNG")
            print("Found play button")
            return
        
            
def collect(x,y):
    time.sleep(3)
    if pag.locateOnScreen("Collect.PNG", region=(x+550,y+550,600,300)):
        pag.click("Collect.PNG")
        time.sleep(4)
        pag.click(x=x+670,y=y+500)
        time.sleep(0.5)
        pag.click()
        time.sleep(0.5)
        pag.click(x=x+960,y=y+500)
        time.sleep(0.5)
        pag.click()
        time.sleep(0.5)
        pag.click()
        time.sleep(2)
        print("Box Collected")

def mapSelect(mapCtrl,window):
    mapIndex = 0
    pag.click("Expert.PNG")
    time.sleep(0.5)
    if not pag.locateOnScreen("Bonus2.PNG", region=window,confidence=0.95):
        pag.click()
        mapIndex += 6
        time.sleep(0.5)
    mapX, mapY = pag.center(pag.locateOnScreen("Bonus2.PNG",confidence=0.95))
    if mapY-mapCtrl.y > 400:
        mapIndex += 3
    if mapX-mapCtrl.x > 1200:
        mapIndex += 2
    elif mapX-mapCtrl.x > 800:
        mapIndex += 1
    pag.click(mapX, mapY)
    return mapIndex

class MapControl:
    def __init__(self, anchor):
        self.x = anchor.left
        self.y = anchor.top
    
    def startRound(self):
        pdi.press("space")
        print("Round Start")
        
    def waitForRound(self):
        while not pag.locateOnScreen("Start.PNG", region=(self.x+1530,self.y+875,150,150)):
            pass
        print("Round End")
            
    def skipRounds(self,rounds=1):
        for i in range(rounds):
            self.startRound()
            self.waitForRound()

    def lastRound(self):
        self.startRound()
        while not pag.locateOnScreen("Next.PNG", region=(self.x+700,self.y+800,250,125)):
            pass
        pag.click("Next.PNG")
        while not pag.locateOnScreen("Home.PNG", region=(self.x+475,self.y+725,150,180)):
            pass
        pag.click("Home.PNG")
        print("Map End")
        
    def upgrade(self,path):
        print(f"Upgrading path {path}")
        if path==1:
            pdi.press(",")
        elif path==2:
            pdi.press(".")
        else:
            pdi.press("/")
            
    def targeting(self,num):
        pdi.press("tab",presses=num)
        print("Changing Targeting")
        
    def setTarget(self,x,y):
        time.sleep(0.2)
        pag.click("SelectTargLoc.PNG")
        pag.click(x,y)
        print("Setting FlameWall Target")

monkeyDict = {
    "u": "Hero",
    "q": "Dart Monkey",
    "w": "Boomerang",
    "e": "Bomb Shooter",
    "r": "Tack Shooter",
    "t": "Ice",
    "y": "Glue",
    "z": "Sniper",
    "x": "Sub",
    "c": "Buccaneer",
    "v": "Ace",
    "b": "Heli",
    "n": "Mortar",
    "m": "Dartling",
    "a": "Wizard",
    "s": "Super",
    "d": "Ninja",
    "f": "Alchemist",
    "g": "Druid",
    "h": "Banana Farm",
    "l": "Engineer",
    "j": "Spike Factory",
    "k": "Village",
}

class Monkey:
    def __init__(self, hotkey, x, y):
        self.monkeyType = monkeyDict[hotkey]
        self.x = x
        self.y = y
        pdi.press(hotkey)
        time.sleep(0.1)
        self.selectMonkey()
        time.sleep(0.1)
        print(f"Bought a {self.monkeyType}")
        
    def __str__(self):
        return f"This is a {self.monkeyType} at x={self.x}, y={self.y}"
    
    def selectMonkey(self):
        pag.click(x=self.x,y=self.y)

def sanctuary(mapCtrl):
    monkeyList = []
    monkeyList.append(Monkey("u",mapCtrl.x+1100,mapCtrl.y+530))
    monkeyList.append(Monkey("q",mapCtrl.x+640,mapCtrl.y+283))
    monkeyList.append(Monkey("z",mapCtrl.x+1031,mapCtrl.y+814))
    mapCtrl.startRound()
    mapCtrl.skipRounds()#end of round 1
    monkeyList.append(Monkey("j",mapCtrl.x+838,mapCtrl.y+252))
    monkeyList[-1].selectMonkey()
    mapCtrl.upgrade(3)
    mapCtrl.skipRounds()#end of round 2
    mapCtrl.upgrade(3)
    mapCtrl.targeting(3)
    mapCtrl.skipRounds(rounds=2)#end of round 4
    mapCtrl.upgrade(1)
    monkeyList.append(Monkey("a",mapCtrl.x+190,mapCtrl.y+283))
    monkeyList[-1].selectMonkey()
    mapCtrl.skipRounds()#end of round 5
    mapCtrl.upgrade(2)
    mapCtrl.skipRounds()#end of round 6
    mapCtrl.upgrade(2)
    mapCtrl.skipRounds()#end of round 7
    mapCtrl.upgrade(1)
    monkeyList.append(Monkey("a",mapCtrl.x+1188,mapCtrl.y+345))
    monkeyList[-1].selectMonkey()
    mapCtrl.skipRounds()#end of round 8
    mapCtrl.upgrade(2)
    mapCtrl.skipRounds()#end of round 9
    mapCtrl.upgrade(2)
    mapCtrl.upgrade(1)
    mapCtrl.skipRounds(rounds=30)#end of round 39
    mapCtrl.lastRound()#last round

def ravine(mapCtrl):
    monkeyList = []
    monkeyList.append(Monkey("u",mapCtrl.x+853,mapCtrl.y+142))
    monkeyList.append(Monkey("q",mapCtrl.x+137,mapCtrl.y+472))
    monkeyList.append(Monkey("j",mapCtrl.x+615,mapCtrl.y+759))
    monkeyList[-1].selectMonkey()
    mapCtrl.startRound()
    mapCtrl.skipRounds()#end of round 1
    mapCtrl.upgrade(3)
    mapCtrl.upgrade(3)
    mapCtrl.targeting(3)
    mapCtrl.skipRounds()#end of round 2
    monkeyList.append(Monkey("g",mapCtrl.x+718,mapCtrl.y+906))
    monkeyList[-1].selectMonkey()
    mapCtrl.skipRounds()#end of round 3
    mapCtrl.upgrade(2)
    mapCtrl.upgrade(2)
    mapCtrl.skipRounds(rounds=2)#end of round 5
    mapCtrl.upgrade(2)
    mapCtrl.skipRounds()#end of round 6
    monkeyList.append(Monkey("g",mapCtrl.x+593,mapCtrl.y+131))
    monkeyList[-1].selectMonkey()
    mapCtrl.upgrade(2)
    mapCtrl.upgrade(2)
    mapCtrl.skipRounds()#end of round 7
    mapCtrl.upgrade(1)
    mapCtrl.skipRounds()#end of round 8
    mapCtrl.upgrade(2)
    mapCtrl.skipRounds(rounds=31)#end of round 39
    mapCtrl.lastRound()#last round
    
def floodedValley(mapCtrl):
    monkeyList = []
    monkeyList.append(Monkey("u",mapCtrl.x+164,mapCtrl.y+717))
    monkeyList.append(Monkey("x",mapCtrl.x+840,mapCtrl.y+715))
    monkeyList[-1].selectMonkey()
    mapCtrl.targeting(3)
    mapCtrl.upgrade(3)
    mapCtrl.startRound()
    mapCtrl.skipRounds()#end of round 1
    mapCtrl.upgrade(2)
    mapCtrl.skipRounds()#end of round 2
    mapCtrl.upgrade(2)
    mapCtrl.skipRounds(rounds=2)#end of round 4
    mapCtrl.upgrade(3)
    mapCtrl.skipRounds()#end of round 5
    mapCtrl.upgrade(3)
    mapCtrl.skipRounds()#end of round 6
    monkeyList.append(Monkey("x",mapCtrl.x+881,mapCtrl.y+645))
    mapCtrl.skipRounds(rounds=33)#end of round 39
    mapCtrl.lastRound()#last round

def infernal(mapCtrl):
    monkeyList = []
    monkeyList.append(Monkey("u",mapCtrl.x+695,mapCtrl.y+326))
    monkeyList.append(Monkey("q",mapCtrl.x+697,mapCtrl.y+648))
    monkeyList[-1].selectMonkey()
    mapCtrl.upgrade(3)
    mapCtrl.upgrade(3)
    mapCtrl.upgrade(3)
    mapCtrl.startRound()
    mapCtrl.skipRounds()#end of round 1
    mapCtrl.upgrade(2)
    mapCtrl.upgrade(2)
    mapCtrl.skipRounds()#end of round 2
    monkeyList.append(Monkey("g",mapCtrl.x+700,mapCtrl.y+735))
    monkeyList[-1].selectMonkey()
    mapCtrl.upgrade(2)
    mapCtrl.skipRounds()#end of round 3
    mapCtrl.upgrade(2)
    mapCtrl.skipRounds(rounds=2)#end of round 5
    mapCtrl.upgrade(2)
    mapCtrl.upgrade(1)
    mapCtrl.skipRounds(rounds=34)#end of round 39
    mapCtrl.lastRound()#last round
    
def bloodyPuddles(mapCtrl):
    monkeyList = []
    monkeyList.append(Monkey("u",mapCtrl.x+693,mapCtrl.y+401))
    monkeyList.append(Monkey("q",mapCtrl.x+240,mapCtrl.y+178))
    monkeyList[-1].selectMonkey()
    mapCtrl.upgrade(3)
    mapCtrl.upgrade(3)
    monkeyList.append(Monkey("x",mapCtrl.x+963,mapCtrl.y+143))
    monkeyList[-1].selectMonkey()
    mapCtrl.upgrade(1)
    mapCtrl.startRound()
    mapCtrl.skipRounds()#end of round 1
    mapCtrl.upgrade(1)
    mapCtrl.skipRounds()#end of round 2
    mapCtrl.upgrade(3)
    mapCtrl.skipRounds(rounds=2)#end of round 4
    mapCtrl.upgrade(3)
    mapCtrl.skipRounds(rounds=2)#end of round 6
    mapCtrl.upgrade(3)
    monkeyList.append(Monkey("g",mapCtrl.x+589,mapCtrl.y+338))
    monkeyList[-1].selectMonkey()
    mapCtrl.skipRounds()#end of round 7
    mapCtrl.upgrade(2)
    mapCtrl.upgrade(2)
    mapCtrl.skipRounds(rounds=2)#end of round 9
    mapCtrl.upgrade(2)
    mapCtrl.upgrade(1)
    mapCtrl.skipRounds(rounds=30)#end of round 39
    mapCtrl.lastRound()#last round

def workshop(mapCtrl):
    monkeyList = []
    monkeyList.append(Monkey("u",mapCtrl.x+1015,mapCtrl.y+236))
    monkeyList.append(Monkey("q",mapCtrl.x+866,mapCtrl.y+477))
    monkeyList.append(Monkey("a",mapCtrl.x+438,mapCtrl.y+474))
    monkeyList[-1].selectMonkey()
    mapCtrl.targeting(3)
    mapCtrl.upgrade(2)
    mapCtrl.startRound()
    mapCtrl.skipRounds(rounds=2)#end of round 2
    mapCtrl.upgrade(2)
    mapCtrl.upgrade(1)
    mapCtrl.skipRounds(rounds=2)#end of round 4
    monkeyList.append(Monkey("j",mapCtrl.x+1385,mapCtrl.y+591))
    monkeyList[-1].selectMonkey()
    mapCtrl.upgrade(3)
    mapCtrl.skipRounds()#end of round 5
    mapCtrl.upgrade(3)
    mapCtrl.targeting(1)
    mapCtrl.skipRounds()#end of round 6
    mapCtrl.upgrade(1)
    mapCtrl.skipRounds(rounds=2)#end of round 8
    monkeyList.append(Monkey("j",mapCtrl.x+1307,mapCtrl.y+591))
    monkeyList[-1].selectMonkey()
    mapCtrl.upgrade(3)
    mapCtrl.skipRounds()#end of round 9
    mapCtrl.upgrade(3)
    mapCtrl.targeting(1)
    mapCtrl.skipRounds()#end of round 10
    mapCtrl.upgrade(1)
    mapCtrl.skipRounds(rounds=29)#end of round 39
    mapCtrl.lastRound()#last round
    
def quad(mapCtrl):
    monkeyList = []
    monkeyList.append(Monkey("u",mapCtrl.x+836,mapCtrl.y+452))
    monkeyList.append(Monkey("q",mapCtrl.x+641,mapCtrl.y+797))
    monkeyList[-1].selectMonkey()
    mapCtrl.targeting(3)
    monkeyList.append(Monkey("z",mapCtrl.x+882,mapCtrl.y+538))
    monkeyList[-1].selectMonkey()
    mapCtrl.targeting(3)
    monkeyList.append(Monkey("a",mapCtrl.x+303,mapCtrl.y+530))
    monkeyList[-1].selectMonkey()
    mapCtrl.targeting(3)
    mapCtrl.upgrade(2)
    mapCtrl.startRound()
    mapCtrl.skipRounds(rounds=2)#end of round 2
    mapCtrl.upgrade(2)
    mapCtrl.skipRounds()#end of round 3
    mapCtrl.upgrade(1)
    mapCtrl.setTarget(mapCtrl.x+132,mapCtrl.y+522)
    monkeyList.append(Monkey("a",mapCtrl.x+731,mapCtrl.y+258))
    monkeyList[-1].selectMonkey()
    mapCtrl.targeting(3)
    mapCtrl.skipRounds()#end of round 4
    mapCtrl.upgrade(2)
    mapCtrl.skipRounds(rounds=2)#end of round 6
    mapCtrl.upgrade(2)
    mapCtrl.upgrade(1)
    mapCtrl.setTarget(mapCtrl.x+704,mapCtrl.y+110)
    mapCtrl.skipRounds()#end of round 7
    monkeyList.append(Monkey("j",mapCtrl.x+658,mapCtrl.y+260))
    monkeyList[-1].selectMonkey()
    mapCtrl.upgrade(3)
    mapCtrl.skipRounds()#end of round 8
    mapCtrl.upgrade(3)
    mapCtrl.targeting(3)
    mapCtrl.skipRounds(rounds=31)
    mapCtrl.lastRound()#last round
    
def darkCastle(mapCtrl): #with double cash/easy
    monkeyList = []
    monkeyList.append(Monkey("u",mapCtrl.x+700,mapCtrl.y+200))
    monkeyList.append(Monkey("q",mapCtrl.x+479,mapCtrl.y+469))
    mapCtrl.startRound()
    mapCtrl.skipRounds()#end of round 1
    monkeyList.append(Monkey("j",mapCtrl.x+1312,mapCtrl.y+525))
    monkeyList[-1].selectMonkey()
    mapCtrl.skipRounds()#end of round 2
    mapCtrl.upgrade(2)
    mapCtrl.upgrade(3)
    mapCtrl.skipRounds()#end of round 3
    mapCtrl.upgrade(3)
    mapCtrl.skipRounds()#end of round 4
    mapCtrl.upgrade(2)
    mapCtrl.skipRounds()#end of round 5
    monkeyList.append(Monkey("a",mapCtrl.x+868,mapCtrl.y+424))
    monkeyList[-1].selectMonkey()
    mapCtrl.targeting(3)
    mapCtrl.upgrade(1)
    mapCtrl.skipRounds()#end of round 6
    mapCtrl.upgrade(2)
    mapCtrl.skipRounds()#end of round 7
    mapCtrl.upgrade(1)
    mapCtrl.skipRounds()#end of round 8
    mapCtrl.upgrade(2)
    mapCtrl.skipRounds(rounds=2)#end of round 10
    mapCtrl.upgrade(1)
    mapCtrl.skipRounds(rounds=29)
    mapCtrl.lastRound()#last round
    
def muddyPuddles(mapCtrl):
    monkeyList = []
    monkeyList.append(Monkey("u",mapCtrl.x+553,mapCtrl.y+428))
    monkeyList.append(Monkey("q",mapCtrl.x+296,mapCtrl.y+186))
    monkeyList[-1].selectMonkey()
    mapCtrl.upgrade(3)
    mapCtrl.upgrade(3)
    monkeyList.append(Monkey("x",mapCtrl.x+1020,mapCtrl.y+444))
    monkeyList[-1].selectMonkey()
    mapCtrl.upgrade(1)
    mapCtrl.startRound()
    mapCtrl.skipRounds()#end of round 1
    mapCtrl.upgrade(1)
    mapCtrl.skipRounds()#end of round 2
    mapCtrl.upgrade(3)
    mapCtrl.skipRounds(rounds=2)#end of round 4
    mapCtrl.upgrade(3)
    monkeyList.append(Monkey("g",mapCtrl.x+933,mapCtrl.y+187))
    monkeyList[-1].selectMonkey()
    mapCtrl.skipRounds()#end of round 5
    mapCtrl.upgrade(2)
    mapCtrl.upgrade(2)
    mapCtrl.skipRounds(rounds=2)#end of round 7
    mapCtrl.upgrade(2)
    mapCtrl.upgrade(1)
    mapCtrl.skipRounds(rounds=32)#end of round 39
    mapCtrl.lastRound()#last round

def ouch(mapCtrl):
    monkeyList = []
    monkeyList.append(Monkey("u",mapCtrl.x+970,mapCtrl.y+310))
    monkeyList.append(Monkey("q",mapCtrl.x+450,mapCtrl.y+319))
    monkeyList.append(Monkey("c",mapCtrl.x+706,mapCtrl.y+528))
    monkeyList[-1].selectMonkey()
    mapCtrl.upgrade(2)
    mapCtrl.startRound()
    mapCtrl.skipRounds()#end of round 1
    mapCtrl.upgrade(2)
    mapCtrl.skipRounds()#end of round 2
    mapCtrl.upgrade(1)
    mapCtrl.skipRounds()#end of round 3
    mapCtrl.upgrade(1)
    mapCtrl.skipRounds(rounds=5)#end of round 8
    mapCtrl.upgrade(1)
    mapCtrl.skipRounds(rounds=31)#end of round 39
    mapCtrl.lastRound()#last round
    
expertMapIndexDict = {
    0: "Sanctuary",
    1: "Ravine",
    2: "Flooded Valley",
    3: "Infernal",
    4: "Bloody Puddles",
    5: "Workshop",
    6: "Quad",
    7: "Dark Castle",
    8: "Muddy Puddles",
    9: "#Ouch",
}

expertMapDict = {
    0: sanctuary,
    1: ravine,
    2: floodedValley,
    3: infernal,
    4: bloodyPuddles,
    5: workshop,
    6: quad,
    7: darkCastle,
    8: muddyPuddles,
    9: ouch,
}

#############################################################
# Misc Functions
#############################################################

def rand():
	return random.random()

#############################################################
# end of functions

#############################################################

if __name__ == '__main__':
    active_window() # Activates Bloons window
    bloons_window_box = get_window_coordinates()
    debug = False

    if not debug: #main loop
        mapCtrl = MapControl(pag.locateOnScreen("Anchor.PNG", region=bloons_window_box))
        while True: 
            # Main Menu
            play(mapCtrl.x,mapCtrl.y)
            time.sleep(0.5)
            mapIndex = mapSelect(mapCtrl,bloons_window_box)
            print(expertMapIndexDict[mapIndex])
            time.sleep(0.5)
            pag.click("Easy.PNG")
            time.sleep(0.5)
            pag.click("Standard.PNG")
            mapCtrl.waitForRound()
            # In Game
            time.sleep(0.3)
            expertMapDict[mapIndex](mapCtrl)
            collect(mapCtrl.x,mapCtrl.y)
            
    #debug mode
    mapCtrl = MapControl(pag.locateOnScreen("Anchor.PNG", region=bloons_window_box))
    while True:
        x,y=pag.position()
        #print(pag.locateOnScreen("Anchor.PNG", region=bloons_window_box))
        #print(f"x={x}, y=,{y}")
        print(f"x={x-mapCtrl.x}, y=,{y-mapCtrl.y}")