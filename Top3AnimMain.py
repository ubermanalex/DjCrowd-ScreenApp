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
            self.title=avg.WordsNode (pos=(75,0),font="arial", variant="Bold", text="Top 7 Songs", color="000000", fontsize=40, opacity = 1, parent=self.divNode)
            self.votes=avg.WordsNode (pos=(600,0),font="arial", variant="Bold", text="Votes", color="000000", fontsize=40, opacity = 1, parent=self.divNode)
            
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
                
                player.setTimeout(5000, topthreeanim)
        
        def Tauschen(a,b,AX,AY,BX,BY):
                def startAnim():
                    animObj.start()
        
                animObj1 = LinearAnim(a, "y", 2000, AY, BY)
                animObj2 = LinearAnim(b, "y", 2000, BY, AY)
                animList = (animObj2, animObj1)
                animObj = ParallelAnim(animList)

                player.setTimeout(2000, startAnim)      
            
            
        def right(): #rechts mit Balken
            self.divNode=avg.DivNode(pos=(a-2*(a/5),50), size=(2*(a/5),b-50),parent=self.rootNode)
            self.rightr=avg.RectNode (pos=(0,0), size=(2*(a/5), b-50), parent=self.divNode, color="F0F0F4", fillopacity=1)
            
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
        Tauschen(self.div1, self.div2, self.div1.x, self.div1.y, self.div2.x , self.div2.y)
        
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
                 self.title, self.votes)
        
        
        
  
        
if __name__=='__main__':
    screen.start(resolution=(1440, 900))   
  

