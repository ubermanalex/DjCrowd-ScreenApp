'''
Created on 06.06.2013

@author: Steffi
'''

from libavg import *
import time
import thread
import sys
import ctypes
 
from twisted.internet import *
from twisted.python import *
from autobahn.websocket import *

from copy import deepcopy

class screen(AVGApp):
    def __init__(self, parentNode):
        
        player = avg.Player.get()   #player
        global a,b,z
       
        timeFade = 0.5
        timeAnim = timeFade *1000
        
        maxAnimationDauer = 15 #in sekunden, 0.3 bis 1 sekunde schneller fertig
        #timeVotesFade = 1000
        #timeVotes = 1
        #timeHalf = 0.5
        #timeHalfVotes = 500
        (a,b) = parentNode.size     #aufloesung
        player.setResolution(True,int(a),int(b),32)
        canvas = player.createMainCanvas(size=(a,b)) #canvas kreieren
        self.rootNode = canvas.getRootNode()
        self.back = avg.RectNode (pos=(0,0), size=(a,b), parent=self.rootNode, color="000000", fillcolor="3D4163", fillopacity=1) 
        self.z = int (a-(a/3.5))
        self.title=avg.WordsNode (pos=(a/30,0),font="marketing script", variant="Bold", text="DjCrowd", color="E9EBFF", fontsize=55, alignment="left", parent=self.rootNode) 
        self.logog=avg.ImageNode (href="logodj100pxpng.png", pos=(((a/2)-100),0),parent=self.rootNode)
        self.timer=avg.WordsNode (font="marketing script", variant="Bold", text="Countdown 60:00", color="E9EBFF", fontsize=55, indent=self.z, parent=self.rootNode)
        
        def left(): #links Songs Votes usw
            
            self.alteOrdnung = [] #alter Array zum Vergleichen Initialisierung
            self.alteOrdnung.append(["Interpret1", "Song1", "0"])
            self.alteOrdnung.append(["Interpret2", "Song2", "0"])
            self.alteOrdnung.append(["Interpret3", "Song3", "0"])
            self.alteOrdnung.append(["Interpret4", "Song4", "0"])
            self.alteOrdnung.append(["Interpret5", "Song5", "0"])
            self.alteOrdnung.append(["Interpret6", "Song6", "0"])
            self.alteOrdnung.append(["Interpret7", "Song7", "0"])
            
            middle=a/2.5+10
            
            self.divNode=avg.DivNode(pos=(0,(b/12)), size=(3*(a/5),b-50),parent=self.rootNode)
            self.ranking=avg.WordsNode (pos=(a/30,int(b/6)),font="arial", variant="Bold", width=40, height= (b-50),text="1. <br/> <br/> <br/> 2. <br/> <br/> <br/> 3. <br/> <br/> <br/> 4. <br/> <br/> <br/> 5. <br/> <br/> <br/> 6. <br/> <br/> <br/> 7.", color="E9EBFF", fontsize=30, parent=self.rootNode)
            self.leftr=avg.RectNode (pos=(0,0), size=(3*(a/5), b-50), parent=self.divNode, color="000000", fillcolor="464646",fillopacity=1)
            self.title=avg.WordsNode (pos=(int(a/5.5),0),font="marketing script", variant="Bold", text=" Top 7 Songs ", color="E9EBFF", fontsize=40, parent=self.divNode)
            self.votes=avg.WordsNode (pos=(int(a/2-80),0),font="marketing script", variant="Bold", text="Votes", color="E9EBFF", fontsize=40, parent=self.divNode)
            
            self.div1=avg.DivNode(pos=(a/18,b/6), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz1a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text=self.alteOrdnung[0][1], color="DDDC3C", fontsize=30, parent=self.div1)
            self.platz1b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text=self.alteOrdnung[0][0], color="DDDC3C", fontsize=20, parent=self.div1)
            self.platz1c=avg.WordsNode (pos=(middle,0),font="arial", variant="Bold", text=self.alteOrdnung[0][2], color="DDDC3C", fontsize=30, parent=self.div1)
            
            
            self.div2=avg.DivNode(pos=(a/18,b/3.5175), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz2a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text=self.alteOrdnung[1][1], color="C9C9C5", fontsize=30, parent=self.div2)
            self.platz2b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text=self.alteOrdnung[1][0], color="C9C9C5", fontsize=20, parent=self.div2)
            self.platz2c=avg.WordsNode (pos=(middle,0),font="arial", variant="Bold", text=self.alteOrdnung[1][2], color="C9C9C5", fontsize=30, parent=self.div2)
            
            self.div3=avg.DivNode(pos=(a/18,b/2.495), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz3a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text=self.alteOrdnung[2][1], color="EFBF34", fontsize=30, parent=self.div3)
            self.platz3b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text=self.alteOrdnung[2][0], color="EFBF34", fontsize=20, parent=self.div3)
            self.platz3c=avg.WordsNode (pos=(middle,0),font="arial", variant="Bold", text=self.alteOrdnung[2][2], color="EFBF34", fontsize=30, parent=self.div3)
            
            
            self.div4=avg.DivNode(pos=(a/18,b/1.935), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz4a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text=self.alteOrdnung[3][1], color="E9EBFF", fontsize=30, parent=self.div4)
            self.platz4b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text=self.alteOrdnung[3][0], color="E9EBFF", fontsize=20, parent=self.div4)
            self.platz4c=avg.WordsNode (pos=(middle,0),font="arial", variant="Bold", text=self.alteOrdnung[3][2], color="E9EBFF", fontsize=30, parent=self.div4)
            
            self.div5=avg.DivNode(pos=(a/18,b/1.58), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz5a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text=self.alteOrdnung[4][1], color="E9EBFF", fontsize=30, parent=self.div5)
            self.platz5b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text=self.alteOrdnung[4][0], color="E9EBFF", fontsize=20, parent=self.div5)
            self.platz5c=avg.WordsNode (pos=(middle,0),font="arial", variant="Bold", text=self.alteOrdnung[4][2], color="E9EBFF", fontsize=30, parent=self.div5)
            
            self.div6=avg.DivNode(pos=(a/18,b/1.335), size=(3*(a/5)-20,30),parent=self.rootNode)
            self.platz6a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text=self.alteOrdnung[5][1], color="E9EBFF", fontsize=30, parent=self.div6)
            self.platz6b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text=self.alteOrdnung[5][0], color="E9EBFF", fontsize=20, parent=self.div6)
            self.platz6c=avg.WordsNode (pos=(middle,0),font="arial", variant="Bold", text=self.alteOrdnung[5][2], color="E9EBFF", fontsize=30, parent=self.div6)
            
            self.div7=avg.DivNode(pos=(a/18,b/1.155), size=(3*(a/5)-20,30),parent=self.rootNode)
            #Titel
            self.platz7a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text=self.alteOrdnung[6][1], color="E9EBFF", fontsize=30, parent=self.div7)
            #Interpret
            self.platz7b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text=self.alteOrdnung[6][0], color="E9EBFF", fontsize=20, parent=self.div7)
            #Votes
            self.platz7c=avg.WordsNode (pos=(middle,0),font="arial", variant="Bold", text=self.alteOrdnung[6][2], color="E9EBFF", fontsize=30, parent=self.div7)
            
           
        def fadeAnimSongsTop3 (neueOrdnung, null):
            time.sleep(0.1)
            fadeOut(self.div1, timeAnim)
            fadeOut(self.div2, timeAnim)
            fadeOut(self.div3, timeAnim)
            time.sleep(timeFade)
            
            self.div1.pos = (a/18,b/6)
            self.div2.pos = (a/18,b/3.5175)
            self.div3.pos = (a/18,b/2.495) 
            
            self.platz1b.pos = (33, 40) 
            self.platz2b.pos = (33, 40)
            self.platz3b.pos = (33, 40)
            
            self.platz1a.fontsize = 30 
            self.platz2a.fontsize = 30
            self.platz3a.fontsize = 30
            self.platz1b.fontsize = 20
            self.platz2b.fontsize = 20
            self.platz3b.fontsize = 20
            
            self.platz1a.text= neueOrdnung[0][1]
            self.platz2a.text= neueOrdnung[1][1]
            self.platz3a.text= neueOrdnung[2][1]
            self.platz4a.text= neueOrdnung[3][1]
            self.platz5a.text= neueOrdnung[4][1]
            self.platz6a.text= neueOrdnung[5][1]
            self.platz7a.text= neueOrdnung[6][1]
                
            self.platz1b.text= neueOrdnung[0][0]
            self.platz2b.text= neueOrdnung[1][0]
            self.platz3b.text= neueOrdnung[2][0]
            self.platz4b.text= neueOrdnung[3][0]
            self.platz5b.text= neueOrdnung[4][0]
            self.platz6b.text= neueOrdnung[5][0]
            self.platz7b.text= neueOrdnung[6][0]
             
            self.platz1c.text= neueOrdnung[0][2]
            self.platz2c.text= neueOrdnung[1][2]
            self.platz3c.text= neueOrdnung[2][2]
            self.platz4c.text= neueOrdnung[3][2]
            self.platz5c.text= neueOrdnung[4][2]
            self.platz6c.text= neueOrdnung[5][2]
            self.platz7c.text= neueOrdnung[6][2]
            #print "jetzt doch?"
            #altes array anpassen
            self.alteOrdnung = deepcopy(neueOrdnung)
            #print "waaas"
            fadeIn(self.div1, timeAnim)
            fadeIn(self.div2, timeAnim)
            fadeIn(self.div3, timeAnim)
            fadeIn(self.div4, timeAnim)
            fadeIn(self.div5, timeAnim)
            fadeIn(self.div6, timeAnim)
            fadeIn(self.div7, timeAnim)
            fadeIn(self.ranking, timeAnim)
            fadeIn(self.platz1c, timeAnim)
            fadeIn(self.platz2c, timeAnim)
            fadeIn(self.platz3c, timeAnim)
                
            #print "ich"  
            
        def fadeAnimSongsNormal (neueOrdnung, null):
            time.sleep(0.1)
            #print "ahhhh"
            fadeOut(self.div1, timeAnim)
            #print "hi"
            fadeOut(self.div2, timeAnim)
            #print "nein"
            fadeOut(self.div3, timeAnim)
            fadeOut(self.div4, timeAnim)
            fadeOut(self.div5, timeAnim)
            fadeOut(self.div6, timeAnim)
            fadeOut(self.div7, timeAnim)
            time.sleep(timeFade)
            #print "was"
            
            self.platz1a.text= neueOrdnung[0][1]
            self.platz2a.text= neueOrdnung[1][1]
            self.platz3a.text= neueOrdnung[2][1]
            self.platz4a.text= neueOrdnung[3][1]
            self.platz5a.text= neueOrdnung[4][1]
            self.platz6a.text= neueOrdnung[5][1]
            self.platz7a.text= neueOrdnung[6][1]
                
            self.platz1b.text= neueOrdnung[0][0]
            self.platz2b.text= neueOrdnung[1][0]
            self.platz3b.text= neueOrdnung[2][0]
            self.platz4b.text= neueOrdnung[3][0]
            self.platz5b.text= neueOrdnung[4][0]
            self.platz6b.text= neueOrdnung[5][0]
            self.platz7b.text= neueOrdnung[6][0]
             
            self.platz1c.text= neueOrdnung[0][2]
            self.platz2c.text= neueOrdnung[1][2]
            self.platz3c.text= neueOrdnung[2][2]
            self.platz4c.text= neueOrdnung[3][2]
            self.platz5c.text= neueOrdnung[4][2]
            self.platz6c.text= neueOrdnung[5][2]
            self.platz7c.text= neueOrdnung[6][2]
            #print "jetzt doch?"
            self.alteOrdnung = deepcopy(neueOrdnung)
            #print "waaas"
            fadeIn(self.div1, timeAnim)
            fadeIn(self.div2, timeAnim)
            fadeIn(self.div3, timeAnim)
            fadeIn(self.div4, timeAnim)
            fadeIn(self.div5, timeAnim)
            fadeIn(self.div6, timeAnim)
            fadeIn(self.div7, timeAnim)
                
            #print "ich"
        
        def TauschenKopie(array, position1, position2): #Arrayanpassung der Kopie des alten Ordnung
            interpret1 = array[position1][0]
            song1 = array[position1][1]
            votes1 = array[position1][2]
            
            array[position1][0] = array[position2][0]
            array[position1][1] = array[position2][1]
            array[position1][2] = array[position2][2]
            
            array[position2][0] = interpret1
            array[position2][1] = song1
            array[position2][2] = votes1
        
        
         
        def animationUpdate (neueOrdnung):
            animationDauer = 3
            print "initalisierung", animationDauer
            kopie = deepcopy(self.alteOrdnung)
            #kopie = []
            #for i in range(7):    
            #   kopie.append(self.alteOrdnung[i])
            #print neueOrdnung
            #print self.alteOrdnung
            #print kopie
