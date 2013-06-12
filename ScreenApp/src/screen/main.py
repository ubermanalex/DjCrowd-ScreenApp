'''
Created on 06.06.2013

@author: Steffi
'''

from libavg import *
import time
import thread

class screen(AVGApp):
    def __init__(self, parentNode):
        
        player = avg.Player.get()  
        global a,b,z
        (a,b) = parentNode.size
        canvas = player.createMainCanvas(size=(a,b)) #Aufloesung Bildschirm
        self.rootNode = canvas.getRootNode()
        self.back = avg.RectNode (pos=(0,0), size=(a,b), parent=self.rootNode, color="A4A4A4", fillcolor="A4A4A4", fillopacity=1) 
        self.z = int (a-449)
        self.title=avg.WordsNode (font="arial", variant="Bold", text="DjCrowd - Canossa", color="000000", fontsize=40, alignment="left", parent=self.rootNode)
        print self.z
        self.timer=avg.WordsNode (font="arial", variant="Bold", text="Song-Countdown 30:00", color="000000", fontsize=40, indent=self.z, parent=self.rootNode)

        
        def left():
            self.divNode=avg.DivNode(pos=(0,50), size=((a/2)-20,b-50),parent=self.rootNode)
            self.left=avg.RectNode (pos=(0,0), size=((a/2)-20, b-50), parent=self.divNode, color="F0F0F0", fillopacity=1)
            self.title=avg.WordsNode (font="arial", variant="Bold", text="Top 7 Songs", color="000000", fontsize=30, parent=self.divNode, alignment="center")
            
        def right():
            self.divNode=avg.DivNode(pos=(a/2,50), size=((a/2)-20,b-50),parent=self.rootNode)
            self.left=avg.RectNode (pos=(0,0), size=((a/2)-20, b-50), parent=self.divNode, color="F0F0F4", fillopacity=1)
            
        def countdown(m,s):
            
            def MsToSecs(m,s):
                return m*60 + s

            def secsToMs(secs):
                mins = secs//60
                secs -= mins*60
                mins = str(mins)
                secs = str(secs)
                return mins,secs
            
            seconds = MsToSecs(m,s)
            while seconds > 0:
                (mint,sect)=secsToMs(seconds)
                self.timer.text="Countdown " + mint + ":" + sect
                seconds -= 1
                time.sleep(1)
                if seconds ==0:
                    seconds = 1800
        
            
        left()
        right()
        thread.start_new_thread(countdown,(0,2))
        
        
        
  
        
if __name__=='__main__':
    screen.start(resolution=(1024, 768))   
  

