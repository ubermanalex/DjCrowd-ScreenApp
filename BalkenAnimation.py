'''
Created on 12.06.2013

@author: Kirstin
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
            self.leftr=avg.RectNode (pos=(25,0), size=(((a/2)-50), b-50), parent=self.divNode, color="F0F0F0", fillopacity=1)
            self.title=avg.WordsNode (pos=(100,0),font="arial", variant="Bold", text="Top 7 Songs", color="000000", fontsize=30, parent=self.divNode)
            self.votes=avg.WordsNode (pos=(350,0),font="arial", variant="Bold", text="Votes", color="000000", fontsize=30, parent=self.divNode)
            self.platz1=avg.WordsNode (pos=(70,80),font="arial", variant="Bold", text="1. ", color="DDDC3C", fontsize=30, parent=self.divNode)
            self.platz2=avg.WordsNode (pos=(70,120),font="arial", variant="Bold", text="2. ", color="C9C9C5", fontsize=30, parent=self.divNode)
            self.platz3=avg.WordsNode (pos=(70,160),font="arial", variant="Bold", text="3. ", color="EFBF34", fontsize=30, parent=self.divNode)
            self.platz4=avg.WordsNode (pos=(70,200),font="arial", variant="Bold", text="4. ", color="000000", fontsize=30, parent=self.divNode)
            self.platz5=avg.WordsNode (pos=(70,240),font="arial", variant="Bold", text="5. ", color="000000", fontsize=30, parent=self.divNode)
            self.platz6=avg.WordsNode (pos=(70,280),font="arial", variant="Bold", text="6. ", color="000000", fontsize=30, parent=self.divNode)
            self.platz7=avg.WordsNode (pos=(70,320),font="arial", variant="Bold", text="7. ", color="000000", fontsize=30, parent=self.divNode)
        
        def Tauschen(a,b,AX,AY,BX,BY):
                def startAnim():
                    animObj.start()
        
                animObj1 = LinearAnim(a, "y", 2000, AY, BY)
                animObj2 = LinearAnim(b, "y", 2000, BY, AY)
                animList = (animObj2, animObj1)
                animObj = ParallelAnim(animList)

                player.setTimeout(2000, startAnim)    
        
        def right():
            self.divNode=avg.DivNode(pos=(a/2,50), size=((a/2)-20,b-50),parent=self.rootNode)
            self.rightr=avg.RectNode (pos=(0,0), size=((a/2)-20, b-50), parent=self.divNode, color="F0F0F4", fillopacity=1)
            
            #On Start : 
            leute=[]
            leute.append(["Alexander", "0"])
            leute.append(["Pascal", "0"])
            leute.append(["Antonio", "0"])
            
            self.erster=avg.RectNode(pos=(50,b-200), size=(30,5), parent=self.divNode, color="0489B1", fillcolor="2E9AFE", fillopacity=1)
            self.zweiter=avg.RectNode(pos=(200,b-200), size=(30,5), parent=self.divNode, color="0489B1", fillcolor="2E9AFE", fillopacity=1)
            self.zweiter=avg.RectNode(pos=(350, b-200), size=(30,5), parent=self.divNode, color="0489B1", fillcolor="2E9AFE",fillopacity=1)
            
            self.ersterName=avg.WordsNode(pos=(50,b-140), text=" " ,parent=self.divNode, font='arial', color="6E6E6E", fontsize=20)
            self.ersterName.text=leute[0][0]
            
            self.zweiterName=avg.WordsNode(pos=(200,b-140), text=" " ,parent=self.divNode, font='arial', color="6E6E6E", fontsize=20)
            self.zweiterName.text=leute[1][0]
            
            self.dritterName=avg.WordsNode(pos=(350,b-140), text=" " ,parent=self.divNode, font='arial', color="6E6E6E", fontsize=20)
            self.dritterName.text=leute[2][0]
            
            
            #ON Message
            
            
            
            nodea = avg.WordsNode(pos=(10,10), font="arial",
                              text="Hello World", parent=self.divNode, color="6E6E6E", fontsize=20)
            nodeb = avg.WordsNode(pos=(10,30), font="arial", text="Hello back", parent=self.divNode, color="6E6E6E", fontsize=20)
            Tauschen(nodea, nodeb, 10, 10, 10, 30)
            
            print leute.index("Alexander")
           
            
           
            """if msg[0:4] == 'INIT':
                str1 = msg.split(" ")
                leute.append([str1[1],str1[2]])
                leute.append([str1[3],str1[4]])
                leute.append([str1[5],str1[6]])
                print leute            
                
            
            PunkteErster = leute[0][1]
            NameErster = leute[0][0]
            PunkteErster = float(PunkteErster)
            
            PunkteZweiter = leute[1][1]
            NameZweiter = leute[1][0]
            PunkteZweiter = float(PunkteZweiter)
            
            PunkteDritter = leute[2][1]
            NameDritter = leute[2][0]
            PunkteDritter = float(PunkteDritter)
            
            Hundertprozent = b-200
            Punktezweiter = (Hundertprozent/PunkteErster)*PunkteZweiter
            Punktedritter = (Hundertprozent/PunkteErster)*PunkteDritter
                
            
            self.erster=avg.RectNode(pos=(50,50), size=(30,Hundertprozent), parent=self.divNode, color="0489B1", fillcolor="2E9AFE", fillopacity=1)
            self.zweiter=avg.RectNode(pos=(200,50+(b-200)-Punktezweiter), size=(30,Punktezweiter), parent=self.divNode, color="0489B1", fillcolor="2E9AFE", fillopacity=1)
            self.zweiter=avg.RectNode(pos=(350,50+(b-200)-Punktedritter), size=(30,Punktedritter), parent=self.divNode, color="0489B1", fillcolor="2E9AFE",fillopacity=1)
            
            self.ersterName=avg.WordsNode(pos=(50,Hundertprozent+60), text=" " ,parent=self.divNode, font='arial', color="6E6E6E", fontsize=20)
            self.ersterName.text=NameErster
            
            self.zweiterName=avg.WordsNode(pos=(200,Hundertprozent+60), text=" " ,parent=self.divNode, font='arial', color="6E6E6E", fontsize=20)
            self.zweiterName.text=NameZweiter
            
            self.dritterName=avg.WordsNode(pos=(350,Hundertprozent+60), text=" " ,parent=self.divNode, font='arial', color="6E6E6E", fontsize=20)
            self.dritterName.text=NameDritter
            """
            
        def receiveArraywithSongs():
            
            title=[]
            title.append("Silbermond##Nichts passiert##7")
            title.append("Juli##Gute Zeit##6")
            title.append("Nickelback##Silver side up##5")
            title.append("Carly Rae Jeapson##I just met you##4")
            title.append("Sportfreunde Stiller##Applaus Applaus##3")
            title.append("Will.I.am##Scream&Shout##2")
            title.append("Justin Timberlake##Mirrors##1")
            stringarray=[]

            ArrayLen = len(title)
            for i in range(0,ArrayLen):
                string = title[i]
                string2 = string.split("##")
                stringarray.append([string2[0],string2[1],string2[2]]) ##Interpret , Titel, Votes
            print stringarray[0][0]
            
            
            self.platz1.text= "1. "+stringarray[0][0]
            self.platz2.text= "2. "+stringarray[1][0]
            self.platz3.text= "3. "+stringarray[2][0]
            self.platz4.text= "4. "+stringarray[3][0]
            self.platz5.text= "5. "+stringarray[4][0]
            self.platz6.text= "6. "+stringarray[5][0]
            self.platz7.text= "7. "+stringarray[6][0]
            

            
            
            
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
    screen.start(resolution=(1024, 640))   
  

