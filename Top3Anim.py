'''
Created on 12.06.2013

@author: Norine
'''

from libavg import *
 
def startAnim():
    animObj.start()
    
 
player = avg.Player.get()
canvas = player.createMainCanvas(size=(640,480))
rootNode = canvas.getRootNode()

ranking = avg.WordsNode (pos=(10,10), font="arial",
                         text="1. <br/> 2. <br/> 3. <br/> 4. <br/> 5.", 
                         color="ffffff", parent=rootNode)
div13 = avg.DivNode(pos=(0,0), size = (100, 100), elementoutlinecolor = "ffffff",  parent = rootNode)
(b,h)=div13.size
node1 = avg.WordsNode(pos=(25,10), font="arial", text="Titel 1", color ="ffffff", fontsize = 15, parent=div13)
node2 = avg.WordsNode(pos=(25,25), font="arial", text="Titel 2", color ="ffffff", fontsize = 15, parent=div13)
node3 = avg.WordsNode(pos=(25,40), font="arial", text="Titel 3", color ="ffffff", fontsize = 15, parent=div13)

node4 = avg.WordsNode(pos=(25,55), font="arial", text="Titel 4", color ="ffffff", fontsize = 15, parent=rootNode)
node5 = avg.WordsNode(pos=(25,70), font="arial", text="Titel 5", color ="ffffff", fontsize = 15, parent=rootNode)

animObj = ParallelAnim(
    [LinearAnim(node4, "opacity", 2000, 1, 0),
     LinearAnim(node5, "opacity", 2000, 1, 0),
     LinearAnim(ranking, "opacity", 2000, 1, 0),
     LinearAnim(div13, "size", 2000, (100, 100), (300, 300)),
     LinearAnim(node1, "fontsize", 2000, 15, 30),
     LinearAnim(node2, "fontsize", 2000, 15, 30),
     LinearAnim(node3, "fontsize", 2000, 15, 30),
     LinearAnim(node1, "pos", 2000, (25, 10), (25, 30)),
     LinearAnim(node2, "pos", 2000, (25, 25), (25, 300/4)),
     LinearAnim(node3, "pos", 2000, (25, 40), (25, 600/5))])

player.setTimeout(0, startAnim)


        
if __name__=='__main__':
    player.play()