#             self.alteOrdnung[0][0] = "scheisse"
#             print neueOrdnung
#             print self.alteOrdnung
#             print kopie

            #berechne animationsdauer
            
            
            
            
            
            #platz 1
            anzAnim1 = schonda(kopie, neueOrdnung[0][1], neueOrdnung[0][0]) #platz 1
            animationDauer += (anzAnim1 + 1) * timeFade #animationen und votes anpassung animation
            print "platz 1:", animationDauer
            if anzAnim1 == 7: #nich in liste
                #arraykopie altes array anpassen
                kopie[6][0] = neueOrdnung[0][0]
                kopie[6][1] = neueOrdnung[0][1]
                kopie[6][2] = neueOrdnung[0][2]
                
                animationDauer -= 1 * timeFade #da votes nicht aktualisiert werden muessen
                
                TauschenKopie (kopie, 5, 6)
                TauschenKopie (kopie, 4, 5)
                TauschenKopie (kopie, 3, 4)
                TauschenKopie (kopie, 2, 3)
                TauschenKopie (kopie, 1, 2)
                TauschenKopie (kopie, 0, 1)
            elif anzAnim1 == 6: #platz 7
                TauschenKopie (kopie, 5, 6)
                TauschenKopie (kopie, 4, 5)
                TauschenKopie (kopie, 3, 4)
                TauschenKopie (kopie, 2, 3)
                TauschenKopie (kopie, 1, 2)
                TauschenKopie (kopie, 0, 1)
            elif anzAnim1 == 5: #platz 6
                TauschenKopie (kopie, 4, 5)
                TauschenKopie (kopie, 3, 4)
                TauschenKopie (kopie, 2, 3)
                TauschenKopie (kopie, 1, 2)
                TauschenKopie (kopie, 0, 1)
            elif anzAnim1 == 4: #platz 5
                TauschenKopie (kopie, 3, 4)
                TauschenKopie (kopie, 2, 3)
                TauschenKopie (kopie, 1, 2)
                TauschenKopie (kopie, 0, 1)
            elif anzAnim1 == 3: #platz 4
                TauschenKopie (kopie, 2, 3)
                TauschenKopie (kopie, 1, 2)
                TauschenKopie (kopie, 0, 1)
            elif anzAnim1 == 2: #platz 3
                TauschenKopie (kopie, 1, 2)
                TauschenKopie (kopie, 0, 1)
            elif anzAnim1 == 1: #platz 2
                TauschenKopie (kopie, 0, 1)
            elif anzAnim1 == 0: #platz 1
                if kopie[0][2] == neueOrdnung[0][2]:
                    animationDauer -= 1 * timeFade #da votes nicht angepasst werden muessen
                
            print "platz 1:", animationDauer
                
                
            anzAnim2 = schonda(kopie, neueOrdnung[1][1], neueOrdnung[1][0]) #platz 2
            animationDauer += (anzAnim2 - 0) * timeFade
            print "platz 2:", animationDauer
            if anzAnim2 == 7: #nich in liste
                #arraykopie altes array anpassen
                kopie[6][0] = neueOrdnung[1][0]
                kopie[6][1] = neueOrdnung[1][1]
                kopie[6][2] = neueOrdnung[1][2]
                
                animationDauer -= 1 * timeFade
                
                TauschenKopie (kopie, 5, 6)
                TauschenKopie (kopie, 4, 5)
                TauschenKopie (kopie, 3, 4)
                TauschenKopie (kopie, 2, 3)
                TauschenKopie (kopie, 1, 2)
            elif anzAnim2 == 6: #platz 7
                TauschenKopie (kopie, 5, 6)
                TauschenKopie (kopie, 4, 5)
                TauschenKopie (kopie, 3, 4)
                TauschenKopie (kopie, 2, 3)
                TauschenKopie (kopie, 1, 2)
            elif anzAnim2 == 5: #platz 6
                TauschenKopie (kopie, 4, 5)
                TauschenKopie (kopie, 3, 4)
                TauschenKopie (kopie, 2, 3)
                TauschenKopie (kopie, 1, 2)
            elif anzAnim2 == 4: #platz 5
                TauschenKopie (kopie, 3, 4)
                TauschenKopie (kopie, 2, 3)
                TauschenKopie (kopie, 1, 2)
            elif anzAnim2 == 3: #platz 4
                TauschenKopie (kopie, 2, 3)
                TauschenKopie (kopie, 1, 2)
            elif anzAnim2 == 2: #platz 3
                TauschenKopie (kopie, 1, 2)
            elif anzAnim2 == 1: #platz 2
                if kopie[1][2] == neueOrdnung[1][2]:
                    animationDauer -= 1 * timeFade
            
            print "platz 2:", animationDauer
            
            
            anzAnim3 = schonda(kopie, neueOrdnung[2][1], neueOrdnung[2][0]) #platz 3
            animationDauer += (anzAnim3 - 1) * timeFade
            print "platz 3:", animationDauer
            if anzAnim3 == 7: #nich in liste
                #arraykopie altes array anpassen
                kopie[6][0] = neueOrdnung[2][0]
                kopie[6][1] = neueOrdnung[2][1]
                kopie[6][2] = neueOrdnung[2][2]
                
                animationDauer -= 1 * timeFade
                
                TauschenKopie (kopie, 5, 6)
                TauschenKopie (kopie, 4, 5)
                TauschenKopie (kopie, 3, 4)
                TauschenKopie (kopie, 2, 3)
            elif anzAnim3 == 6: #platz 7
                TauschenKopie (kopie, 5, 6)
                TauschenKopie (kopie, 4, 5)
                TauschenKopie (kopie, 3, 4)
                TauschenKopie (kopie, 2, 3)
            elif anzAnim3 == 5: #platz 6
                TauschenKopie (kopie, 4, 5)
                TauschenKopie (kopie, 3, 4)
                TauschenKopie (kopie, 2, 3)
            elif anzAnim3 == 4: #platz 5
                TauschenKopie (kopie, 3, 4)
                TauschenKopie (kopie, 2, 3)
            elif anzAnim3 == 3: #platz 4
                TauschenKopie (kopie, 2, 3)
            elif anzAnim3 == 2: #platz 3
                if kopie[2][2] == neueOrdnung[2][2]:
                    animationDauer -= 1 * timeFade
                    
            print "platz 3:", animationDauer     
                    
            
            anzAnim4 = schonda(kopie, neueOrdnung[3][1], neueOrdnung[3][0]) #platz 4
            animationDauer += (anzAnim4 - 2) * timeFade
            print "platz 4:", animationDauer
            if anzAnim4 == 7: #nich in liste
                #arraykopie altes array anpassen
                kopie[6][0] = neueOrdnung[3][0]
                kopie[6][1] = neueOrdnung[3][1]
                kopie[6][2] = neueOrdnung[3][2]
                
                animationDauer -= 1 * timeFade
                
                TauschenKopie (kopie, 5, 6)
                TauschenKopie (kopie, 4, 5)
                TauschenKopie (kopie, 3, 4)
            elif anzAnim4 == 6: #platz 7
                TauschenKopie (kopie, 5, 6)
                TauschenKopie (kopie, 4, 5)
                TauschenKopie (kopie, 3, 4)
            elif anzAnim4 == 5: #platz 6
                TauschenKopie (kopie, 4, 5)
                TauschenKopie (kopie, 3, 4)
            elif anzAnim4 == 4: #platz 5
                TauschenKopie (kopie, 3, 4)
            elif anzAnim4 == 3: #platz 4
                if kopie[3][2] == neueOrdnung[3][2]:
                    animationDauer -= 1 * timeFade
            
            print "platz 4:", animationDauer
            
            
            
            anzAnim5 = schonda(kopie, neueOrdnung[4][1], neueOrdnung[4][0]) #platz 5
            animationDauer += (anzAnim5 - 3) * timeFade
            print "platz 5:", animationDauer
            if anzAnim5 == 7: #nich in liste
                #arraykopie altes array anpassen
                kopie[6][0] = neueOrdnung[4][0]
                kopie[6][1] = neueOrdnung[4][1]
                kopie[6][2] = neueOrdnung[4][2]
                
                animationDauer -= 1 * timeFade
                
                TauschenKopie (kopie, 5, 6)
                TauschenKopie (kopie, 4, 5)
            elif anzAnim5 == 6: #platz 7
                TauschenKopie (kopie, 5, 6)
                TauschenKopie (kopie, 4, 5)
            elif anzAnim5 == 5: #platz 6
                TauschenKopie (kopie, 4, 5)
            elif anzAnim5 == 4: #platz 5
                if kopie[4][2] == neueOrdnung[4][2]:
                    animationDauer -= 1 * timeFade
            
            print "platz 5:", animationDauer
            
            
            
            anzAnim6 = schonda(kopie, neueOrdnung[5][1], neueOrdnung[5][0]) #platz 6
            animationDauer += (anzAnim6 - 4) * timeFade
            print "platz 6:", animationDauer
            if anzAnim6 == 7: #nich in liste
                #arraykopie altes array anpassen
                kopie[6][0] = neueOrdnung[5][0]
                kopie[6][1] = neueOrdnung[5][1]
                kopie[6][2] = neueOrdnung[5][2]
                
                animationDauer -= 1 * timeFade
                
                TauschenKopie (kopie, 5, 6)
            elif anzAnim6 == 6: #platz 7
                TauschenKopie (kopie, 5, 6)
            elif anzAnim6 == 5: #platz 6
                if kopie[5][2] == neueOrdnung[5][2]:
                    animationDauer -= 1 * timeFade
            print "platz 6:", animationDauer
            
            
            
            anzAnim7 = schonda(kopie, neueOrdnung[6][1], neueOrdnung[6][0]) #platz 7
            animationDauer += (anzAnim7 - 5) * timeFade
            print "platz 7:", animationDauer
            if anzAnim7 == 7: #nich in liste
                #arraykopie altes array anpassen
                kopie[6][0] = neueOrdnung[6][0]
                kopie[6][1] = neueOrdnung[6][1]
                kopie[6][2] = neueOrdnung[6][2]
                
                animationDauer -= 1 * timeFade
