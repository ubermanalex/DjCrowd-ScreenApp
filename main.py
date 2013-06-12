'''
Created on 06.06.2013

@author: Steffi
'''

from libavg import *
import time
import thread

class screen(AVGApp):
    def __init__(self, parentNode):
        
        player = avg.Player.get()   #player
        global a,b,z
        (a,b) = parentNode.size     #aufloesung
        canvas = player.createMainCanvas(size=(a,b)) #canvas kreieren
        self.rootNode = canvas.getRootNode()
        self.back = avg.RectNode (pos=(0,0), size=(a,b), parent=self.rootNode, color="A4A4A4", fillcolor="A4A4A4", fillopacity=1) 
        self.z = int (a-449)
        self.title=avg.WordsNode (font="arial", variant="Bold", text="DjCrowd - Canossa", color="000000", fontsize=40, alignment="left", parent=self.rootNode)
        print self.z
        self.timer=avg.WordsNode (font="arial", variant="Bold", text="Song-Countdown 30:00", color="000000", fontsize=40, indent=self.z, parent=self.rootNode)

        
        def left(): #links
            self.divNode=avg.DivNode(pos=(0,50), size=(3*(a/5),b-50),parent=self.rootNode)
            self.leftr=avg.RectNode (pos=(0,0), size=(3*(a/5), b-50), parent=self.divNode, color="F0F0F0", fillopacity=1)
            self.title=avg.WordsNode (pos=(100,0),font="arial", variant="Bold", text="Top 7 Songs", color="000000", fontsize=30, parent=self.divNode)
            self.votes=avg.WordsNode (pos=(600,0),font="arial", variant="Bold", text="Votes", color="000000", fontsize=30, parent=self.divNode)
            
            self.div1=avg.DivNode(pos=(70,110), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz1a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text="1. ", color="DDDC3C", fontsize=30, parent=self.div1)
            self.platz1b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text="1. ", color="DDDC3C", fontsize=20, parent=self.div1)
            self.platz1c=avg.WordsNode (pos=(563,0),font="arial", variant="Bold", text="1. ", color="DDDC3C", fontsize=30, parent=self.div1)
            
            self.div2=avg.DivNode(pos=(70,210), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz2a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text="2. ", color="C9C9C5", fontsize=30, parent=self.div2)
            self.platz2b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text="2. ", color="C9C9C5", fontsize=20, parent=self.div2)
            self.platz2c=avg.WordsNode (pos=(563,0),font="arial", variant="Bold", text="2. ", color="C9C9C5", fontsize=30, parent=self.div2)
            
            self.div3=avg.DivNode(pos=(70,310), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz3a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text="3. ", color="EFBF34", fontsize=30, parent=self.div3)
            self.platz3b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text="3. ", color="EFBF34", fontsize=20, parent=self.div3)
            self.platz3c=avg.WordsNode (pos=(563,0),font="arial", variant="Bold", text="3. ", color="EFBF34", fontsize=30, parent=self.div3)
            
            
            self.div4=avg.DivNode(pos=(70,410), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz4a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text="4. ", color="000000", fontsize=30, parent=self.div4)
            self.platz4b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text="4. ", color="000000", fontsize=20, parent=self.div4)
            self.platz4c=avg.WordsNode (pos=(563,0),font="arial", variant="Bold", text="4. ", color="000000", fontsize=30, parent=self.div4)
            
            self.div5=avg.DivNode(pos=(70,510), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz5a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text="5. ", color="000000", fontsize=30, parent=self.div5)
            self.platz5b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text="5. ", color="000000", fontsize=20, parent=self.div5)
            self.platz5c=avg.WordsNode (pos=(563,0),font="arial", variant="Bold", text="5. ", color="000000", fontsize=30, parent=self.div5)
            
            self.div6=avg.DivNode(pos=(70,610), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz6a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text="6. ", color="000000", fontsize=30, parent=self.div6)
            self.platz6b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text="6. ", color="000000", fontsize=20, parent=self.div6)
            self.platz6c=avg.WordsNode (pos=(563,0),font="arial", variant="Bold", text="6. ", color="000000", fontsize=30, parent=self.div6)
            
            self.div7=avg.DivNode(pos=(70,710), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz7a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text="7. ", color="000000", fontsize=30, parent=self.div7)
            self.platz7b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text="7. ", color="000000", fontsize=20, parent=self.div7)
            self.platz7c=avg.WordsNode (pos=(563,0),font="arial", variant="Bold", text="7. ", color="000000", fontsize=30, parent=self.div7)
            
            
        def right(): #rechts 
            self.divNode=avg.DivNode(pos=(a-2*(a/5),50), size=(2*(a/5),b-50),parent=self.rootNode)
            self.rightr=avg.RectNode (pos=(0,0), size=(2*(a/5), b-50), parent=self.divNode, color="F0F0F4", fillopacity=1)
            
            
        def receiveArraywithSongs():
            
            title=[]
            title.append("Silbermond##Nichts passiert##7")
            title.append("Juli##Gute Zeit##6")
            title.append("Nickelback##Silver side up##5")
            title.append("Carly Rae Jeapson##I just met you##4")
            title.append("Sportfreunde Stiller##Applaus Applaus##3")
            title.append("Will.I.am##Scream and Shout##2")
            title.append("Justin Timberlake##Mirrors##1")
            stringarray=[]

            ArrayLen = len(title)
            for i in range(0,ArrayLen):
                string = title[i]
                string2 = string.split("##")
                stringarray.append([string2[0],string2[1],string2[2]]) ##Interpret , Titel, Votes
            print stringarray[0][0]
            
            
            self.platz1a.text= stringarray[0][1]
            self.platz2a.text= stringarray[1][1]
            self.platz3a.text= stringarray[2][1]
            self.platz4a.text= stringarray[3][1]
            self.platz5a.text= stringarray[4][1]
            self.platz6a.text= stringarray[5][1]
            self.platz7a.text= stringarray[6][1]
            
            self.platz1b.text= stringarray[0][0]
            self.platz2b.text= stringarray[1][0]
            self.platz3b.text= stringarray[2][0]
            self.platz4b.text= stringarray[3][0]
            self.platz5b.text= stringarray[4][0]
            self.platz6b.text= stringarray[5][0]
            self.platz7b.text= stringarray[6][0]
            
            self.platz1c.text= stringarray[0][2]
            self.platz2c.text= stringarray[1][2]
            self.platz3c.text= stringarray[2][2]
            self.platz4c.text= stringarray[3][2]
            self.platz5c.text= stringarray[4][2]
            self.platz6c.text= stringarray[5][2]
            self.platz7c.text= stringarray[6][2]
            

            
            
            
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
        receiveArraywithSongs()
        
        
        
  
        
if __name__=='__main__':
    screen.start(resolution=(1440, 900))   
  

