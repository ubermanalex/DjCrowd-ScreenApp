'''
Created on 12.06.2013

@author: Kirstin
'''
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
    stringarray.append(string2[0]+" "+"-"+" "+string2[1]+" "+string2[2])
print stringarray