#                 
            elif anzAnim7 == 6: #platz 7
                if kopie[6][2] == neueOrdnung[6][2]:
                    animationDauer -= 1 * timeFade
            print "platz 7:", animationDauer
            
            
            
            
            print "ende:", animationDauer
            
            if (animationDauer > maxAnimationDauer):
                #print "zu lang"
                thread.start_new_thread(fadeAnimSongsNormal, (neueOrdnung, 0)) #fadeanimation wird ausfefuehrt
            else:
#                 print "klappt"
#                 print self.alteOrdnung
#                 print kopie
#                 print neueOrdnung
                thread.start_new_thread(updateRanking, (neueOrdnung, 0)) #animation wird duchgefuehrt
            
        
        
        def schonda (alteOrdnung, song, interpret): #check in alter Ordnung, ob in geg. Lied schon im alterOrdnung drin ist
            i = 0
            while i < 7 :
                if alteOrdnung[i][1] == song and alteOrdnung[i][0] == interpret:
                    return i
                i += 1
            return -1
        
        def swap (a, b): #linke Swap animation von den Divs fuer Ranking
            def startAnim():
                animObj.start()
                
            posa = a.pos
            posb = b.pos
            animObj = ParallelAnim([LinearAnim(a, "pos", 500, posa, posb),
                                    LinearAnim(b, "pos", 500, posb, posa)])
            player.setTimeout(0, startAnim)
            time.sleep(0.5)
            
            
        def colswap (w1a, w1b, w1c, w2a, w2b, w2c): #farben aendern der DIVNodes wenn Ranking 1 2 3 usw.
            #tauscht die Farben der Wordsnodes in 2 divs
            col1 = w1a.color
            col2 = w2a.color
            w1a.color = col2
            w1b.color = col2
            w1c.color = col2
            w2a.color = col1
            w2b.color = col1
            w2c.color = col1
            
        
        def sevenSix(): #Tauschfunktion von Paar
            swap(self.div7, self.div6)
            colswap(self.platz6a, self.platz6b, self.platz6c, self.platz7a, self.platz7b, self.platz7c)
            time.sleep(0.1)
            #array anpassen
            TauschenAlteOrdnung(5, 6)
            #divs tauschen
            TauschenSongDivs(self.div6, self.div7, 5, 6, self.platz6a, self.platz6b, self.platz6c, self.platz7a, self.platz7b, self.platz7c)
            
            
            
        def sixFive(): #Tauschfunktion von Paar
            swap(self.div6, self.div5)
            colswap(self.platz5a, self.platz5b, self.platz5c, self.platz6a, self.platz6b, self.platz6c)
            time.sleep(0.1)
            #array anpassen
            TauschenAlteOrdnung(4, 5)
            #divs tauschen
            TauschenSongDivs(self.div5, self.div6, 4, 5, self.platz5a, self.platz5b, self.platz5c, self.platz6a, self.platz6b, self.platz6c)
            
            
            
        def fiveFour(): #Tauschfunktion von Paar
            swap(self.div5, self.div4)
            colswap(self.platz4a, self.platz4b, self.platz4c, self.platz5a, self.platz5b, self.platz5c)
            time.sleep(0.1)
            #array anpassen
            TauschenAlteOrdnung(3, 4)
            #divs tauschen
            TauschenSongDivs(self.div4, self.div5, 3, 4, self.platz4a, self.platz4b, self.platz4c, self.platz5a, self.platz5b, self.platz5c)
            
            
            
        def fourThree():#Tauschfunktion von Paar
            swap(self.div4, self.div3)
            colswap(self.platz3a, self.platz3b, self.platz3c, self.platz4a, self.platz4b, self.platz4c)
            time.sleep(0.1)
            #array anpassen
            TauschenAlteOrdnung(2, 3)
            #divs tauschen
            TauschenSongDivs(self.div3, self.div4, 2, 3, self.platz3a, self.platz3b, self.platz3c, self.platz4a, self.platz4b, self.platz4c)
            
            
            
        def threeTwo():#Tauschfunktion von Paar
            swap(self.div3, self.div2)
            colswap(self.platz2a, self.platz2b, self.platz2c, self.platz3a, self.platz3b, self.platz3c)
            time.sleep(0.1)
            #array anpassen
            TauschenAlteOrdnung(1, 2)
            #divs tauschen
            TauschenSongDivs(self.div2, self.div3, 1, 2, self.platz2a, self.platz2b, self.platz2c, self.platz3a, self.platz3b, self.platz3c)
            
            
            
        def twoOne():#Tauschfunktion von Paar
            swap(self.div2, self.div1)
            colswap(self.platz1a, self.platz1b, self.platz1c, self.platz2a, self.platz2b, self.platz2c)
            time.sleep(0.1)
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
           
            
        def TauschenAlteOrdnung(position1, position2): #Arrayanpassung der getauschten Positionen
            interpret1 = self.alteOrdnung[position1][0]
            song1 = self.alteOrdnung[position1][1]
            votes1 = self.alteOrdnung[position1][2]
            
            self.alteOrdnung[position1][0] = self.alteOrdnung[position2][0]
            self.alteOrdnung[position1][1] = self.alteOrdnung[position2][1]
            self.alteOrdnung[position1][2] = self.alteOrdnung[position2][2]
            
            self.alteOrdnung[position2][0] = interpret1
            self.alteOrdnung[position2][1] = song1
            self.alteOrdnung[position2][2] = votes1
            
        def div7Setzen(neueOrdnung0,neueOrdnung1, neueOrdnung2):  #neues Lied ganz unten initialisieren
            fadeOut(self.platz7a, 500)
            fadeOut(self.platz7b, 500)
            fadeOut(self.platz7c, 500)
            time.sleep(0.5)
            self.platz7a.text = neueOrdnung1
            self.platz7b.text = neueOrdnung0
            self.platz7c.text = neueOrdnung2
            fadeIn(self.platz7a, 500)
            fadeIn(self.platz7b, 500)
            fadeIn(self.platz7c, 500)
            time.sleep(0.5)
            
        def aktualisiereVotes(position, wordsnode, neueVotes): #Votes aktualisieren, nur wenn das Lied bereits vorhanden
            fadeOut(wordsnode, 500)
            time.sleep(0.5)
            wordsnode.text = neueVotes
            fadeIn(wordsnode, 500)
            time.sleep(0.5)
            self.alteOrdnung[position][2] = neueVotes
            time.sleep(0.1)
            
        def votesInAlteOrdnungAnpassen(platz, neueVotes): # Vote aktualisert vom veraenderten Lied
            self.alteOrdnung[platz][2] = neueVotes
       
        def platz7inAlteOrdnungSetzen(song, interpret, votes): # in Array 
            self.alteOrdnung[6][0] = interpret
            self.alteOrdnung[6][1] = song
            self.alteOrdnung[6][2] = votes
            
        
        def updateRanking (neueOrdnung, null):  #mit recieveArraywithSongs -> 2 dim stringarray
            #stringarray mit interpret, titel, votes
            time.sleep(0.5)
            #print "neueOrdnung: "
            #print neueOrdnung
            #ersern Song setzten
            #noch nicht da:
            where = schonda(self.alteOrdnung, neueOrdnung[0][1], neueOrdnung[0][0])
            if where == -1:
                #div 7 setzen
                #print "change"
                div7Setzen(neueOrdnung[0][0], neueOrdnung[0][1], neueOrdnung[0][2])
                
                #infos in array anpassen
                platz7inAlteOrdnungSetzen(self.platz7a.text, self.platz7b.text, self.platz7c.text)
                #print self.alteOrdnung
                
                sevenSix()
                sixFive()
                fiveFour()
                fourThree()
                threeTwo()
                twoOne()
                
                #print self.alteOrdnung
                
            else:
                if where == 6: #testen ob interpret gleich und votes aktualisiern
                    aktualisiereVotes(6, self.platz7c, neueOrdnung[0][2])
                    sevenSix()
                    sixFive()
                    fiveFour()
                    fourThree()
                    threeTwo()
                    twoOne()
                elif where == 5:
                    aktualisiereVotes(5, self.platz6c, neueOrdnung[0][2])
                    sixFive()
                    fiveFour()
                    fourThree()
                    threeTwo()
                    twoOne()
                elif where == 4:
                    aktualisiereVotes(4, self.platz5c, neueOrdnung[0][2])
                    fiveFour()
                    fourThree()
                    threeTwo()
                    twoOne()
                elif where == 3:
                    aktualisiereVotes(3, self.platz4c, neueOrdnung[0][2])
                    fourThree()
                    threeTwo()
                    twoOne()
                elif where == 2:
                    aktualisiereVotes(2, self.platz3c, neueOrdnung[0][2])
                    threeTwo()
                    twoOne()
                elif where == 1:
                    #print "platz2 mit platz1 tauschen"
                    aktualisiereVotes(1, self.platz2c, neueOrdnung[0][2])
                    twoOne()
                elif where == 0:
                    #votes updaten
                    #print "Noemi ist nett"
                    if self.platz1c.text != neueOrdnung[0][2]:
                        #print self.platz1c.text
                        #print neueOrdnung[0][2]
                        aktualisiereVotes(0, self.platz1c, neueOrdnung[0][2])
                    
                    
            #print "platz 1 gesetzt"
            
            #print "starte platz 2"   
            where2 = schonda(self.alteOrdnung, neueOrdnung[1][1], neueOrdnung[1][0])
            if where2 == -1:
                #div 7 setzen
                #print "change"
                div7Setzen(neueOrdnung[1][0], neueOrdnung[1][1], neueOrdnung[1][2])
                
                #infos in array anpassen
                platz7inAlteOrdnungSetzen(self.platz7a.text, self.platz7b.text, self.platz7c.text)
                #print self.alteOrdnung
                
                sevenSix()
                sixFive()
                fiveFour()
                fourThree()
                threeTwo()
                
            else:
                if where2 == 6: #testen ob interpret gleich und votes aktualisiern
                    aktualisiereVotes(6, self.platz7c, neueOrdnung[1][2])
                    sevenSix()
                    sixFive()
                    fiveFour()
                    fourThree()
                    threeTwo()
                elif where2 == 5:
                    aktualisiereVotes(5, self.platz6c, neueOrdnung[1][2])
                    sixFive()
                    fiveFour()
                    fourThree()
                    threeTwo()
                elif where2 == 4:
                    aktualisiereVotes(4, self.platz5c, neueOrdnung[1][2])
                    fiveFour()
                    fourThree()
                    threeTwo()
                elif where2 == 3:
                    aktualisiereVotes(3, self.platz4c, neueOrdnung[1][2])
                    fourThree()
                    threeTwo()
                elif where2 == 2:
                    aktualisiereVotes(2, self.platz3c, neueOrdnung[1][2])
                    threeTwo()
                elif where2 == 1:
                    #print "platz2 mit platz1 tauschen"
                    if self.platz2c.text != neueOrdnung[1][2]:
                        aktualisiereVotes(1, self.platz2c, neueOrdnung[1][2])
            #print "platz 2 gesetzt"
                    
            #print "starte platz 3"   
            where3 = schonda(self.alteOrdnung, neueOrdnung[2][1], neueOrdnung[2][0])
            if where3 == -1:
                #div 7 setzen
                #print "change"
                div7Setzen(neueOrdnung[2][0], neueOrdnung[2][1], neueOrdnung[2][2])
                
                #infos in array anpassen
                platz7inAlteOrdnungSetzen(self.platz7a.text, self.platz7b.text, self.platz7c.text)
                #print self.alteOrdnung
                
                sevenSix()
                sixFive()
                fiveFour()
                fourThree()
                                          
            else:
                if where3 == 6: #testen ob interpret gleich und votes aktualisiern
                    aktualisiereVotes(6, self.platz7c, neueOrdnung[2][2])
                    sevenSix()
                    sixFive()
                    fiveFour()
                    fourThree()
                elif where3 == 5:
                    aktualisiereVotes(5, self.platz6c, neueOrdnung[2][2])
                    sixFive()
                    fiveFour()
                    fourThree()
                elif where3 == 4:
                    aktualisiereVotes(4, self.platz5c, neueOrdnung[2][2])
                    fiveFour()
                    fourThree()
                elif where3 == 3:
                    aktualisiereVotes(3, self.platz4c, neueOrdnung[2][2])
                    fourThree()
                elif where3 == 2:
                    if self.platz3c.text != neueOrdnung[2][2]:
                        aktualisiereVotes(2, self.platz3c, neueOrdnung[2][2])
            #print "platz 3 gesetzt"
            
            #print "starte platz 4"   
            where4 = schonda(self.alteOrdnung, neueOrdnung[3][1], neueOrdnung[3][0])
            if where4 == -1:
                #div 7 setzen
                #print "change"
                div7Setzen(neueOrdnung[3][0], neueOrdnung[3][1], neueOrdnung[3][2])
                
                #infos in array anpassen
                platz7inAlteOrdnungSetzen(self.platz7a.text, self.platz7b.text, self.platz7c.text)
                #print self.alteOrdnung
                
                sevenSix()
                sixFive()
                fiveFour()
                                          
            else:
                if where4 == 6: #testen ob interpret gleich und votes aktualisiern
                    aktualisiereVotes(6, self.platz7c, neueOrdnung[3][2])
                    sevenSix()
                    sixFive()
                    fiveFour()
                elif where4 == 5:
                    aktualisiereVotes(5, self.platz6c, neueOrdnung[3][2])
                    sixFive()
                    fiveFour()
                elif where4 == 4:
                    aktualisiereVotes(4, self.platz5c, neueOrdnung[3][2])
                    fiveFour()
                elif where4 == 3:
                    if self.platz4c.text != neueOrdnung[3][2]:
                        aktualisiereVotes(3, self.platz4c, neueOrdnung[3][2])
            #print "platz 4 gesetzt"
            
            #print "starte platz 5"   
            where5 = schonda(self.alteOrdnung, neueOrdnung[4][1], neueOrdnung[4][0])
            if where5 == -1:
                #div 7 setzen
                #print "change"
                div7Setzen(neueOrdnung[4][0], neueOrdnung[4][1], neueOrdnung[4][2])
                
                #infos in array anpassen
                platz7inAlteOrdnungSetzen(self.platz7a.text, self.platz7b.text, self.platz7c.text)
                #print self.alteOrdnung
                
                sevenSix()
                sixFive()
                                          
            else:
                if where5 == 6: #testen ob interpret gleich und votes aktualisiern
                    aktualisiereVotes(6, self.platz7c, neueOrdnung[4][2])
                    sevenSix()
                    sixFive()
                elif where5 == 5:
                    aktualisiereVotes(5, self.platz6c, neueOrdnung[4][2])
                    sixFive()
                elif where5 == 4:
                    if self.platz5c.text != neueOrdnung[4][2]:
                        aktualisiereVotes(4, self.platz5c, neueOrdnung[4][2])
            #print "platz 5 gesetzt"
            
            #print "starte platz 6"   
            where6 = schonda(self.alteOrdnung, neueOrdnung[5][1], neueOrdnung[5][0])
            if where6 == -1:
                #div 7 setzen
                #print "change"
                div7Setzen(neueOrdnung[5][0], neueOrdnung[5][1], neueOrdnung[5][2])
                
                #infos in array anpassen
                platz7inAlteOrdnungSetzen(self.platz7a.text, self.platz7b.text, self.platz7c.text)
                #print self.alteOrdnung
                
                sevenSix()
                                          
            else:
                if where6 == 6: #testen ob interpret gleich und votes aktualisiern
                    aktualisiereVotes(6, self.platz7c, neueOrdnung[5][2])
                    sevenSix()
                elif where6 == 5:
                    if self.platz6c.text != neueOrdnung[5][2]:
                        aktualisiereVotes(5, self.platz6c, neueOrdnung[5][2])
            #print "platz 6 gesetzt"
            
            #print "starte platz 7"   
            where7 = schonda(self.alteOrdnung, neueOrdnung[6][1], neueOrdnung[6][0])
            if where7 == -1:
                #div 7 setzen
                #print "change"
                div7Setzen(neueOrdnung[6][0], neueOrdnung[6][1], neueOrdnung[6][2])
                
                #infos in array anpassen
                platz7inAlteOrdnungSetzen(self.platz7a.text, self.platz7b.text, self.platz7c.text)
                #print self.alteOrdnung
                
                                          
            else:
                if where7 == 6: #testen ob interpret gleich und votes aktualisiern
                    if self.platz7c.text != neueOrdnung[6][2]:
                        aktualisiereVotes(6, self.platz7c, neueOrdnung[6][2])
            #print "platz 6 gesetzt"
            
            #print self.alteOrdnung
        
        
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
            self.divNode=avg.DivNode(pos=(a-2*(a/4.25),75), size=(2*(a/4.25),b),parent=self.rootNode)
            self.rightr=avg.RectNode (pos=(0,0), size=(2*(a/4.25), b), parent=self.divNode, color="000000", fillcolor="464646", fillopacity=1)
            
            breite = 2*(a/4.25)
            #On Start : 
            self.leute=[]
            self.leute.append(["Alexander", "0"])
            self.leute.append(["Pascal", "0"])
            self.leute.append(["Antonio", "0"])
            
            self.divNode1=avg.DivNode(pos=(50,0), size=((breite/3),b-50),parent=self.divNode)
            self.erster=avg.RectNode(pos=(50,b/1.3), size=(30,5), parent=self.divNode1, color="0489B1", fillcolor="2E9AFE", fillopacity=1)
            self.ersterName=avg.WordsNode(pos=(15,b/1.25), text=" " ,parent=self.divNode1, font='arial', color="6E6E6E", fontsize=20)
            self.ersterName.text=self.leute[0][0]
            
            self.divNode2=avg.DivNode(pos=((breite/2.5),0), size=((breite/2.5),b-50),parent=self.divNode)
            self.zweiter=avg.RectNode(pos=(50,b/1.3), size=(30,5), parent=self.divNode2, color="0489B1", fillcolor="2E9AFE", fillopacity=1)
            self.zweiterName=avg.WordsNode(pos=(30,b/1.25), text=" " ,parent=self.divNode2, font='arial', color="6E6E6E", fontsize=20)
            self.zweiterName.text=self.leute[1][0]
            
            self.divNode3=avg.DivNode(pos=((breite-(breite/3.5)),0), size=((breite/3.5),b-50),parent=self.divNode)
            self.dritter=avg.RectNode(pos=(50, b/1.3), size=(30,5), parent=self.divNode3, color="0489B1", fillcolor="2E9AFE",fillopacity=1)      
            self.dritterName=avg.WordsNode(pos=(35,b/1.25), text=" " ,parent=self.divNode3, font='arial', color="6E6E6E", fontsize=20)
            self.dritterName.text=self.leute[2][0]
            
        def recievedpunkte(arrayuser,null): 
                                     
            neueLeute=arrayuser
            
            if neueLeute[0][0]==" ":
                pass
            
            elif neueLeute==self.leute:
                pass
            
                
            elif neueLeute [0][0]!=" " and neueLeute [1][0]==" " and neueLeute [2][0]==" ":
                
                PunkteErster = neueLeute[0][1]
                NameErster = neueLeute[0][0]
                PunkteErster = float(PunkteErster)
            
                PunkteZweiter = self.leute[0][1]
                NameZweiter = self.leute[0][0]
                PunkteZweiter = float(PunkteZweiter)
            
                PunkteDritter = self.leute[1][1]
                NameDritter = self.leute[1][0]
                PunkteDritter = float(PunkteDritter)
                
                neueLeute[1]=self.leute[0]
                
            
            
                if PunkteErster ==0:
                    PunkteErster=5
                    balkenpos=b/1.3
                    Hundertprozent = 5
                else:
                    balkenpos=50
                    Hundertprozent=b-250
                
                Punktezweiter = 5
                Punktedritter = 5
                breite = 2*(a/4.25)
            
            
            elif neueLeute [0][0]!=" " and neueLeute [1][0]!=" " and neueLeute [2][0]==" ":
                
                PunkteErster = neueLeute[0][1]
                NameErster = neueLeute[0][0]
                PunkteErster = float(PunkteErster)
            
                PunkteZweiter = neueLeute[1][1]
                NameZweiter = neueLeute [1][0]
                PunkteZweiter = float(PunkteZweiter)
            
                PunkteDritter = self.leute[0][1]
                NameDritter = self.leute[0][0]
                PunkteDritter = float(PunkteDritter)
                
                neueLeute[2]=self.leute[0]
            
            
                if PunkteErster ==0:
                    PunkteErster=5
                    balkenposy=b/1.3
                    Hundertprozent = 5
                    Punktezweiter = 5
                    Punktedritter = 5
                else:
                    balkenposy=50
                    Hundertprozent=b-250
                    Punktezweiter = (Hundertprozent/PunkteErster)*PunkteZweiter
                    Punktedritter = (Hundertprozent/PunkteErster)*PunkteDritter
                breite = 2*(a/4.25)          
                
            
            else:
                PunkteErster = neueLeute[0][1]
                NameErster = neueLeute[0][0]
                PunkteErster = float(PunkteErster)
             
                PunkteZweiter = neueLeute[1][1]
                NameZweiter = neueLeute[1][0]
                PunkteZweiter = float(PunkteZweiter)
             
                PunkteDritter = neueLeute[2][1]
                NameDritter = neueLeute[2][0]
                PunkteDritter = float(PunkteDritter)

                if PunkteErster ==0:
                    PunkteErster=5
                    balkenposy=b/1.3
                    Hundertprozent = 5
                    Punktezweiter = 5
                    Punktedritter = 5
                else:
                    balkenposy=50
                    Hundertprozent=b-250
                    Punktezweiter = (Hundertprozent/PunkteErster)*PunkteZweiter
                    Punktedritter = (Hundertprozent/PunkteErster)*PunkteDritter
                
                breite = 2*(a/4.25)
                
                
                
            #Erster der neuen Liste nicht in alter Liste
            if Suchen(self.leute, neueLeute[0][0])== -1 :
                self.dritter.pos=(50,balkenposy)
                self.dritter.size=(30, Hundertprozent)
                self.dritterName.pos=(35,b/1.25)
                self.dritterName.text=NameErster
                
                TauschenDIV(self.divNode2, self.divNode3, breite/2.5, breite-(breite/3.5))    #Tausch vin dritter zu zweiter    
                time.sleep(5)     
                TauschenDIV(self.divNode3, self.divNode1, breite/2.5, 50) #Tausch vom neuen zweiten zum ersten
                
                time.sleep(5)
                
                SetzenimArray(self.leute, neueLeute[0][0], neueLeute[0][1])
                TauschenimArray(self.leute, 1, 2)                
                TauschenimArray(self.leute, 0, 1)
                
                self.divNode1.pos = (50,0) 
                self.erster.pos=(50,balkenposy) 
                self.erster.size=(30,Hundertprozent)
                self.ersterName.pos=(15,b/1.25)
                self.ersterName.text=self.leute[0][0]
               
            
                self.divNode2.pos = (breite/2.5, 0)
                self.zweiter.pos=(50,b/1.3)
                self.zweiter.size=(30,5)
                self.zweiterName.pos=(30,b/1.25)
                self.zweiterName.text=self.leute[1][0]
             
            
                self.divNode3.pos = (breite-(breite/3.5),0)
                self.dritter.pos=(50,b/1.3)      
                self.dritter.size=(30,5)
                self.dritterName.pos=(35,b/1.25)
                self.dritterName.text=self.leute[2][0]

                
            #Erster schon in der Liste 
            else :
                i = Suchen(self.leute, neueLeute[0][0])
                if i == 2:
                    self.dritter.pos=(50,50)
                    self.dritter.size=(30,Hundertprozent)
                    TauschenDIV(self.divNode2, self.divNode3, breite/2.5, breite-(breite/3.5))     
                    time.sleep(5)           
                    TauschenDIV(self.divNode3, self.divNode1, breite/2.5, 0)
                    self.leute[2][1] = neueLeute[2][1]
                    TauschenimArray(self.leute, 1, 2)                
                    TauschenimArray(self.leute, 0, 1)
                    
                    time.sleep(5)
                    
                    self.divNode1.pos = (50,0) 
                    self.erster.pos=(50,b/1.3) 
                    self.erster.size=(30,Hundertprozent)
                    self.ersterName.text=self.leute[0][0]
                    print self.erster.pos
            
                    self.divNode2.pos = (breite/2.5, 0)
                    self.zweiter.pos=(50,b/1.3)
                    self.zweiter.size=(30,5)
                    self.zweiterName.text=self.leute[1][0]
            
                    self.divNode3.pos = (breite-(breite/3.5),0)
                    self.dritter.pos=(50,b/1.3)      
                    self.dritter.size=(30,5)
                    self.dritterName.text=self.leute[2][0]
                    
                    
                elif i ==1:
                    self.zweiter.pos=(50,50)
                    self.zweiter.size=(30,Hundertprozent)
                    TauschenDIV(self.divNode2, self.divNode1, breite/2.5, 50)
                    self.leute[1][1] = neueLeute[1][1]
                    TauschenimArray(self.leute, 0, 1)
                    
                    time.sleep(5)
                    
                    self.divNode1.pos = (50,0) 
                    self.erster.pos=(50,b/1.3) 
                    self.erster.size=(30,Hundertprozent)
                    self.ersterName.text=self.leute[0][0]
            
                    self.divNode2.pos = (breite/2.5, 0)
                    self.zweiter.pos=(50,b/1.3)
                    self.zweiter.size=(30,5)
                    self.zweiterName.text=self.leute[1][0]
                    
                    
                else:
                    self.erster.pos=(50,b/1.3)
                    self.erster.size=(30,Hundertprozent)
                    self.leute[0][1] = neueLeute[0][1]
                    
                    
            time.sleep(2)
            
            #Zwite Person noch nicht in der Liste
            if Suchen(self.leute, neueLeute[1][0])== -1 :
                
                self.dritter.pos= (50,50+(b-250)-Punktezweiter)
                self.dritter.size=(30,Punktezweiter)
                self.dritterName.text=NameZweiter
                
                TauschenDIV(self.divNode3, self.divNode2, breite-(breite/3.5), breite/2.5)
                
                SetzenimArray(self.leute, neueLeute[1][0], neueLeute[1][1])   
                TauschenimArray(self.leute, 1, 2)
                
                time.sleep(5)
            
                self.divNode2.pos = (breite/2.5, 0)
                self.zweiter.pos=(50,50+(b-250)-Punktezweiter)
                self.zweiter.size=(30,Punktezweiter)
                self.zweiterName.text=self.leute[1][0]
            
                self.divNode3.pos = (breite-(breite/3.5),0)
                self.dritter.pos=(50,b/1.3)      
                self.dritter.size=(30,5)
                self.dritterName.text=self.leute[2][0]
                
                
            #Zweite Person schon in Liste      
            else :
                i = Suchen(self.leute, neueLeute[1][0])
                if i == 2:
                    self.dritter.pos=(50,50+(b-250)-Punktezweiter)
                    self.dritter.size=(30,Punktezweiter)
                    TauschenDIV(self.divNode2, self.divNode3, breite/2.5, breite-(breite/3.5))
                    self.leute[2][1] = neueLeute[2][1]
                    TauschenimArray(self.leute, 1, 2)       
                    
                    time.sleep(5)
            
                    self.divNode2.pos = (breite/2.5, 0)
                    self.zweiter.pos=(50,50+(b-250)-Punktezweiter)
                    self.zweiter.size=(30,Punktezweiter)
                    self.zweiterName.text=self.leute[1][0]
            
                    self.divNode3.pos = (breite-(breite/3.5),0)
                    self.dritter.pos=(50,b/1.3)      
                    self.dritter.size=(30,5)
                    self.dritterName.text=self.leute[2][0] 
                        
                else:
                    self.zweiter.pos=(50,50+(b-250)-Punktezweiter)
                    self.zweiter.size=(30,Punktezweiter)
                    self.leute[1][1] = neueLeute[1][1]
                    
            time.sleep(2)
            #Dritter noch nicht in Liste
            if Suchen(self.leute, neueLeute[2][0])== -1 :
                    
                self.dritter.pos= (50,50+(b-250)-Punktedritter)
                self.dritter.size=(30,Punktedritter)
                self.dritterName.text=NameDritter
                    
                SetzenimArray(self.leute, neueLeute[2][0], neueLeute[2][1])   
                #Dritter in Liste
            else:
                self.dritter.pos= (50,50+(b-250)-Punktedritter)
                self.dritter.size=(30,Punktedritter)
                SetzenimArray(self.leute, neueLeute[2][0], neueLeute[2][1])  
                


        def builtArrayOutOfString(rcvstring): 

            print rcvstring
        
            stringinput = rcvstring.split("!#!")
            stringarray=[]

            ArrayLen = len(stringinput)
            print ArrayLen
            
            if (ArrayLen ==7):
                for i in range(0,ArrayLen):
                    string = stringinput[i]
                    string2 = string.split("##")
                    stringarray.append([string2[0],string2[1],string2[2]]) ##Interpret , Titel, Votes
                print stringarray
                return stringarray
            if (ArrayLen==3):
                for i in range(0,ArrayLen):
                    string = stringinput[i]
                    string2 = string.split("##")
                    stringarray.append([string2[0],string2[1]]) ##Interpret , Titel, Votes
                print stringarray
                return stringarray
            
            print "Falschen String erhalten"
            
        def checkLenArray(str_builtArrayOutofString):
             
            ArrayLen=len(str_builtArrayOutofString)
             
            if (ArrayLen == 7):
