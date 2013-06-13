'''
Created on 12.06.2013

@author: Kirstin
'''

from libavg import *
 
def startAnim():
    animObj.start()
    
 
player = avg.Player.get()
canvas = player.createMainCanvas(size=(640,480))
rootNode = canvas.getRootNode()
nodea = avg.WordsNode(pos=(10,10), font="arial",
        text="Hello World", parent=rootNode)
nodeb = avg.WordsNode(pos=(10,20), font="arial", text="Hello back", parent=rootNode)

animObj = ParallelAnim(
    [LinearAnim(nodea, "y", 2000, 10, 30),
     LinearAnim(nodeb, "y", 2000, 20, 10)])

player.setTimeout(0, startAnim)



player.play()