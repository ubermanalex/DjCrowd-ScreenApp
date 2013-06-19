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
        self.timer=avg.WordsNode (font="arial", variant="Bold", text="Song-Countdown 30:00", color="000000", fontsize=40, indent=self.z, parent=self.rootNode)
        
        def left(): #links Songs Votes usw
            self.divNode=avg.DivNode(pos=(0,50), size=(3*(a/5),b-50),parent=self.rootNode)
            self.ranking=avg.WordsNode (pos=(45,110),font="arial", variant="Bold", width=40, height= (b-50),text="1. <br/> <br/> <br/> 2. <br/> <br/> <br/> 3. <br/> <br/> <br/> 4. <br/> <br/> <br/> 5. <br/> <br/> <br/> 6. <br/> <br/> <br/> 7.", color="000000", fontsize=30, parent=self.rootNode)
            self.leftr=avg.RectNode (pos=(0,0), size=(3*(a/5), b-50), parent=self.divNode, color="F0F0F0", fillopacity=1)
            self.title=avg.WordsNode (pos=(75,0),font="arial", variant="Bold", text=" Top 7 Songs ", color="000000", fontsize=40, parent=self.divNode)
            self.votes=avg.WordsNode (pos=(600,0),font="arial", variant="Bold", text="Votes", color="000000", fontsize=40, parent=self.divNode)
            
            self.div1=avg.DivNode(pos=(75,110), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz1a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text="1. ", color="DDDC3C", fontsize=30, parent=self.div1)
            self.platz1b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text="1. ", color="DDDC3C", fontsize=20, parent=self.div1)
            self.platz1c=avg.WordsNode (pos=(561,0),font="arial", variant="Bold", text="1. ", color="DDDC3C", fontsize=30, parent=self.div1)
            
            
            self.div2=avg.DivNode(pos=(75,215), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz2a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text="2. ", color="C9C9C5", fontsize=30, parent=self.div2)
            self.platz2b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text="2. ", color="C9C9C5", fontsize=20, parent=self.div2)
            self.platz2c=avg.WordsNode (pos=(561,0),font="arial", variant="Bold", text="2. ", color="C9C9C5", fontsize=30, parent=self.div2)
            
            self.div3=avg.DivNode(pos=(75,320), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz3a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text="3. ", color="EFBF34", fontsize=30, parent=self.div3)
            self.platz3b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text="3. ", color="EFBF34", fontsize=20, parent=self.div3)
            self.platz3c=avg.WordsNode (pos=(561,0),font="arial", variant="Bold", text="3. ", color="EFBF34", fontsize=30, parent=self.div3)
            
            
            self.div4=avg.DivNode(pos=(75,426), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz4a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text="4. ", color="000000", fontsize=30, parent=self.div4)
            self.platz4b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text="4. ", color="000000", fontsize=20, parent=self.div4)
            self.platz4c=avg.WordsNode (pos=(561,0),font="arial", variant="Bold", text="4. ", color="000000", fontsize=30, parent=self.div4)
            
            self.div5=avg.DivNode(pos=(75,530), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz5a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text="5. ", color="000000", fontsize=30, parent=self.div5)
            self.platz5b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text="5. ", color="000000", fontsize=20, parent=self.div5)
            self.platz5c=avg.WordsNode (pos=(561,0),font="arial", variant="Bold", text="5. ", color="000000", fontsize=30, parent=self.div5)
            
            self.div6=avg.DivNode(pos=(75,636), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz6a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text="6. ", color="000000", fontsize=30, parent=self.div6)
            self.platz6b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text="6. ", color="000000", fontsize=20, parent=self.div6)
            self.platz6c=avg.WordsNode (pos=(561,0),font="arial", variant="Bold", text="6. ", color="000000", fontsize=30, parent=self.div6)
            
            self.div7=avg.DivNode(pos=(75,740), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz7a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text="7. ", color="000000", fontsize=30, parent=self.div7)
            self.platz7b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text="7. ", color="000000", fontsize=20, parent=self.div7)
            self.platz7c=avg.WordsNode (pos=(561,0),font="arial", variant="Bold", text="7. ", color="000000", fontsize=30, parent=self.div7)
            
        
        def Tauschen(a,b,AX,AY,BX,BY):
                def startAnim():
                    animObj.start()
        
                animObj1 = LinearAnim(a, "y", 2000, AY, BY)
                animObj2 = LinearAnim(b, "y", 2000, BY, AY)
                animList = (animObj2, animObj1)
                animObj = ParallelAnim(animList)

                player.setTimeout(2000, startAnim) 
        
        def TauschenDIV(a,b,AX,BX):
                def startAnim():
                    animObj.start()
        
                animObj1 = LinearAnim(a, "x", 2000, AX, BX)
                animObj2 = LinearAnim(b, "x", 2000, BX, AX)
                animList = (animObj2, animObj1)
                animObj = ParallelAnim(animList)

                player.setTimeout(0, startAnim) 
        
        def Suchen(array, name):
                i = 0
                while i<2 :
                    if array[i][0] == name:
                        return i
                    
                
                    i += 1
                return -1
            
        def TauschenimArray(array, Position1, Position2):
            name1 = array[Position1][0]
            punkte1 = array[Position1][1]
            array[Position1][0] = array[Position2][0]
            array[Position1][1] = array[Position2][1]
            array[Position2][0] = name1
            array[Position2][1] = punkte1
            
        def SetzenimArray(array, name, punkte):
            array[2][0] = name
            array[2][1] = punkte     
            
            
        def right(): #rechts mit Balken
            self.divNode=avg.DivNode(pos=(a-2*(a/5),50), size=(2*(a/5),b-50),parent=self.rootNode)
            self.rightr=avg.RectNode (pos=(0,0), size=(2*(a/5), b-50), parent=self.divNode, color="F0F0F4", fillopacity=1)
            
            breite = 2*(a/5)
            #On Start : 
            self.leute=[]
            self.leute.append(["Alexander", "0"])
            self.leute.append(["Pascal", "0"])
            self.leute.append(["Antonio", "0"])
            
            self.divNode1=avg.DivNode(pos=(0,0), size=((breite/3),b-50),parent=self.divNode)
            self.erster=avg.RectNode(pos=(50,b-155), size=(30,5), parent=self.divNode1, color="0489B1", fillcolor="2E9AFE", fillopacity=1)
            self.ersterName=avg.WordsNode(pos=(50,b-100), text=" " ,parent=self.divNode1, font='arial', color="6E6E6E", fontsize=20)
            self.ersterName.text=self.leute[0][0]
            
            self.divNode2=avg.DivNode(pos=((breite/3),0), size=((breite/3),b-50),parent=self.divNode)
            self.zweiter=avg.RectNode(pos=(50,b-155), size=(30,5), parent=self.divNode2, color="0489B1", fillcolor="2E9AFE", fillopacity=1)
            self.zweiterName=avg.WordsNode(pos=(50,b-100), text=" " ,parent=self.divNode2, font='arial', color="6E6E6E", fontsize=20)
            self.zweiterName.text=self.leute[1][0]
            
            self.divNode3=avg.DivNode(pos=((breite-(breite/3)),0), size=((breite/3),b-50),parent=self.divNode)
            self.dritter=avg.RectNode(pos=(50, b-155), size=(30,5), parent=self.divNode3, color="0489B1", fillcolor="2E9AFE",fillopacity=1)      
            self.dritterName=avg.WordsNode(pos=(50,b-100), text=" " ,parent=self.divNode3, font='arial', color="6E6E6E", fontsize=20)
            self.dritterName.text=self.leute[2][0]
            
        def recievedpunkte(string,null):
            
            array = string.split("###")
                         
            neueLeute = []
            neueLeute.append([array[1], array[2]])
            neueLeute.append([array[3], array[4]])
            neueLeute.append([array[5], array[6]])
            
            
            PunkteErster = neueLeute[0][1]
            NameErster = neueLeute[0][0]
            PunkteErster = float(PunkteErster)
            
            PunkteZweiter = neueLeute[1][1]
            NameZweiter = neueLeute[1][0]
            PunkteZweiter = float(PunkteZweiter)
            
            PunkteDritter = neueLeute[2][1]
            NameDritter = neueLeute[2][0]
            PunkteDritter = float(PunkteDritter)
            
            Hundertprozent = b-200
            Punktezweiter = (Hundertprozent/PunkteErster)*PunkteZweiter
            Punktedritter = (Hundertprozent/PunkteErster)*PunkteDritter
            
            breite = 2*(a/5)
            
            
            #Erster der neuen Liste nicht in alter Liste
            if Suchen(self.leute, neueLeute[0][0])== -1 :
                self.dritter.pos=(50,50)
                self.dritter.size=(30, Hundertprozent)
                self.dritterName.text=NameErster
                
                TauschenDIV(self.divNode2, self.divNode3, breite/3, breite-(breite/3))        
                time.sleep(5)     
                TauschenDIV(self.divNode3, self.divNode1, breite/3, 0)
                
                time.sleep(5)
                
                SetzenimArray(self.leute, neueLeute[0][0], neueLeute[0][1])
                TauschenimArray(self.leute, 1, 2)                
                TauschenimArray(self.leute, 0, 1)
                
                self.divNode1.pos = (0,0) 
                self.erster.pos=(50,50) 
                self.erster.size=(30,Hundertprozent)
                self.ersterName.text=self.leute[0][0]
            
                self.divNode2.pos = (breite/3, 0)
                self.zweiter.pos=(50,b-155)
                self.zweiter.size=(30,5)
                self.zweiterName.text=self.leute[1][0]
            
                self.divNode3.pos = (breite-(breite/3),0)
                self.dritter.pos=(50,b-155)      
                self.dritter.size=(30,5)
                self.dritterName.text=self.leute[2][0]
                
            #Erster schon in der Liste 
            else :
                i = Suchen(self.leute, neueLeute[0][0])
                if i == 2:
                    self.dritter.pos=(50,50)
                    self.dritter.size=(30,Hundertprozent)
                    TauschenDIV(self.divNode2, self.divNode3, breite/3, breite-(breite/3))     
                    time.sleep(5)           
                    TauschenDIV(self.divNode3, self.divNode1, breite/3, 0)
                    self.leute[2][1] = neueLeute[2][1]
                    TauschenimArray(self.leute, 1, 2)                
                    TauschenimArray(self.leute, 0, 1)
                    
                    time.sleep(5)
                    
                    self.divNode1.pos = (0,0) 
                    self.erster.pos=(50,50) 
                    self.erster.size=(30,Hundertprozent)
                    self.ersterName.text=self.leute[0][0]
            
                    self.divNode2.pos = (breite/3, 0)
                    self.zweiter.pos=(50,b-155)
                    self.zweiter.size=(30,5)
                    self.zweiterName.text=self.leute[1][0]
            
                    self.divNode3.pos = (breite-(breite/3),0)
                    self.dritter.pos=(50,b-155)      
                    self.dritter.size=(30,5)
                    self.dritterName.text=self.leute[2][0]
                    
                    
                elif i ==1:
                    self.zweiter.pos=(50,50)
                    self.zweiter.size=(30,Hundertprozent)
                    TauschenDIV(self.divNode2, self.divNode1, breite/3, 0)
                    self.leute[1][1] = neueLeute[1][1]
                    TauschenimArray(self.leute, 0, 1)
                    
                    time.sleep(5)
                    
                    self.divNode1.pos = (0,0) 
                    self.erster.pos=(50,50) 
                    self.erster.size=(30,Hundertprozent)
                    self.ersterName.text=self.leute[0][0]
            
                    self.divNode2.pos = (breite/3, 0)
                    self.zweiter.pos=(50,b-155)
                    self.zweiter.size=(30,5)
                    self.zweiterName.text=self.leute[1][0]
                    
                    
                else :
                    self.erster.pos=(50,50)
                    self.erster.size=(30,Hundertprozent)
                    self.leute[0][1] = neueLeute[0][1]
                    
                    
            time.sleep(2)
            
            #Zwite Person noch nicht in der Liste
            if Suchen(self.leute, neueLeute[1][0])== -1 :
                
                self.dritter.pos= (50,50+(b-200)-Punktezweiter)
                self.dritter.size=(30,Punktezweiter)
                self.dritterName.text=NameZweiter
                
                TauschenDIV(self.divNode3, self.divNode2, breite-(breite/3), breite/3)
                
                SetzenimArray(self.leute, neueLeute[1][0], neueLeute[1][1])   
                TauschenimArray(self.leute, 1, 2)
                
                time.sleep(5)
            
                self.divNode2.pos = (breite/3, 0)
                self.zweiter.pos=(50,50+(b-200)-Punktezweiter)
                self.zweiter.size=(30,Punktezweiter)
                self.zweiterName.text=self.leute[1][0]
            
                self.divNode3.pos = (breite-(breite/3),0)
                self.dritter.pos=(50,b-155)      
                self.dritter.size=(30,5)
                self.dritterName.text=self.leute[2][0]
                
                
            #Zweite Person schon in Liste      
            else :
                i = Suchen(self.leute, neueLeute[1][0])
                if i == 2:
                    self.dritter.pos=(50,50+(b-200)-Punktezweiter)
                    self.dritter.size=(30,Punktezweiter)
                    TauschenDIV(self.divNode2, self.divNode3, breite/3, breite-(breite/3))
                    self.leute[2][1] = neueLeute[2][1]
                    TauschenimArray(self.leute, 1, 2)       
                    
                    time.sleep(5)
            
                    self.divNode2.pos = (breite/3, 0)
                    self.zweiter.pos=(50,50+(b-200)-Punktezweiter)
                    self.zweiter.size=(30,Punktezweiter)
                    self.zweiterName.text=self.leute[1][0]
            
                    self.divNode3.pos = (breite-(breite/3),0)
                    self.dritter.pos=(50,b-155)      
                    self.dritter.size=(30,5)
                    self.dritterName.text=self.leute[2][0] 
                    
                else:
                    self.zweiter.pos=(50,50+(b-200)-Punktezweiter)
                    self.zweiter.size=(30,Punktezweiter)
                    self.leute[1][1] = neueLeute[1][1]
                    
            time.sleep(2)
            #Dritter noch nicht in Liste
            if Suchen(self.leute, neueLeute[2][0])== -1 :
                
                self.dritter.pos= (50,50+(b-200)-Punktedritter)
                self.dritter.size=(30,Punktedritter)
                self.dritterName.text=NameDritter
                
                SetzenimArray(self.leute, neueLeute[2][0], neueLeute[2][1])   
            #Dritter in Liste
            else:
                self.dritter.pos= (50,50+(b-200)-Punktedritter)
                self.dritter.size=(30,Punktedritter)
                SetzenimArray(self.leute, neueLeute[2][0], neueLeute[2][1])   
                
        def receiveArraywithSongs(): ## Initialisieren
            
            a="Silbermond##Nichts passiert##7!#!Juli##Gute Zeit##6!#!Nickelback##Silver side up##5!#!Citizens##True Romance##4!#!Sportfreunde Stiller##Applaus Applaus##3!#!Will.I.am##Scream and Shout##2!#!Justin Timberlake##Mirrors##1" 
            songinput = a.split("!#!")
            stringarray=[]

            ArrayLen = len(songinput)
            for i in range(0,ArrayLen):
                string = songinput[i]
                string2 = string.split("##")
                stringarray.append([string2[0],string2[1],string2[2]]) ##Interpret , Titel, Votes
            print stringarray
                   
            
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
            
        
        def checkArraysthenchange(array1, array2):

            ArrayLen = len(array1)
            for i in range(0,ArrayLen):
                string = songinput[i]
                string2 = string.split("##")
                stringarray.append([string2[0],string2[1],string2[2]]) ##Interpret , Titel, Votes
            print stringarray
            
            
            

            
            
            
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
        string = ("Balken###Pascal###460###Alexander###210###Rebecca###60")
        thread.start_new_thread(recievedpunkte,(string,0))
        receiveArraywithSongs()
        Tauschen(self.div1, self.div2, self.div1.x, self.div1.y, self.div2.x , self.div2.y)
    
        
        
        
  
        
if __name__=='__main__':
    screen.start(resolution=(900, 600))   
  