#                 initializeDivs (str_builtArrayOutofString)
                thread.start_new_thread(updateRanking,(str_builtArrayOutofString,0))
            
            elif (ArrayLen==3):
                thread.start_new_thread(recievedpunkte,(str_builtArrayOutofString,0))
            
            else: 
                print "falsches Array gebaut"
                   
            
            
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
            while seconds >= 0:
                (mint,sect)=secsToMs(seconds)
                if int(sect) < 10 and int (mint)<10:
                    self.timer.text="Countdown "+"0"+mint+":" +"0"+sect 
                elif int(sect) <10:
                    self.timer.text="Countdown "+mint+":"+"0"+sect
                elif int(mint) <10:
                    self.timer.text="Countdown "+"0"+mint+":"+sect    
                else: 
                    self.timer.text="Countdown " + mint + ":" + sect
                time.sleep(1)
                seconds -= 1
                if seconds ==-1:
                    seconds = 3599
                    '''Top3Anim(self.div1, self.div2, self.div3, 
                             self.platz1a, self.platz2a, self.platz3a, 
                             self.platz1a.fontsize, self.platz2a.fontsize, self.platz3a.fontsize, 
                             self.div1.pos, self.div2.pos, self.div3.pos,
                             self.platz1b, self.platz2b, self.platz3b, 
                             self.platz1b.pos, self.platz2b.pos, self.platz3b.pos,
                             self.platz1b.fontsize, self.platz2b.fontsize, self.platz3b.fontsize,
                             self.div4, self.div5, self.div6, self.div7,
                             self.ranking,
                             self.platz1c, self.platz2c, self.platz3c,
                             self.title, self.votes)'''
                    
        
        def initializeWebSocket():##Starts the WebSocket
            log.startLogging(sys.stdout)
            self.receiver = WebSocketClientFactory("ws://localhost:9034", debug = False)
            self.receiver.protocol=MessageBasedHashClientProtocol
            connectWS(self.receiver)
            a="websocket ok"
            print a
            reactor.run(installSignalHandlers=0)##"installSignalHandlers=0" Necessary for Multithreading 
        
        left()
        right()
