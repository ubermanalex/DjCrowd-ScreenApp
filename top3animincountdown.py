'''
Created on 06.06.2013

@author: Steffi
'''

from libavg import *
import time
import thread
import sys
 
from twisted.internet import *
from twisted.python import *
 
from autobahn.websocket import *



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
            
            self.alteOrdnung = []
            self.alteOrdnung.append(["Interpret1", "Song1", "0"])
            self.alteOrdnung.append(["Interpret2", "Song2", "0"])
            self.alteOrdnung.append(["Interpret3", "Song3", "0"])
            self.alteOrdnung.append(["Interpret4", "Song4", "0"])
            self.alteOrdnung.append(["Interpret5", "Song5", "0"])
            self.alteOrdnung.append(["Interpret6", "Song6", "0"])
            self.alteOrdnung.append(["Interpret7", "Song7", "0"])
            
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
            #Titel
            self.platz7a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text="7. ", color="000000", fontsize=30, parent=self.div7)
            #Interpret
            self.platz7b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text="7. ", color="000000", fontsize=20, parent=self.div7)
            #Votes
            self.platz7c=avg.WordsNode (pos=(561,0),font="arial", variant="Bold", text="7. ", color="000000", fontsize=30, parent=self.div7)
            
        
        def schonda (alteOrdnung, suchobjekt, arrayposition):
            print suchobjekt
            print alteOrdnung
            print arrayposition
            i = 0
            while i < 7 :
                print "iter"
                if alteOrdnung[i][arrayposition] == suchobjekt:
                    print i
                    print "mach doch endlich!"
                    return i
                i += 1
            print "schonda?"
            return -1
        
        def swap (a, b):
            def startAnim():
                animObj.start()
                print "anim"
                
            posa = a.pos
            posb = b.pos
            print "pos"
            animObj = ParallelAnim([LinearAnim(a, "pos", 2000, posa, posb),
                                    LinearAnim(b, "pos", 2000, posb, posa)])
            player.setTimeout(0, startAnim)
            time.sleep(2)
            
            
        def colswap (w1a, w1b, w1c, w2a, w2b, w2c):
            col1 = w1a.color
            col2 = w2a.color
            w1a.color = col2
            w1b.color = col2
            w1c.color = col2
            w2a.color = col1
            w2b.color = col1
            w2c.color = col1
            
        
        def sevenSix():
            swap(self.div7, self.div6)
            colswap(self.platz6a, self.platz6b, self.platz6c, self.platz7a, self.platz7b, self.platz7c)
            time.sleep(2)
            
            
            
        def sixFive():
            swap(self.div7, self.div5)
            colswap(self.platz5a, self.platz5b, self.platz5c, self.platz7a, self.platz7b, self.platz7c)
            time.sleep(2)
            
            
            
        def fiveFour():
            swap(self.div7, self.div4)
            colswap(self.platz4a, self.platz4b, self.platz4c, self.platz7a, self.platz7b, self.platz7c)
            time.sleep(2)
            
            
            
        def fourThree():
            swap(self.div7, self.div3)
            colswap(self.platz3a, self.platz3b, self.platz3c, self.platz7a, self.platz7b, self.platz7c)
            time.sleep(2)
            
            
            
        def threeTwo():
            swap(self.div3, self.div2)
            colswap(self.platz2a, self.platz2b, self.platz2c, self.platz7a, self.platz7b, self.platz7c)
            time.sleep(2)
            
            #array anpassen
            TauschenAlteOrdnung(1, 2)
            
            #divs tauschen
            TauschenSongDivs(self.div2, self.div3, 1, 2, self.platz2a, self.platz2b, self.platz2c, self.platz3a, self.platz3b, self.platz3c)
            
            
            
        def twoOne():
            swap(self.div2, self.div1)
            colswap(self.platz1a, self.platz1b, self.platz1c, self.platz2a, self.platz2b, self.platz2c)
            time.sleep(2)
            
            #array anpassen
            TauschenAlteOrdnung(0, 1)
            
            #divs tauschen
            TauschenSongDivs(self.div1, self.div2, 0, 1, self.platz1a, self.platz1b, self.platz1c, self.platz2a, self.platz2b, self.platz2c)
            
            
        def TauschenSongDivs(div1, div2, arrayposition1, arrayposition2, platz1a, platz1b, platz1c, platz2a, platz2b, platz2c):
            pos1 = div1.pos
            pos2 = div2.pos
            div1.pos = pos2
            div2.pos = pos1
            
            platz1a.text = self.alteOrdnung[arrayposition1][1]
            platz1b.text = self.alteOrdnung[arrayposition1][0]
            platz1c.text = self.alteOrdnung[arrayposition1][2]
            
            platz2a.text = self.alteOrdnung[arrayposition2][1]
            platz2b.text = self.alteOrdnung[arrayposition2][0]
            platz2c.text = self.alteOrdnung[arrayposition2][2]
            
            colswap(platz1a, platz1b, platz1c, platz2a, platz2b, platz2c)
            
            time.sleep(2)
            
        def TauschenAlteOrdnung(position1, position2):
            interpret1 = self.alteOrdnung[position1][0]
            song1 = self.alteOrdnung[position1][1]
            votes1 = self.alteOrdnung[position1][2]
            
            self.alteOrdnung[position1][0] = self.alteOrdnung[position2][0]
            self.alteOrdnung[position1][1] = self.alteOrdnung[position2][1]
            self.alteOrdnung[position1][2] = self.alteOrdnung[position2][2]
            
            self.alteOrdnung[position2][0] = interpret1
            self.alteOrdnung[position2][1] = song1
            self.alteOrdnung[position2][2] = votes1
            
        
        """
        def SetzenimArray(array, name, punkte):
            array[2][0] = name
            array[2][1] = punkte"""
            
            
        
        def updateRanking (neueOrdnung, null):  #mit recieveArraywithSongs -> 2 dim stringarray
            #stringarray mit interpret, titel, votes
            time.sleep(2)
            print "neueOrdnung: "
            print neueOrdnung
            #ersern Song setzten
            #noch nicht da:
            if schonda(self.alteOrdnung, neueOrdnung[0][1], 1) == -1:
                print "change"
                self.platz7a.text = neueOrdnung[0][1]
                self.platz7b.text = neueOrdnung[0][0]
                self.platz7c.text = neueOrdnung[0][2]
                print "yes"
                
                sevenSix()
                sixFive()
                fiveFour()
                fourThree()
                threeTwo()
                twoOne()
                
            else:
                if schonda(self.alteOrdnung, neueOrdnung[0][1], 1) == 6: #testen ob interpret gleich und votes aktualisiern
                    sevenSix()
                    sixFive()
                    fiveFour()
                    fourThree()
                    threeTwo()
                    twoOne()
                elif schonda(self.alteOrdnung, neueOrdnung[0][1], 1) == 5:
                    sixFive()
                    fiveFour()
                    fourThree()
                    threeTwo()
                    twoOne()
                elif schonda(self.alteOrdnung, neueOrdnung[0][1], 1) == 4:
                    fiveFour()
                    fourThree()
                    threeTwo()
                    twoOne()
                elif schonda(self.alteOrdnung, neueOrdnung[0][1], 1) == 3:
                    fourThree()
                    threeTwo()
                    twoOne()
                elif schonda(self.alteOrdnung, neueOrdnung[0][1], 1) == 2:
                    threeTwo()
                    twoOne()
                elif schonda(self.alteOrdnung, neueOrdnung[0][1], 1) == 1:
                    print "platz2 mit platz1 tauschen"
                    twoOne()
                elif schonda(self.alteOrdnung, neueOrdnung[0][1], 1) == 0:
                    #votes updaten
                    print "Noemi ist nett"
            
            
            
        """def recievedpunkte(string,null):
                  
             
            #Erster der neuen Liste nicht in alter Liste
            
                
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
                SetzenimArray(self.leute, neueLeute[2][0], neueLeute[2][1])"""
        
        
        
        
        
        
        
        def Top3Anim (number1div, number2div, number3div, number1titel, number2titel, number3titel, size1t, size2t, size3t, pos1div, pos2div, pos3div, 
                      number1inter, number2inter, number3inter, pos1inter, pos2inter, pos3inter, size1inter, size2inter, size3inter,
                      div4, div5, div6, div7, ranking, number1votes, number2votes, number3votes, top7, votes):
                def topthreeanim():
                    animObj.start()
                    
                animObj = ParallelAnim ([LinearAnim(number1titel, "fontsize", 2000, size1t, size1t + 30),
                                        LinearAnim(number2titel, "fontsize", 2000, size2t, size2t + 30),
                                        LinearAnim(number3titel, "fontsize", 2000, size3t, size3t + 30),
                                        
                                        LinearAnim(number1div, "pos", 2000, pos1div, (75, a/10)),
                                        LinearAnim(number2div, "pos", 2000, pos2div, (75, a/4)),
                                        LinearAnim(number3div, "pos", 2000, pos3div, (75, 2*a/5)),
                                        
                                        LinearAnim(number1inter, "pos", 2000, pos1inter, (33, 70)),
                                        LinearAnim(number2inter, "pos", 2000, pos2inter, (33, 70)),
                                        LinearAnim(number3inter, "pos", 2000, pos3inter, (33, 70)),
                                        
                                        LinearAnim(number1inter, "fontsize", 2000, size1inter, size1inter + 20),
                                        LinearAnim(number2inter, "fontsize", 2000, size2inter, size2inter + 20),
                                        LinearAnim(number3inter, "fontsize", 2000, size3inter, size3inter + 20),
                                        
                                        
                                        LinearAnim(div4, "opacity", 2000, 1, 0),
                                        LinearAnim(div5, "opacity", 2000, 1, 0),
                                        LinearAnim(div6, "opacity", 2000, 1, 0),
                                        LinearAnim(div7, "opacity", 2000, 1, 0),
                                        LinearAnim(ranking, "opacity", 2000, 1, 0),
                                        LinearAnim(number1votes, "opacity", 2000, 1, 0),
                                        LinearAnim(number2votes, "opacity", 2000, 1, 0),
                                        LinearAnim(number3votes, "opacity", 2000, 1,0),
                                        
                                        LinearAnim(top7, "opacity", 2000, 1, 0),
                                        LinearAnim(votes, "opacity", 2000, 1, 0)])
                
                player.setTimeout(0, topthreeanim)
        
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
            print "alteOrdnung: "
            print stringarray
            return stringarray
                   
        def initializeDivs(stringarray):
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
            
            #alte Ordnung array aktualisieren
            self.alteOrdnung[0][0] = self.platz1b.text 
            self.alteOrdnung[0][1] = self.platz1a.text
            self.alteOrdnung[0][2] = self.platz1c.text
            self.alteOrdnung[1][0] = self.platz2b.text 
            self.alteOrdnung[1][1] = self.platz2a.text
            self.alteOrdnung[1][2] = self.platz2c.text
            self.alteOrdnung[2][0] = self.platz3b.text 
            self.alteOrdnung[2][1] = self.platz3a.text
            self.alteOrdnung[2][2] = self.platz3c.text
            self.alteOrdnung[3][0] = self.platz4b.text 
            self.alteOrdnung[3][1] = self.platz4a.text
            self.alteOrdnung[3][2] = self.platz4c.text
            self.alteOrdnung[4][0] = self.platz5b.text 
            self.alteOrdnung[4][1] = self.platz5a.text
            self.alteOrdnung[4][2] = self.platz5c.text
            self.alteOrdnung[5][0] = self.platz6b.text 
            self.alteOrdnung[5][1] = self.platz6a.text
            self.alteOrdnung[5][2] = self.platz6c.text
            self.alteOrdnung[6][0] = self.platz7b.text 
            self.alteOrdnung[6][1] = self.platz7a.text
            self.alteOrdnung[6][2] = self.platz7c.text
            
        
            
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
                """if mint == "30" and sect == "0": #wann soll die animation starten
                    Top3Anim(self.div1, self.div2, self.div3, 
                             self.platz1a, self.platz2a, self.platz3a, 
                             self.platz1a.fontsize, self.platz2a.fontsize, self.platz3a.fontsize, 
                             self.div1.pos, self.div2.pos, self.div3.pos,
                             self.platz1b, self.platz2b, self.platz3b, 
                             self.platz1b.pos, self.platz2b.pos, self.platz3b.pos,
                             self.platz1b.fontsize, self.platz2b.fontsize, self.platz3b.fontsize,
                             self.div4, self.div5, self.div6, self.div7,
                             self.ranking,
                             self.platz1c, self.platz2c, self.platz3c,
                             self.title, self.votes)"""
                seconds -= 1
                time.sleep(1)
                if seconds ==0:
                    seconds = 1800
                    
        
        def initializeWebSocket():##Starts the WebSocket
            self.receiver = WebSocketClientFactory("ws://localhost:9034", debug = False)
            a="websocket ok"
            print a
            listenWS(self.receiver)
            reactor.run(installSignalHandlers=0)##"installSignalHandlers=0" Necessary for Multithreading 
        
  
            
        left()
        right()
        thread.start_new_thread(countdown,(0,5))
        string = ("Balken###Pascal###460###Alexander###210###Rebecca###60")
        thread.start_new_thread(recievedpunkte,(string,0))
        initializeDivs(receiveArraywithSongs())
        
        thread.start_new_thread(initializeWebSocket,()) ##start the WebSocket in new Thread
#         Tauschen(self.div1, self.div2, self.div1.x, self.div1.y, self.div2.x , self.div2.y)
        #time.sleep(2)
        neu = [['Juli', 'Gute Zeit', '7'], ['Juli', 'Gute Zeit', '6'], ['Nickelback', 'Silver side up', '5'], ['Citizens', 'True Romance', '4'], ['Sportfreunde Stiller', 'Applaus Applaus', '3'], ['Will.I.am', 'Scream and Shout', '2'], ['Justin Timberlake', 'Mirrors', '1']]
        thread.start_new_thread(updateRanking, (neu,  0))
        
        
         
        
if __name__=='__main__':
    screen.start(resolution=(1440, 800))   
  

