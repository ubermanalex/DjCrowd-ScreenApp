'''
Created on 03.07.2013

@author: Norine Coenen
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
        
        #aktuelle IP des Servers
        #serverip = "192.168.2.111" #kirstin
        #serverip = "192.168.2.110" #alex
        serverip = "localhost"
       
        #Variablen fuer die Animationsdauer
        timeFade = 1
        timeAnim = timeFade *1000
        
        #Wert fuer die maximale Animationsdauer des Rankings, sodass die einzelnen Aenderungen animiert werden (in Sekunden)
        maxAnimationDauer = 15 
        
        (a,b) = parentNode.size     #aufloesung
        #Startet im Fullscreen-Modus
        #player.setResolution(True,int(a),int(b),32)
        canvas = player.createMainCanvas(size=(a,b)) #canvas kreieren
        self.rootNode = canvas.getRootNode()
        self.back = avg.RectNode (pos=(0,0), size=(a,b), parent=self.rootNode, color="000000", fillcolor="3D4163", fillopacity=1)
        if int(a)<=1024:
            self.z= int (a-(a/2.5))
        else:
            self.z = int (a-(a/3.0)) #(3.5 bei 1440 x 900) #(3.0 bei 1280x800)
        self.title=avg.WordsNode (pos=(a/30,0),font="marketing script", variant="Bold", text="DjCrowd", color="E9EBFF", fontsize=55, alignment="left", parent=self.rootNode) 
        self.logog=avg.ImageNode (href="logodj100pxpng.png", pos=(((a/2)-100),0),parent=self.rootNode)
        self.timer=avg.WordsNode (font="marketing script", variant="Bold", text="Countdown 60:00", color="E9EBFF", fontsize=55, indent=self.z, parent=self.rootNode)
        
        #Initialisiert die linke Haelfte des Bildschirms
        def left():
            
            #Initaialisierung des Vergleichsarrays fuer das Ranking
            self.alteOrdnung = [] 
            self.alteOrdnung.append(["-1-", "-1-", "0"])
            self.alteOrdnung.append(["-2-", "-2-", "0"])
            self.alteOrdnung.append(["-3-", "-3-", "0"])
            self.alteOrdnung.append(["-4-", "-4-", "0"])
            self.alteOrdnung.append(["-5-", "-5-", "0"])
            self.alteOrdnung.append(["-6-", "-6-", "0"])
            self.alteOrdnung.append(["-7-", "-7-", "0"])
            
            middle=a/2.5+10
            
            self.divNode=avg.DivNode(pos=(0,(b/11)), size=(3*(a/5),b-50),parent=self.rootNode) #b-50
            
            #Divs fuer das Ranking
            self.ranking1=avg.WordsNode (pos=(a/30,int(b/6)),font="arial", variant="Bold", width=40, height= (b-50),text="1.", color="E9EBFF", fontsize=30, parent=self.rootNode)
            self.ranking2=avg.WordsNode (pos=(a/30,int(b/3.5175)),font="arial", variant="Bold", width=40, height= (b-50),text="2.", color="E9EBFF", fontsize=30, parent=self.rootNode)
            self.ranking3=avg.WordsNode (pos=(a/30,int(b/2.495)),font="arial", variant="Bold", width=40, height= (b-50),text="3." , color="E9EBFF", fontsize=30, parent=self.rootNode)
            self.ranking4=avg.WordsNode (pos=(a/30,int(b/1.935)),font="arial", variant="Bold", width=40, height= (b-50),text="4.", color="E9EBFF", fontsize=30, parent=self.rootNode)
            self.ranking5=avg.WordsNode (pos=(a/30,int(b/1.58)),font="arial", variant="Bold", width=40, height= (b-50),text="5.", color="E9EBFF", fontsize=30, parent=self.rootNode)
            self.ranking6=avg.WordsNode (pos=(a/30,int(b/1.335)),font="arial", variant="Bold", width=40, height= (b-50),text="6.", color="E9EBFF", fontsize=30, parent=self.rootNode)
            self.ranking7=avg.WordsNode (pos=(a/30,int(b/1.155)),font="arial", variant="Bold", width=40, height= (b-50),text="7.", color="E9EBFF", fontsize=30, parent=self.rootNode)
            
            #Grundgeruest fuer die linke Seite
            self.leftr=avg.RectNode (pos=(0,0), size=(3*(a/5), b-50), parent=self.divNode, color="000000", fillcolor="464646",fillopacity=1)
            self.title=avg.WordsNode (pos=(int(a/5.5),0),font="marketing script", variant="Bold", text=" Top 7 Songs ", color="E9EBFF", fontsize=40, parent=self.divNode)
            self.votes=avg.WordsNode (pos=(int(a/2-80),0),font="marketing script", variant="Bold", text="Votes", color="E9EBFF", fontsize=40, parent=self.divNode)
            
            #Initialisierung der sieben Divs fuer die Plaetze mit ihren zugehoehrigen Wordsnodes 
            #(in platzXa steht der Titel des Liedes, in platzXb der Interpret und in platzXc die Anzahl der Votes)
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
            self.platz7a=avg.WordsNode (pos=(0,0),font="arial", variant="Bold", text=self.alteOrdnung[6][1], color="E9EBFF", fontsize=30, parent=self.div7)
            self.platz7b=avg.WordsNode (pos=(33,40),font="arial", variant="Bold", text=self.alteOrdnung[6][0], color="E9EBFF", fontsize=20, parent=self.div7)
            self.platz7c=avg.WordsNode (pos=(middle,0),font="arial", variant="Bold", text=self.alteOrdnung[6][2], color="E9EBFF", fontsize=30, parent=self.div7)
            
            
    #Deklaration aller noetigen Hilfsvariablen fuer die Animationen der linken Seite
        
        #sucht in der Vergleichsordnung, ob das gegebene Lied (Titel und Interpret) dort schon enthalten ist. 
        #Falls dies der Fall ist, wird die Position in der alten Ordnung zurueckgegeben, falls nicht, so wird 7 zurueckgegeben.
        def schonda (alteOrdnung, titel, interpret):
            i = 0
            while i < 7 :
                if alteOrdnung[i][1] == titel and alteOrdnung[i][0] == interpret:
                    return i
                i += 1
            return 7
        
        #Tauscht die Positionen der beiden uebergebenen Objekte (Divs aus dem Ranking) als Animation
        def swap (a, b): 
            def startAnim():
                animObj.start()
                
            posa = a.pos
            posb = b.pos
            animObj = ParallelAnim([LinearAnim(a, "pos", timeAnim, posa, posb),  
                                    LinearAnim(b, "pos", timeAnim, posb, posa)])
            player.setTimeout(0, startAnim)
            time.sleep(timeFade)
            
        #Tauscht die Farben der Wordsnodes von zwie Divs 
        def colswap (w1a, w1b, w1c, w2a, w2b, w2c): 
            col1 = w1a.color
            col2 = w2a.color
            w1a.color = col2
            w1b.color = col2
            w1c.color = col2
            w2a.color = col1
            w2b.color = col1
            w2c.color = col1
           
        #Tauscht die Divs der Songs wieder zurueck, damit anschliessend wieder mit den alten Bezeichnungen gearbeitet werden kann
        def TauschenSongDivs(div1, div2, arrayposition1, arrayposition2, platz1a, platz1b, platz1c, platz2a, platz2b, platz2c):
            #vertauscht die Positionen der beiden Divs
            pos1 = div1.pos
            pos2 = div2.pos
            div1.pos = pos2
            div2.pos = pos1
            
            #passt den Inhalt der Wordsnodes entsprechend des Tausches an
            platz1a.text = self.alteOrdnung[arrayposition1][1]
            platz1b.text = self.alteOrdnung[arrayposition1][0]
            platz1c.text = self.alteOrdnung[arrayposition1][2]
            
            platz2a.text = self.alteOrdnung[arrayposition2][1]
            platz2b.text = self.alteOrdnung[arrayposition2][0]
            platz2c.text = self.alteOrdnung[arrayposition2][2]
            
            #tauscht die Farben der Wordsnodes, sodass alles optisch aussieht, wie vor dem Tausch
            colswap(platz1a, platz1b, platz1c, platz2a, platz2b, platz2c)
           
        #Tauschen von Elementen im Array
        def TauschenArray(array, position1, position2):
            #speichert die Werte an der erten Position im Array zwischen
            interpret1 = array[position1][0]
            song1 = array[position1][1]
            votes1 = array[position1][2]
            
            #ueberschreibt die Werte an der ersten Position im Array mit denen an der zweiten Position
            array[position1][0] = array[position2][0]
            array[position1][1] = array[position2][1]
            array[position1][2] = array[position2][2]
            
            #ueberschreibt die Werte an der zweiten Position im Array mit den vorher zwischengespeicherten Werten von Position 1
            array[position2][0] = interpret1
            array[position2][1] = song1
            array[position2][2] = votes1
     
        #Animiert das Ersetzen des ersten Platzes und passt das Vergleichsarray an
        def div7setzen(neueOrdnung0, neueOrdnung1, neueOrdnung2):
            #blendet das aktuel letzte Lied aus
            fadeOut(self.platz7a, timeAnim)
            fadeOut(self.platz7b, timeAnim)
            fadeOut(self.platz7c, timeAnim)
            time.sleep(timeFade)
            
            #ueberschreibt den Text in den Wordsnodes von Div 7
            self.platz7a.text = neueOrdnung1
            self.platz7b.text = neueOrdnung0
            self.platz7c.text = neueOrdnung2
            
            #blendet das neue Lied wieder ganz unten ein
            fadeIn(self.platz7a, timeAnim)
            fadeIn(self.platz7b, timeAnim)
            fadeIn(self.platz7c, timeAnim)
            time.sleep(timeFade)
            
            #aktualisiert auch die Informationen im Vergleichsarray
            self.alteOrdnung[6][0] = neueOrdnung0
            self.alteOrdnung[6][1] = neueOrdnung1
            self.alteOrdnung[6][2] = neueOrdnung2
     
        #Tauscht das letzte mit dem vorletzen Lied (erst werden die Divs getauscht, dann die Farben und 
        #anschliessend wird das Vergleichsarray angepasst und die Divs werden zurueckgetauscht)
        def sevenSix():
            swap(self.div7, self.div6)
            colswap(self.platz6a, self.platz6b, self.platz6c, self.platz7a, self.platz7b, self.platz7c)
            time.sleep(0.1)
            TauschenArray(self.alteOrdnung, 5, 6)
            TauschenSongDivs(self.div6, self.div7, 5, 6, self.platz6a, self.platz6b, self.platz6c, self.platz7a, self.platz7b, self.platz7c)
           
        #Tauscht das sechste mit dem fuenften Lied (erst werden die Divs getauscht, dann die Farben und 
        #anschliessend wird das Vergleichsarray angepasst und die Divs werden zurueckgetauscht)  
        def sixFive():
            swap(self.div6, self.div5)
            colswap(self.platz5a, self.platz5b, self.platz5c, self.platz6a, self.platz6b, self.platz6c)
            time.sleep(0.1)
            TauschenArray(self.alteOrdnung, 4, 5)
            TauschenSongDivs(self.div5, self.div6, 4, 5, self.platz5a, self.platz5b, self.platz5c, self.platz6a, self.platz6b, self.platz6c)
         
        #Tauscht das fuenfte mit dem vierten Lied (erst werden die Divs getauscht, dann die Farben und 
        #anschliessend wird das Vergleichsarray angepasst und die Divs werden zurueckgetauscht)  
        def fiveFour(): 
            swap(self.div5, self.div4)
            colswap(self.platz4a, self.platz4b, self.platz4c, self.platz5a, self.platz5b, self.platz5c)
            time.sleep(0.1)
            TauschenArray(self.alteOrdnung, 3, 4)
            TauschenSongDivs(self.div4, self.div5, 3, 4, self.platz4a, self.platz4b, self.platz4c, self.platz5a, self.platz5b, self.platz5c)
          
        #Tauscht das vierte mit dem dritten Lied (erst werden die Divs getauscht, dann die Farben und 
        #anschliessend wird das Vergleichsarray angepasst und die Divs werden zurueckgetauscht) 
        def fourThree():
            swap(self.div4, self.div3)
            colswap(self.platz3a, self.platz3b, self.platz3c, self.platz4a, self.platz4b, self.platz4c)
            time.sleep(0.1)
            TauschenArray(self.alteOrdnung, 2, 3)
            TauschenSongDivs(self.div3, self.div4, 2, 3, self.platz3a, self.platz3b, self.platz3c, self.platz4a, self.platz4b, self.platz4c)
            
        #Tauscht das dritte mit dem zweiten Lied (erst werden die Divs getauscht, dann die Farben und 
        #anschliessend wird das Vergleichsarray angepasst und die Divs werden zurueckgetauscht)
        def threeTwo():
            swap(self.div3, self.div2)
            colswap(self.platz2a, self.platz2b, self.platz2c, self.platz3a, self.platz3b, self.platz3c)
            time.sleep(0.1)
            TauschenArray(self.alteOrdnung, 1, 2)
            TauschenSongDivs(self.div2, self.div3, 1, 2, self.platz2a, self.platz2b, self.platz2c, self.platz3a, self.platz3b, self.platz3c)
            
        #Tauscht das zweite mit dem ersten Lied (erst werden die Divs getauscht, dann die Farben und 
        #anschliessend wird das Vergleichsarray angepasst und die Divs werden zurueckgetauscht)
        def twoOne():
            swap(self.div2, self.div1)
            colswap(self.platz1a, self.platz1b, self.platz1c, self.platz2a, self.platz2b, self.platz2c)
            time.sleep(0.1)
            TauschenArray(self.alteOrdnung, 0, 1)
            TauschenSongDivs(self.div1, self.div2, 0, 1, self.platz1a, self.platz1b, self.platz1c, self.platz2a, self.platz2b, self.platz2c)
        
        #aktualisiert die Votezahl am uebergebenen Platz als Animation im Wordsnode und zusaetzlich im Vergliechsarray
        def aktualisiereVotes(position, wordsnode, neueVotes):
            #Animation auf dem Screen
            fadeOut(wordsnode, timeAnim)
            time.sleep(timeFade)
            wordsnode.text = neueVotes
            fadeIn(wordsnode, timeAnim)
            time.sleep(timeFade)
            
            #Anpassen des Vergleichsarrays
            self.alteOrdnung[position][2] = neueVotes
            time.sleep(0.1)
            
        #Funktion, die die Animation der Rankingaenderungen implementiert
        def updateRanking (neueOrdnung, null):  
            #verzoegert den Start der Animation, um Threadingprobleme zu verhindern                         
            time.sleep(0.5)
            
        #zuerst wird der erste Platz des Rankings animiert
            #prueft, ob das neue erste Lied schon im Ranking enthalten ist und gibt gegebenenfalls die Position zurueck, sonst 7
            where = schonda(self.alteOrdnung, neueOrdnung[0][1], neueOrdnung[0][0])
            #falls das Lied noch nicht im Ranking enthalten ist:
            if where == 7:
                #ersetzt den letzten Platz mit dem neuen Lied
                div7setzen(neueOrdnung[0][0], neueOrdnung[0][1], neueOrdnung[0][2])
                #und animiert dies dann bis an die erste Stelle
                sevenSix()
                sixFive()
                fiveFour()
                fourThree()
                threeTwo()
                twoOne()
            #falls das Lied schon im Ranking enthalten ist, wird geprueft, an welcher Stelle es sich befindet und entsprechend animiert
            else:
                #Lied befindet sich an letzer Stelle
                if where == 6: 
                    #aktualisert gegebenenfalls die Votes
                    if self.platz7c.text != neueOrdnung[0][2]:
                        aktualisiereVotes(6, self.platz7c, neueOrdnung[0][2])
                    #und animiert das Lied an die erste Stelle
                    sevenSix()
                    sixFive()
                    fiveFour()
                    fourThree()
                    threeTwo()
                    twoOne()
                #Lied befindet sich an der sechsten Stelle
                elif where == 5:
                    #aktualisert gegebenenfalls die Votes
                    if self.platz6c.text != neueOrdnung[0][2]:
                        aktualisiereVotes(5, self.platz6c, neueOrdnung[0][2])
                    #und animiert das Lied an die erste Stelle
                    sixFive()
                    fiveFour()
                    fourThree()
                    threeTwo()
                    twoOne()
                #Lied befindet sich an der fuenften Stelle
                elif where == 4:
                    #aktualisert gegebenenfalls die Votes
                    if self.platz5c.text != neueOrdnung[0][2]:
                        aktualisiereVotes(4, self.platz5c, neueOrdnung[0][2])
                    #und animiert das Lied an die erste Stelle
                    fiveFour()
                    fourThree()
                    threeTwo()
                    twoOne()
                #Lied befindet sich an der vierten Stelle
                elif where == 3:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz4c.text != neueOrdnung[0][2]:
                        aktualisiereVotes(3, self.platz4c, neueOrdnung[0][2])
                    #und animiert das Lied an die erste Stelle
                    fourThree()
                    threeTwo()
                    twoOne()
                #Lied befindet sich an der dritten Stelle
                elif where == 2:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz3c.text != neueOrdnung[0][2]: 
                        aktualisiereVotes(2, self.platz3c, neueOrdnung[0][2])
                    #und animiert das Lied an die erste Stelle
                    threeTwo()
                    twoOne()
                #Lied befindet sich an der zweiten Stelle
                elif where == 1:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz2c.text != neueOrdnung[0][2]:
                        aktualisiereVotes(1, self.platz2c, neueOrdnung[0][2])
                    #und animiert das Lied an die erste Stelle
                    twoOne()
                #Lied befindet sich bereits an der ersten Stelle
                elif where == 0:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz1c.text != neueOrdnung[0][2]:
                        aktualisiereVotes(0, self.platz1c, neueOrdnung[0][2])
            
        #Nun wird der zweite Platz gesetzt
            #prueft, ob das neue erste Lied schon im Ranking enthalten ist und gibt gegebenenfalls die Position zurueck, sonst 7 
            where2 = schonda(self.alteOrdnung, neueOrdnung[1][1], neueOrdnung[1][0])
            #falls das Lied noch nicht im Ranking enthalten ist:
            if where2 == 7:
                #ersetzt den letzten Platz mit dem neuen Lied
                div7setzen(neueOrdnung[1][0], neueOrdnung[1][1], neueOrdnung[1][2])
                #und animiert dies dann bis an die zweite Stelle
                sevenSix()
                sixFive()
                fiveFour()
                fourThree()
                threeTwo()
            #falls das Lied schon im Ranking enthalten ist, wird geprueft, an welcher Stelle es sich befindet und entsprechend animiert   
            else:
                #Lied befindet sich an letzer Stelle
                if where2 == 6:
                    #aktualisert gegebenenfalls die Votes
                    if self.platz7c.text != neueOrdnung[1][2]:
                        aktualisiereVotes(6, self.platz7c, neueOrdnung[1][2])
                    #und animiert das Lied an die zweite Stelle
                    sevenSix()
                    sixFive()
                    fiveFour()
                    fourThree()
                    threeTwo()
                #Lied befindet sich an der sechsten Stelle
                elif where2 == 5:
                    #aktualisert gegebenenfalls die Votes
                    if self.platz6c.text != neueOrdnung[1][2]:
                        aktualisiereVotes(5, self.platz6c, neueOrdnung[1][2])
                    #und animiert das Lied an die zweite Stelle
                    sixFive()
                    fiveFour()
                    fourThree()
                    threeTwo()
                #Lied befindet sich an fuenfter Stelle
                elif where2 == 4:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz5c.text != neueOrdnung[1][2]:
                        aktualisiereVotes(4, self.platz5c, neueOrdnung[1][2])
                    #und animiert das Lied an die zweite Stelle
                    fiveFour()
                    fourThree()
                    threeTwo()
                #Lied befindet sich an der vierten Stelle
                elif where2 == 3:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz4c.text != neueOrdnung[1][2]:
                        aktualisiereVotes(3, self.platz4c, neueOrdnung[1][2])
                    #und animiert das Lied an die zweite Stelle
                    fourThree()
                    threeTwo()
                #Lied befindet sich an der dritten Stelle
                elif where2 == 2:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz3c.text != neueOrdnung[1][2]:
                        aktualisiereVotes(2, self.platz3c, neueOrdnung[1][2])
                    #und animiert das Lied an die zweite Stelle
                    threeTwo()
                #Lied befindet sich bereits an der zweiten Stelle
                elif where2 == 1:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz2c.text != neueOrdnung[1][2]:
                        aktualisiereVotes(1, self.platz2c, neueOrdnung[1][2])
                        
        #Als naechstes folgt Platz 3
            #prueft, ob das neue erste Lied schon im Ranking enthalten ist und gibt gegebenenfalls die Position zurueck, sonst 7 
            where3 = schonda(self.alteOrdnung, neueOrdnung[2][1], neueOrdnung[2][0])
            #falls das Lied noch nicht im Ranking enthalten ist:
            if where3 == 7:
                #ersetzt den letzten Platz mit dem neuen Lied
                div7setzen(neueOrdnung[2][0], neueOrdnung[2][1], neueOrdnung[2][2])
                #und animiert dies dann bis an die dritte Stelle
                sevenSix()
                sixFive()
                fiveFour()
                fourThree()
            #falls das Lied schon im Ranking enthalten ist, wird geprueft, an welcher Stelle es sich befindet und entsprechend animiert   
            else:
                #Lied befindet sich an letzer Stelle
                if where3 == 6: 
                    #aktualisert gegebenenfalls die Votes
                    if self.platz7c.text != neueOrdnung[2][2]:
                        aktualisiereVotes(6, self.platz7c, neueOrdnung[2][2])
                    #und animiert das Lied an die dritte Stelle
                    sevenSix()
                    sixFive()
                    fiveFour()
                    fourThree()
                #Lied befindet sich an der sechsten Stelle
                elif where3 == 5:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz6c.text != neueOrdnung[2][2]:
                        aktualisiereVotes(5, self.platz6c, neueOrdnung[2][2])
                    #und animiert das Lied an die dritte Stelle
                    sixFive()
                    fiveFour()
                    fourThree()
                #Lied befindet sich an der fuenften Stelle
                elif where3 == 4:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz5c.text != neueOrdnung[2][2]:
                        aktualisiereVotes(4, self.platz5c, neueOrdnung[2][2])
                    #und animiert das Lied an die dritte Stelle
                    fiveFour()
                    fourThree()
                #Lied befindet sich an der vierten Stelle
                elif where3 == 3:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz4c.text != neueOrdnung[2][2]:
                        aktualisiereVotes(3, self.platz4c, neueOrdnung[2][2])
                    #und animiert das Lied an die dritte Stelle
                    fourThree()
                #Lied befindet sich bereits an der dritten Stelle
                elif where3 == 2:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz3c.text != neueOrdnung[2][2]:
                        aktualisiereVotes(2, self.platz3c, neueOrdnung[2][2])
                        
        #Nun betrachten wir den vierten Platz
            #prueft, ob das neue erste Lied schon im Ranking enthalten ist und gibt gegebenenfalls die Position zurueck, sonst 7 
            where4 = schonda(self.alteOrdnung, neueOrdnung[3][1], neueOrdnung[3][0])
            #falls das Lied noch nicht im Ranking enthalten ist:
            if where4 == 7:
                #ersetzt den letzten Platz mit dem neuen Lied
                div7setzen(neueOrdnung[3][0], neueOrdnung[3][1], neueOrdnung[3][2])
                #und animiert dies dann bis an die vierte Stelle
                sevenSix()
                sixFive()
                fiveFour()
            #falls das Lied schon im Ranking enthalten ist, wird geprueft, an welcher Stelle es sich befindet und entsprechend animiert   
            else:
                #Lied befindet sich an letzer Stelle
                if where4 == 6:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz7c.text != neueOrdnung[3][2]:
                        aktualisiereVotes(6, self.platz7c, neueOrdnung[3][2])
                    #und animiert das Lied an die vierte Stelle
                    sevenSix()
                    sixFive()
                    fiveFour()
                #Lied befindet sich an der sechsten Stelle
                elif where4 == 5:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz6c.text != neueOrdnung[3][2]:
                        aktualisiereVotes(5, self.platz6c, neueOrdnung[3][2])
                    #und animiert das Lied an die vierte Stelle
                    sixFive()
                    fiveFour()
                #Lied befindet sich an der fuenften Stelle
                elif where4 == 4:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz5c.text != neueOrdnung[3][2]:
                        aktualisiereVotes(4, self.platz5c, neueOrdnung[3][2])
                    #und animiert das Lied an die vierte Stelle
                    fiveFour()
                #Lied befindet sich bereits an der vierten Stelle
                elif where4 == 3:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz4c.text != neueOrdnung[3][2]:
                        aktualisiereVotes(3, self.platz4c, neueOrdnung[3][2])
          
        #Es folgt die Animation fuer den fuenften Platz
            #prueft, ob das neue erste Lied schon im Ranking enthalten ist und gibt gegebenenfalls die Position zurueck, sonst 7 
            where5 = schonda(self.alteOrdnung, neueOrdnung[4][1], neueOrdnung[4][0])
            #falls das Lied noch nicht im Ranking enthalten ist:
            if where5 == 7:
                #ersetzt den letzten Platz mit dem neuen Lied
                div7setzen(neueOrdnung[4][0], neueOrdnung[4][1], neueOrdnung[4][2])
                #und animiert dies dann bis an die fuenfte Stelle
                sevenSix()
                sixFive()
            #falls das Lied schon im Ranking enthalten ist, wird geprueft, an welcher Stelle es sich befindet und entsprechend animiert   
            else:
                #Lied befindet sich an letzer Stelle
                if where5 == 6: #testen ob interpret gleich und votes aktualisiern
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz7c.text != neueOrdnung[4][2]:
                        aktualisiereVotes(6, self.platz7c, neueOrdnung[4][2])
                    #und animiert dies dann bis an die fuenfte Stelle
                    sevenSix()
                    sixFive()
                #Lied befindet sich an der sechsten Stelle
                elif where5 == 5:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz6c.text != neueOrdnung[4][2]:
                        aktualisiereVotes(5, self.platz6c, neueOrdnung[4][2])
                    #und animiert dies dann bis an die fuenfte Stelle
                    sixFive()
                #Lied befindet sich bereits an der fuenften Stelle
                elif where5 == 4:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz5c.text != neueOrdnung[4][2]:
                        aktualisiereVotes(4, self.platz5c, neueOrdnung[4][2])
            
        #Nun betrachten wir die Animation, die den sechsten Platz aktualisiert
            #prueft, ob das neue erste Lied schon im Ranking enthalten ist und gibt gegebenenfalls die Position zurueck, sonst 7 
            where6 = schonda(self.alteOrdnung, neueOrdnung[5][1], neueOrdnung[5][0])
            #falls das Lied noch nicht im Ranking enthalten ist:
            if where6 == 7:
                #ersetzt den letzten Platz mit dem neuen Lied
                div7setzen(neueOrdnung[5][0], neueOrdnung[5][1], neueOrdnung[5][2])
                #und animiert dies dann bis an die sechste Stelle
                sevenSix()
            #falls das Lied schon im Ranking enthalten ist, wird geprueft, an welcher Stelle es sich befindet und entsprechend animiert   
            else:
                #Lied befindet sich an letzer Stelle
                if where6 == 6: 
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz7c.text != neueOrdnung[5][2]:
                        aktualisiereVotes(6, self.platz7c, neueOrdnung[5][2])
                    #und animiert dies dann bis an die fuenfte Stelle
                    sevenSix()
                #Lied befindet sich bereits an der sechsten Stelle
                elif where6 == 5:
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz6c.text != neueOrdnung[5][2]:
                        aktualisiereVotes(5, self.platz6c, neueOrdnung[5][2])
                        
        #Es fehlt noch die Animation fuer den letzten Platz
            #prueft, ob das neue erste Lied schon im Ranking enthalten ist und gibt gegebenenfalls die Position zurueck, sonst 7 
            where7 = schonda(self.alteOrdnung, neueOrdnung[6][1], neueOrdnung[6][0])
            #falls das Lied noch nicht im Ranking enthalten ist:
            if where7 == 7:
                #ersetzt den letzten Platz mit dem neuen Lied
                div7setzen(neueOrdnung[6][0], neueOrdnung[6][1], neueOrdnung[6][2])
                #hier muss nichts animiert werden, da sich das Lied nach der Initaialisierung bereits an der richtigen Stelle befindet
            #falls das Lied schon im Ranking enthalten ist, wird geprueft, an welcher Stelle es sich befindet und entsprechend animiert   
            else:
                #Lied befindet sich bereits an letzer Stelle
                if where7 == 6: 
                    #aktualisiert gegebenenfalls die Votes
                    if self.platz7c.text != neueOrdnung[6][2]:
                        aktualisiereVotes(6, self.platz7c, neueOrdnung[6][2])
            
        #Falls die Animation der Lieder zu lange dauert, wird diese Funktion aufgerufen. 
        #Es werden alle sieben Lieder ausgefadet und mit der neuen Liste initialisiert wieder eingeblendet.  
        def fadeAnimSongsNormal (neueOrdnung, null):
            time.sleep(0.1)
            
            #Ausblenden der sieben Lied-Divs
            fadeOut(self.div1, timeAnim)
            fadeOut(self.div2, timeAnim)
            fadeOut(self.div3, timeAnim)
            fadeOut(self.div4, timeAnim)
            fadeOut(self.div5, timeAnim)
            fadeOut(self.div6, timeAnim)
            fadeOut(self.div7, timeAnim)
            time.sleep(timeFade)
            
            #Ueberschreiben der Informationen in den Wordsnodes der sieben Lied-Divs mit den Werten der neuen Rangliste
            #Setzen der neuen Titel
            self.platz1a.text= neueOrdnung[0][1]
            self.platz2a.text= neueOrdnung[1][1]
            self.platz3a.text= neueOrdnung[2][1]
            self.platz4a.text= neueOrdnung[3][1]
            self.platz5a.text= neueOrdnung[4][1]
            self.platz6a.text= neueOrdnung[5][1]
            self.platz7a.text= neueOrdnung[6][1]
            #Setzen der neuen Interpreten
            self.platz1b.text= neueOrdnung[0][0]
            self.platz2b.text= neueOrdnung[1][0]
            self.platz3b.text= neueOrdnung[2][0]
            self.platz4b.text= neueOrdnung[3][0]
            self.platz5b.text= neueOrdnung[4][0]
            self.platz6b.text= neueOrdnung[5][0]
            self.platz7b.text= neueOrdnung[6][0]
            #Setzen der neuen Votes
            self.platz1c.text= neueOrdnung[0][2]
            self.platz2c.text= neueOrdnung[1][2]
            self.platz3c.text= neueOrdnung[2][2]
            self.platz4c.text= neueOrdnung[3][2]
            self.platz5c.text= neueOrdnung[4][2]
            self.platz6c.text= neueOrdnung[5][2]
            self.platz7c.text= neueOrdnung[6][2]
            
            #Ueberschreiben des Vergleichsarrays mit dem neuen aktuellen Ranking
            self.alteOrdnung = deepcopy(neueOrdnung)
            
            #Erneutes Einblenden der aktualisierten Divs
            fadeIn(self.div1, timeAnim)
            fadeIn(self.div2, timeAnim)
            fadeIn(self.div3, timeAnim)
            fadeIn(self.div4, timeAnim)
            fadeIn(self.div5, timeAnim)
            fadeIn(self.div6, timeAnim)
            fadeIn(self.div7, timeAnim)
        
        #Simuliert die Animation der Liste und berechnet, wie lange die Animation dauern wuerde. Anschliessend waehlt es auf dieser Basis aus, 
        #ob die neue Liste animiert (updateRanking) oder eingeblendet (fadeAnimSongsNormal) wird 
        def animationUpdate (neueOrdnung):
        #Abfangen von Randfaellen
            #Es wurde noch nichts hinzugefuegt
            if neueOrdnung[0][0] == " " and neueOrdnung[0][1] == " " and neueOrdnung[1][0] == " " and neueOrdnung[1][1] == " " and neueOrdnung[2][0] == " " and neueOrdnung[2][1] == " " and neueOrdnung[3][0] == " " and neueOrdnung[3][1] == " " and neueOrdnung[4][0] == " " and neueOrdnung[4][1] == " " and neueOrdnung[5][0] == " " and neueOrdnung[5][1] == " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung = deepcopy(self.alteOrdnung)
            #Es befindet sich nur ein Lied in der Liste
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] == " " and neueOrdnung[1][1] == " " and neueOrdnung[2][0] == " " and neueOrdnung[2][1] == " " and neueOrdnung[3][0] == " " and neueOrdnung[3][1] == " " and neueOrdnung[4][0] == " " and neueOrdnung[4][1] == " " and neueOrdnung[5][0] == " " and neueOrdnung[5][1] == " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung[1][0] = "-1-"
                neueOrdnung[1][1] = "-1-"
                neueOrdnung[1][2] = "0"
                neueOrdnung[2][0] = "-2-"
                neueOrdnung[2][1] = "-2-"
                neueOrdnung[2][2] = "0"
                neueOrdnung[3][0] = "-3-"
                neueOrdnung[3][1] = "-3-"
                neueOrdnung[3][2] = "0"
                neueOrdnung[4][0] = "-4-"
                neueOrdnung[4][1] = "-4-"
                neueOrdnung[4][2] = "0"
                neueOrdnung[5][0] = "-5-"
                neueOrdnung[5][1] = "-5-"
                neueOrdnung[5][2] = "0"
                neueOrdnung[6][0] = "-6-"
                neueOrdnung[6][1] = "-6-"
                neueOrdnung[6][2] = "0"
            #Es wurden zwei Lieder uebergeben
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] != " " and neueOrdnung[1][1] != " " and neueOrdnung[2][0] == " " and neueOrdnung[2][1] == " " and neueOrdnung[3][0] == " " and neueOrdnung[3][1] == " " and neueOrdnung[4][0] == " " and neueOrdnung[4][1] == " " and neueOrdnung[5][0] == " " and neueOrdnung[5][1] == " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung[2][0] = "-1-"
                neueOrdnung[2][1] = "-1-"
                neueOrdnung[2][2] = "0"
                neueOrdnung[3][0] = "-2-"
                neueOrdnung[3][1] = "-2-"
                neueOrdnung[3][2] = "0"
                neueOrdnung[4][0] = "-3-"
                neueOrdnung[4][1] = "-3-"
                neueOrdnung[4][2] = "0"
                neueOrdnung[5][0] = "-4-"
                neueOrdnung[5][1] = "-4-"
                neueOrdnung[5][2] = "0"
                neueOrdnung[6][0] = "-5-"
                neueOrdnung[6][1] = "-5-"
                neueOrdnung[6][2] = "0"
            #Drei Lieder wurden uebergeben
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] != " " and neueOrdnung[1][1] != " " and neueOrdnung[2][0] != " " and neueOrdnung[2][1] != " " and neueOrdnung[3][0] == " " and neueOrdnung[3][1] == " " and neueOrdnung[4][0] == " " and neueOrdnung[4][1] == " " and neueOrdnung[5][0] == " " and neueOrdnung[5][1] == " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung[3][0] = "-1-"
                neueOrdnung[3][1] = "-1-"
                neueOrdnung[3][2] = "0"
                neueOrdnung[4][0] = "-2-"
                neueOrdnung[4][1] = "-2-"
                neueOrdnung[4][2] = "0"
                neueOrdnung[5][0] = "-3-"
                neueOrdnung[5][1] = "-3-"
                neueOrdnung[5][2] = "0"
                neueOrdnung[6][0] = "-4-"
                neueOrdnung[6][1] = "-4-"
                neueOrdnung[6][2] = "0"
            #Es befinden sich vier Lieder in der Argumentliste
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] != " " and neueOrdnung[1][1] != " " and neueOrdnung[2][0] != " " and neueOrdnung[2][1] != " " and neueOrdnung[3][0] != " " and neueOrdnung[3][1] != " " and neueOrdnung[4][0] == " " and neueOrdnung[4][1] == " " and neueOrdnung[5][0] == " " and neueOrdnung[5][1] == " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung[4][0] = "-1-"
                neueOrdnung[4][1] = "-1-"
                neueOrdnung[4][2] = "0"
                neueOrdnung[5][0] = "-2-"
                neueOrdnung[5][1] = "-2-"
                neueOrdnung[5][2] = "0"
                neueOrdnung[6][0] = "-3-"
                neueOrdnung[6][1] = "-3-"
                neueOrdnung[6][2] = "0"
            #fuenf Lieder als Eingabe
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] != " " and neueOrdnung[1][1] != " " and neueOrdnung[2][0] != " " and neueOrdnung[2][1] != " " and neueOrdnung[3][0] != " " and neueOrdnung[3][1] != " " and neueOrdnung[4][0] != " " and neueOrdnung[4][1] != " " and neueOrdnung[5][0] == " " and neueOrdnung[5][1] == " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung[5][0] = "-1-"
                neueOrdnung[5][1] = "-1-"
                neueOrdnung[5][2] = "0"
                neueOrdnung[6][0] = "-2-"
                neueOrdnung[6][1] = "-2-"
                neueOrdnung[6][2] = "0"
            #Es wurden sechs Lieder uebergeben
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] != " " and neueOrdnung[1][1] != " " and neueOrdnung[2][0] != " " and neueOrdnung[2][1] != " " and neueOrdnung[3][0] != " " and neueOrdnung[3][1] != " " and neueOrdnung[4][0] != " " and neueOrdnung[4][1] != " " and neueOrdnung[5][0] != " " and neueOrdnung[5][1] != " " and neueOrdnung[6][0] == " " and neueOrdnung[6][1] == " ":
                neueOrdnung[6][0] = "-1-"
                neueOrdnung[6][1] = "-1-"
                neueOrdnung[6][2] = "0"
            #Es wurde ein komplett volles Array uebergeben
            elif neueOrdnung[0][0] != " " and neueOrdnung[0][1] != " " and neueOrdnung[1][0] != " " and neueOrdnung[1][1] != " " and neueOrdnung[2][0] != " " and neueOrdnung[2][1] != " " and neueOrdnung[3][0] != " " and neueOrdnung[3][1] != " " and neueOrdnung[4][0] != " " and neueOrdnung[4][1] != " " and neueOrdnung[5][0] != " " and neueOrdnung[5][1] != " " and neueOrdnung[6][0] != " " and neueOrdnung[6][1] != " ":
                pass
                
            #Initialisierung der Animationsdauer, um anfaengliche Verzoegerungen auszugleichen         
            animationDauer = 3
            
            #Erstellung einer unabhaengig veraenderlichen Kopie der alten Vergleichsordnung, um die Animation zu simulieren und deren Dauer abschaetzen zu koennen
            kopie = deepcopy(self.alteOrdnung)
            
    #berechnet die Animationsdauer grob
        #Simulation der Animation fuer den ersten Platz
            #prueft ob, und wenn ja, wo sich das Lied bereits im Ranking befindet
            anzAnim1 = schonda(kopie, neueOrdnung[0][1], neueOrdnung[0][0]) 
            animationDauer += (anzAnim1 + 1) * timeFade #animationen und votes anpassung animation
            
            if anzAnim1 == 7: #nich in liste
                #arraykopie altes array anpassen
                kopie[6][0] = neueOrdnung[0][0]
                kopie[6][1] = neueOrdnung[0][1]
                kopie[6][2] = neueOrdnung[0][2]
                
                animationDauer -= 1 * timeFade #da votes nicht aktualisiert werden muessen
                
                TauschenArray (kopie, 5, 6)
                TauschenArray (kopie, 4, 5)
                TauschenArray (kopie, 3, 4)
                TauschenArray (kopie, 2, 3)
                TauschenArray (kopie, 1, 2)
                TauschenArray (kopie, 0, 1)
            elif anzAnim1 == 6: #platz 7
                TauschenArray (kopie, 5, 6)
                TauschenArray (kopie, 4, 5)
                TauschenArray (kopie, 3, 4)
                TauschenArray (kopie, 2, 3)
                TauschenArray (kopie, 1, 2)
                TauschenArray (kopie, 0, 1)
            elif anzAnim1 == 5: #platz 6
                TauschenArray (kopie, 4, 5)
                TauschenArray (kopie, 3, 4)
                TauschenArray (kopie, 2, 3)
                TauschenArray (kopie, 1, 2)
                TauschenArray (kopie, 0, 1)
            elif anzAnim1 == 4: #platz 5
                TauschenArray (kopie, 3, 4)
                TauschenArray (kopie, 2, 3)
                TauschenArray (kopie, 1, 2)
                TauschenArray (kopie, 0, 1)
            elif anzAnim1 == 3: #platz 4
                TauschenArray (kopie, 2, 3)
                TauschenArray (kopie, 1, 2)
                TauschenArray (kopie, 0, 1)
            elif anzAnim1 == 2: #platz 3
                TauschenArray (kopie, 1, 2)
                TauschenArray (kopie, 0, 1)
            elif anzAnim1 == 1: #platz 2
                TauschenArray (kopie, 0, 1)
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
                
                TauschenArray (kopie, 5, 6)
                TauschenArray (kopie, 4, 5)
                TauschenArray (kopie, 3, 4)
                TauschenArray (kopie, 2, 3)
                TauschenArray (kopie, 1, 2)
            elif anzAnim2 == 6: #platz 7
                TauschenArray (kopie, 5, 6)
                TauschenArray (kopie, 4, 5)
                TauschenArray (kopie, 3, 4)
                TauschenArray (kopie, 2, 3)
                TauschenArray (kopie, 1, 2)
            elif anzAnim2 == 5: #platz 6
                TauschenArray (kopie, 4, 5)
                TauschenArray (kopie, 3, 4)
                TauschenArray (kopie, 2, 3)
                TauschenArray (kopie, 1, 2)
            elif anzAnim2 == 4: #platz 5
                TauschenArray (kopie, 3, 4)
                TauschenArray (kopie, 2, 3)
                TauschenArray (kopie, 1, 2)
            elif anzAnim2 == 3: #platz 4
                TauschenArray (kopie, 2, 3)
                TauschenArray (kopie, 1, 2)
            elif anzAnim2 == 2: #platz 3
                TauschenArray (kopie, 1, 2)
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
                
                TauschenArray (kopie, 5, 6)
                TauschenArray (kopie, 4, 5)
                TauschenArray (kopie, 3, 4)
                TauschenArray (kopie, 2, 3)
            elif anzAnim3 == 6: #platz 7
                TauschenArray (kopie, 5, 6)
                TauschenArray (kopie, 4, 5)
                TauschenArray (kopie, 3, 4)
                TauschenArray (kopie, 2, 3)
            elif anzAnim3 == 5: #platz 6
                TauschenArray (kopie, 4, 5)
                TauschenArray (kopie, 3, 4)
                TauschenArray (kopie, 2, 3)
            elif anzAnim3 == 4: #platz 5
                TauschenArray (kopie, 3, 4)
                TauschenArray (kopie, 2, 3)
            elif anzAnim3 == 3: #platz 4
                TauschenArray (kopie, 2, 3)
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
                
                TauschenArray (kopie, 5, 6)
                TauschenArray (kopie, 4, 5)
                TauschenArray (kopie, 3, 4)
            elif anzAnim4 == 6: #platz 7
                TauschenArray (kopie, 5, 6)
                TauschenArray (kopie, 4, 5)
                TauschenArray (kopie, 3, 4)
            elif anzAnim4 == 5: #platz 6
                TauschenArray (kopie, 4, 5)
                TauschenArray (kopie, 3, 4)
            elif anzAnim4 == 4: #platz 5
                TauschenArray (kopie, 3, 4)
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
                
                TauschenArray (kopie, 5, 6)
                TauschenArray (kopie, 4, 5)
            elif anzAnim5 == 6: #platz 7
                TauschenArray (kopie, 5, 6)
                TauschenArray (kopie, 4, 5)
            elif anzAnim5 == 5: #platz 6
                TauschenArray (kopie, 4, 5)
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
                
                TauschenArray (kopie, 5, 6)
            elif anzAnim6 == 6: #platz 7
                TauschenArray (kopie, 5, 6)
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
                print "zu lang"
                thread.start_new_thread(fadeAnimSongsNormal, (neueOrdnung, 0)) #fadeanimation wird ausfefuehrt
            else:
                print "klappt"
#                 print self.alteOrdnung
#                 print kopie
                print neueOrdnung
                thread.start_new_thread(updateRanking, (neueOrdnung, 0)) #animation wird duchgefuehrt
  
             
             
        
        '''
            animationUpdate
            top3anim
            fadeanimsongstop3
            '''
           
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
            
            #altes array anpassen
            self.alteOrdnung = deepcopy(neueOrdnung)
           
            fadeIn(self.div1, timeAnim)
            fadeIn(self.div2, timeAnim)
            fadeIn(self.div3, timeAnim)
            fadeIn(self.div4, timeAnim)
            fadeIn(self.div5, timeAnim)
            fadeIn(self.div6, timeAnim)
            fadeIn(self.div7, timeAnim)
            #Ranking wieder einblenden
            fadeIn(self.ranking1, timeAnim)
            fadeIn(self.ranking2, timeAnim)
            fadeIn(self.ranking3, timeAnim)
            fadeIn(self.ranking4, timeAnim)
            fadeIn(self.ranking5, timeAnim)
            fadeIn(self.ranking6, timeAnim)
            fadeIn(self.ranking7, timeAnim)
            
            fadeIn(self.platz1c, timeAnim)
            fadeIn(self.platz2c, timeAnim)
            fadeIn(self.platz3c, timeAnim)
            
        
        def Top3Anim (number1div, number2div, number3div, number1titel, number2titel, number3titel, size1t, size2t, size3t, pos1div, pos2div, pos3div, 
                      number1inter, number2inter, number3inter, pos1inter, pos2inter, pos3inter, size1inter, size2inter, size3inter, 
                      div4, div5, div6, div7, ranking1, ranking2, ranking3, ranking4, ranking5, ranking6, ranking7, 
                      number1votes, number2votes, number3votes, top7, votes):
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
                                        
                                        #ranking ausfaden
                                        LinearAnim(ranking1, "opacity", 2000, 1, 0),
                                        LinearAnim(ranking2, "opacity", 2000, 1, 0), 
                                        LinearAnim(ranking3, "opacity", 2000, 1, 0),
                                        LinearAnim(ranking4, "opacity", 2000, 1, 0),
                                        LinearAnim(ranking5, "opacity", 2000, 1, 0),
                                        LinearAnim(ranking6, "opacity", 2000, 1, 0),
                                        LinearAnim(ranking7, "opacity", 2000, 1, 0),
                                        
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
            self.divNode=avg.DivNode(pos=(a-2*(a/4.25),(b/11)), size=(2*(a/4.25),b),parent=self.rootNode) #75
            self.rightr=avg.RectNode (pos=(0,0), size=(2*(a/4.25), b), parent=self.divNode, color="000000", fillcolor="464646", fillopacity=1)
            
            breite = 2*(a/4.25)
            #On Start : 
            self.leute=[]
            self.leute.append(["Alexander", "0"])
            self.leute.append(["Pascal", "0"])
            self.leute.append(["Antonio", "0"])
            
            self.divNode1=avg.DivNode(pos=(50,0), size=((breite/3),b-50),parent=self.divNode)
            self.erster=avg.RectNode(pos=(50,b/1.3), size=(30,5), parent=self.divNode1, color="0489B1", fillcolor="2E9AFE", fillopacity=1)
            self.ersterName=avg.WordsNode(pos=(30,b/1.25), text=" " ,parent=self.divNode1, font='arial', color="6E6E6E", fontsize=20)
            self.ersterName.text=self.leute[0][0]
            
            self.divNode2=avg.DivNode(pos=((breite/2.5),0), size=((breite/2.5),b-50),parent=self.divNode)
            self.zweiter=avg.RectNode(pos=(50,b/1.3), size=(30,5), parent=self.divNode2, color="0489B1", fillcolor="2E9AFE", fillopacity=1)
            self.zweiterName=avg.WordsNode(pos=(30,b/1.25), text=" " ,parent=self.divNode2, font='arial', color="6E6E6E", fontsize=20)
            self.zweiterName.text=self.leute[1][0]
            
            self.divNode3=avg.DivNode(pos=((breite-(breite/3.5)),0), size=((breite/3.5),b-50),parent=self.divNode)
            self.dritter=avg.RectNode(pos=(50, b/1.3), size=(30,5), parent=self.divNode3, color="0489B1", fillcolor="2E9AFE",fillopacity=1)      
            self.dritterName=avg.WordsNode(pos=(30,b/1.25), text=" " ,parent=self.divNode3, font='arial', color="6E6E6E", fontsize=20)
            self.dritterName.text=self.leute[2][0]
            
        def recievedpunkte(arrayuser,null): 
                                     
            neueLeute=arrayuser
            
            if neueLeute[0][0]==" " and neueLeute[1][0] == " " and neueLeute[2][0] == " ":
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
                neueLeute[2] = self.leute[1]
            
            
                if PunkteErster ==0:
                    PunkteErster=5
                    balkenposy=b/1.3
                    Hundertprozent = 5
                else:
                    balkenposy=50
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
                self.ersterName.text=self.leute[0][0]
               
            
                self.divNode2.pos = (breite/2.5, 0)
                self.zweiter.pos=(50,b/1.3)
                self.zweiter.size=(30,5)
                self.zweiterName.text=self.leute[1][0]
             
            
                self.divNode3.pos = (breite-(breite/3.5),0)
                self.dritter.pos=(50,b/1.3)      
                self.dritter.size=(30,5)
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
                self.zweiterName.pos=(30,b/1.25)
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
                    self.zweiterName.pos=(30,b/1.25)
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
                animationUpdate(str_builtArrayOutofString)
            
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
                    Top3Anim(self.div1, self.div2, self.div3, 
                             self.platz1a, self.platz2a, self.platz3a, 
                             self.platz1a.fontsize, self.platz2a.fontsize, self.platz3a.fontsize, 
                             self.div1.pos, self.div2.pos, self.div3.pos,
                             self.platz1b, self.platz2b, self.platz3b, 
                             self.platz1b.pos, self.platz2b.pos, self.platz3b.pos,
                             self.platz1b.fontsize, self.platz2b.fontsize, self.platz3b.fontsize,
                             self.div4, self.div5, self.div6, self.div7,
                             self.ranking1, self.ranking2, self.ranking3, self.ranking4, self.ranking5, self.ranking6, self.ranking7,
                             self.platz1c, self.platz2c, self.platz3c,
                             self.title, self.votes)
                    
        
        def initializeWebSocket():##Starts the WebSocket
            log.startLogging(sys.stdout)
            self.receiver = WebSocketClientFactory("ws://" + serverip + ":9034", debug = False)
            self.receiver.protocol=MessageBasedHashClientProtocol
            connectWS(self.receiver)
            a="websocket ok"
            print a
            reactor.run(installSignalHandlers=0)##"installSignalHandlers=0" Necessary for Multithreading 
        
        left()
        right()

        
        thread.start_new_thread(initializeWebSocket,()) ##start the WebSocket in new Thread

            
        class MessageBasedHashClientProtocol(WebSocketClientProtocol):

            def sendClientName(self):
                data = "PYCLIENT: "
                self.sendMessage(data, binary = True)
                #print data
     
            def onOpen(self):
                self.sendClientName()
                #print "Clientname gesendet"

    
            def onMessage(self, message, binary):
                print "Nachricht erhalten"
                print message
                if (message=="START"):
                    global countvar
                    countvar=thread.start_new_thread(countdown,(3,00))
                elif (message[:6] == 'PLAYED'):
                    fadeAnimSongsTop3(builtArrayOutOfString(message[6:]), 0)     
                elif (message[:6] == "PYMESG"):
                    checkLenArray(builtArrayOutOfString(message[6:]))
                                        
                #print "receivestring ausgefuehrt"
        
        
if __name__=='__main__':
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    screen.start(resolution=(screensize[0], screensize[1]))
  