#         thread.start_new_thread(countdown,(0,5))
#         string = ("Pascal##460!#!Alexander##210!#!Rebecca##60")
#         checkLenArray(builtArrayOutOfString(string))
        
        thread.start_new_thread(initializeWebSocket,()) ##start the WebSocket in new Thread
        #time.sleep(2)
        #neu = [['Silbermond', 'Nichts passiert', '7'], ['Juli', 'Gute Zeit', '6'], ['Nickelback', 'Silver side up', '5'], ['Citizens', 'True Romance', '4'], 
        #      ['Sportfreunde Stiller', 'Applaus Applaus', '3'], ['Will.I.am', 'Scream and Shout', '2'], ['Justin Timberlake', 'Mirrors', '1']]
#         neu = [['Silbermond', 'Nichts passiert','7'],['Lady Gaga','Fraukegirl','89'],['Babapapa','Braunbaer','70'],['Gustav','Die Enten','55'],
#                ['Lausebub','Fruehling','40'],['Antonio','Krueger','30'],['Blue','Scheisse','20'],['Mandarin','Mandarin','3']]
#         neu = [['Silbermond', 'Nichts passiert', '100'], ['Juli', 'Gute Zeit', '88'], ['Nickelback', 'Silver side up', '77'], ['Citizens', 'True Romance', '50'], 
#               ['Sportfreunde Stiller', 'Applaus Applaus', '43'], ['Will.I.am', 'Scream and Shout', '23'], ['Justin Timberlake', 'Mirrors', '12']]
#         thread.start_new_thread(updateRanking, (neu,  0))
#         checkLenArray(neu) #TEST
#         thread.start_new_thread(fadeAnimSongsNormal, (neu, 0))
            
        class MessageBasedHashClientProtocol(WebSocketClientProtocol):

            def sendClientName(self):
                data = "PYCLIENT: "
                self.sendMessage(data, binary = True)
                print data
     
            def onOpen(self):
                self.sendClientName()
                print "Clientname gesendet"
#                 self.sendTestString ()
#                 print "AddSong zum Server gesendet"
    
            def onMessage(self, message, binary):
                print "Nachricht erhalten"
#                  self.messagetest="Gabi##900!#!Ralf##700!#!Marcel##300"
#                  self.messagetest="Silbermond##Nichts passiert##7!#!Juli##Gute Zeit##6!#!Nickelback##Silver side up##5!#!Citizens##True Romance##4!#!Sportfreunde Stiller##Applaus Applaus##3!#!Will.I.am##Scream and Shout##2!#!Justin Timberlake##Mirrors##1"
#                 self.messagetest="START"
                print message
                if (message=="START"):
                    global countvar
                    countvar=thread.start_new_thread(countdown,(0,2))

                else:
                    checkLenArray(builtArrayOutOfString(message))                            
                print "receivestring ausgefuehrt"
        
        
if __name__=='__main__':
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    screen.start(resolution=(screensize[0], screensize[1]))
  

