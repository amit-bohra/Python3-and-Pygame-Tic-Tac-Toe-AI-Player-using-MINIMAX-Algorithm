from copy import deepcopy as dp
import pygame,sys,time
from pygame.locals import *
import random as rd
import itertools as it
import functools
import time
import os
import pickle

time1=time.time()

graph={'0*********0**0':{'1a********1h1a','1*a*******2h2a','1**a******3h3a',
        '1***a*****4h4a','1****a****5h5a','1*****a***6h6a',
        '1******a**7h7a','1*******a*8h8a','1********a9h9a'}}
graphlist={'0*********0**0':['1a********1h1a','1*a*******2h2a','1**a******3h3a',
        '1***a*****4h4a','1****a****5h5a','1*****a***6h6a',
        '1******a**7h7a','1*******a*8h8a','1********a9h9a']}
graphvalue={'0*********0**0':[]}

pinkyloop=False
if os.path.exists('graph.pickle'):
    with open('graph.pickle','rb') as f:
        graph=pickle.load(f)
        pinkyloop=True
        
def stringToList(string):
    level=None
    valuelist=[0,0,0,0,0,0,0,0,0]
    humpos={}
    compos={}
    nopos={}
    tries=None
    player=None
    playpos=None
    playval=None
    hwin=[]
    cwin=[]
    for i in range(len(string)):
        if i in range(1,10):
            if string[i] in ['a','b','c','d','e']:
                humpos[i]=string[i]
                valuelist[i-1]=1
            elif string[i] in ['A','B','C','D','E']:
                compos[i]=string[i]
                valuelist[i-1]=1
            else:
                nopos[i]=0
        else:
            if i==0:
                level=int(string[i])
            if i==10:
                tries=int(string[i])
            if i==11:
                player=string[i]
            if i==12:
                playpos=int(string[i])
            if i==13:
                playval=string[i]
    temp=len(humpos)+len(compos)+valuelist.count(0)
    if len(humpos.keys())>2:
        hwin=list(it.permutations(humpos,3))
    if len(compos.keys())>2:
        cwin=list(it.permutations(compos,3))
    if temp==9:
        return level,valuelist,humpos,compos,nopos,tries,player,playpos,playval,hwin,cwin


def listToString(level,valuelist,humpos,compos,nopos,tries,player,playpos,playval,hwin,cwin):
    temp=''
    humdict={1:'a',}
    for i in range(9):
        if valuelist[i]==1:
            if i+1 in humpos.keys():
                temp+=humpos[i+1]
            elif i+1 in compos.keys():
                temp+=compos[i+1]
        else:
            temp+='*'
    string=str(level)+temp+str(tries)+player+str(playpos)+playval
    if len(string)==14:
        return string


def winValue(string):
    global win_combo
    allhumpos=['a','b','c','d','e']
    allcompos=['A','B','C','D','E']
    hum=[]
    com=[]
    for i in range(1,10):
        if string[i] in allhumpos:
            hum.append(i)
        if string[i] in allcompos:
            com.append(i)
    if len(hum)>2:
        hpem=it.permutations(hum,3)
        for i in hpem:
            if i in win_combo:
                return -1,i
    if len(com)>2:
        cpem=it.permutations(com,3)
        for i in cpem:
            if i in win_combo:
                return 1,i
    return 0

win_combo=[(1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9),(1,5,9),(3,5,7)]


def childGenerator(strong,level,valuelist,humpos,compos,nopos,tries,player,playpos,playval,hwin,cwin):
    allhumpos={1:'a',2:'b',3:'c',4:'d',5:'e'}
    allcompos={1:'A',2:'B',3:'C',4:'D',5:'E'}
    global graph,graphlist,graphvalue,win_combo
    dlevel=level+1
    running=True
    available=list(nopos.keys())
    dtries=dp(tries)
    if dlevel%2==1:
        human=len(humpos.keys())
        add=allhumpos[human+1]
        dplayer='h'
    elif dlevel%2==0:
        computer=len(compos.keys())
        add=allcompos[computer+1]
        dplayer='c'
    dplayval=add
    while(running):
        if len(available)==0:
            break
        dvaluelist=dp(valuelist)
        dhumpos=dp(humpos)
        dcompos=dp(compos)
        dnopos=dp(nopos)
        dplaypos=dp(playpos)
        dhwin=dp(hwin)
        dcwin=dp(cwin)
        choiceposition=rd.choice(available)
        dplaypos=choiceposition
        del available[available.index(choiceposition)]
        dvaluelist[choiceposition-1]=1
        if dlevel%2==1:
            dhumpos[choiceposition]=add
        elif dlevel%2==0:
            dcompos[choiceposition]=add
        if len(dhumpos.keys())>2:
            dhwin=list(it.permutations(dhumpos,3))
        if len(dcompos.keys())>2:
            dcwin=list(it.permutations(dcompos,3))
        dstring=listToString(dlevel,dvaluelist,dhumpos,dcompos,dnopos,dtries,dplayer,dplaypos,dplayval,dhwin,dcwin)
        graph[strong][dstring]=0
        graphlist[strong].append(dstring)
        if strong not in graphvalue.keys():
            graphvalue[strong]=[]
        hwinner=[x for x in win_combo if x not in dhwin]
        cwinner=[x for x in win_combo if x not in dcwin]
        if len(hwinner)<len(win_combo):
            graph[strong][dstring]=-1
            graphvalue[strong].append(-1)
        elif len(cwinner)<len(win_combo):
            graph[strong][dstring]= 1
            graphvalue[strong].append(1)
        else:
            graphvalue[strong].append(0)
        
        
            
if pinkyloop==False:
    for i in graph['0*********0**0']:
        strong=i
        running=True
        stack=[strong]
        traphlist=dp(graphlist)
        size=1
        counter=0
        while len(stack)!=0:
            level,valuelist,humpos,compos,nopos,tries,player,playpos,playval,hwin,cwin=stringToList(strong)
            if level==9 or len(nopos.keys())==0:
                del stack[-1]
                if len(stack)==0:
                    break
                strong=stack[-1]
                continue
            hwinner=[x for x in win_combo if x not in hwin]
            if len(hwinner)<len(win_combo):
                del stack[-1]
                if len(stack)==0:
                    break
                strong=stack[-1]
                continue
            cwinner=[x for x in win_combo if x not in cwin]
            if len(cwinner)<len(win_combo):
                del stack[-1]
                if len(stack)==0:
                    break
                strong=stack[-1]
                continue
            if strong not in graph.keys():
                graph[strong]={}
            if strong not in graphlist.keys():
                graphlist[strong]=[]
            if strong not in graphvalue.keys():
                graphvalue[strong]=[]
            if len(graph[strong].keys())==0:
                childGenerator(strong,level,valuelist,humpos,compos,nopos,tries,player,playpos,playval,hwin,cwin)
                traphlist[strong]=dp(graphlist[strong])
            #print('##############################################')
            #print('traphliststrong',traphlist[strong])
            if len(traphlist[strong])==0 :
                for i in graphlist[strong]:
                    #print('graphlist',graph[strong])
                    if i in graph.keys():
                        #print('i',i)
                        temp=graph[i].values()
                        #print('graphi',graph[i].values())
                        if i[11]=='h':
                            #print('gs',graph[strong][i])
                            graph[strong][i]=max(temp)
                        if i[11]=='c':
                            graph[strong][i]=min(temp)
            choicelist=[x for x in traphlist[strong] if x not in stack]
            choicelist=[x for x in choicelist if graph[strong][x] not in [1,-1]]
            '''print()
            print()
            print(len(traphlist[strong]))
            print('strong',strong)
            print()
            print('stack',stack)
            print()
            print('graph',graph)
            print()
            print('graphlist',graphlist)
            print()
            print('graphvalue',graphvalue)
            print()
            print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')'''
            #print('choicelist',choicelist)
            #print('stack',stack)
            if len(choicelist)==0:
                if len(traphlist[strong])!=0:
                    traphlist[strong]=[]
                    if len(traphlist[strong])==0 :
                        for i in graphlist[strong]:
                            #print('graphlistdown',graph[strong])
                            if i in graph.keys():
                                #print('i',i)
                                temp=graph[i].values()
                                #print('graphidown',graph[i].values())
                                if i[11]=='h':
                                    #print('gsdown',graph[strong][i])
                                    graph[strong][i]=max(temp)
                                elif i[11]=='c':
                                    #print('gsdown',graph[strong][i])
                                    graph[strong][i]=min(temp)
                del stack[-1]
                if len(stack)==0:
                    break
                strong=stack[-1]
            else:
                choice=rd.choice(choicelist)
                #print('traphlist',traphlist[strong])
                del traphlist[strong][traphlist[strong].index(choice)]
                #print('traphlist',traphlist[strong])
                strong=choice
                stack.append(strong)
            #print(len(graph.keys()))
       


            
        
            
time2=time.time()
time3=(time2-time1)/60
print('Time in tree generation {}'.format(time3))            

graphloop=True
if os.path.exists('graph.pickle'):
    graphloop=False
if graphloop==True:
    with open('graph.pickle','wb') as f:
        pickle.dump(graph,f)
    

           



pygame.init()
tie=0
win=0
lost=0
swidth=850
sheight=850
screen=pygame.display.set_mode((swidth,sheight))
pygame.display.set_caption('THIS IS TIC TAC TOE')
gameloop=True
clock=pygame.time.Clock()
xrange=[0]
yrange=[0]
image0=pygame.image.load('re.png').convert_alpha()
imagex=pygame.image.load('close.png').convert_alpha()
imager=pygame.image.load('re.png').convert_alpha()
imagec=pygame.image.load('close.png').convert_alpha()
text_size=32
totallist=[1,2,3,4,5,6,7,8,9]
products=[6,28,45,80,105,162,120,504]
checklist=[]

 


green    =  (0,255,0,20)
white    =  (255,255,255)
aqua     =  (0, 255, 255)
black    =  (0, 0, 0)
blue     =  (0, 0, 255)
fuchsia  =  (255, 0, 255)
gray     =  (128, 128, 128)
lgray    =  (150,150,150,150)
greeny   =  (0, 128, 0)
lime     =  (0, 255, 0)
maroon   =  (128, 0, 0)
navyblue =  (0, 0, 128)
olive    =  (128, 128, 0)
purple   =  (128, 0, 128)
red      =  (255, 0, 0)
silver   =  (192, 192, 192)
teal     =  (0, 128, 128)
white    =  (255, 255, 255)
yellow   =  (255, 255, 0)
colors   =  [green,aqua,blue,fuchsia,greeny,
             lime,maroon,navyblue,olive,purple,red,silver,teal,yellow]

color1=rd.choice(colors)
color2=rd.choice(colors)
color3=rd.choice(colors)
color4=rd.choice(colors)

running=True
dicty={1:[110,110,280,280],2:[290,110,460,280],3:[470,110,640,280],4:[110,290,280,460],5:[290,290,460,460],6:[470,290,640,460],7:[110,470,280,640],8:[290,470,460,640],9:[470,470,640,640]}

level=0
valuelist=[0,0,0,0,0,0,0,0,0]
humpos={}
compos={}
nopos={1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
tries=None
player=None
playpos=None
playval=None
hwin=[]
cwin=[]
doubleloop=False
human=[]
computer=[]
clickhua=False
stringlist=[]
resetflag=False
resetclick=False
closeclick=False
donelist=[]
string=''
strongy=''
winflag=False
lostflag=False
tieflag=False
while(running):
    img=pygame.transform.scale(imager,(100,100))
    screen.blit(img,(700,110))
    img=pygame.transform.scale(imagec,(100,100))
    screen.blit(img,(700,310))
    pygame.draw.rect(screen,white,(100,100,550,550))
    pygame.draw.rect(screen,blue,(100,100,10,550))
    pygame.draw.rect(screen,blue,(280,100,10,550))
    pygame.draw.rect(screen,blue,(460,100,10,550))
    pygame.draw.rect(screen,blue,(640,100,10,550))
    pygame.draw.rect(screen,blue,(100,100,550,10))
    pygame.draw.rect(screen,blue,(100,280,550,10))
    pygame.draw.rect(screen,blue,(100,460,550,10))
    pygame.draw.rect(screen,blue,(100,640,550,10))
    mousex,mousey=pygame.mouse.get_pos()
    for a,b,c,d in dicty.values():
        if mousex in range(a,c+1) and mousey in range(b,d+1):
            pygame.draw.rect(screen,gray,(a,b,170,170))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
            print('WINS ',win)
            print('LOST ',lost)
            print('TIES ',tie)
        if event.type==pygame.MOUSEBUTTONDOWN:
            mx,my=pygame.mouse.get_pos()
            if mx in range(700, 801) and my in range(110,211):
                resetclick=True
            if mx in range(700,801) and my in range(310,441):
                running=False
                if winflag==True:
                    winflag=False
                    win+=1
                if lostflag==True:
                    lostflag=False
                    lost+=1
                if tieflag==True:
                    tieflag=False
                    tie+=1
                print('WINS ',win)
                print('LOST ',lost)
                print('TIES ',tie)
            if resetflag==False:
                for key,(a,b,c,d) in dicty.items():
                    if mousex in range(a,c+1) and mousey in range(b,d+1):
                        if key not in nopos.keys():
                            break
                        if key in donelist:
                            break
                        level+=1
                        valuelist[key-1]=1
                        temp=len(humpos)
                        allhumpos={1:'a',2:'b',3:'c',4:'d',5:'e'}
                        humpos[key]=allhumpos[temp+1]
                        del nopos[key]
                        player='h'
                        playpos=key
                        playval=allhumpos[temp+1]
                        if len(humpos.keys())>2:
                            hwin=list(it.permutations(humpos,3))
                        if len(compos.keys())>2:
                            cwin=list(it.permutations(compos,3))
                        if doubleloop==False:
                            tries=key
                            doubleloop=True
                        string=listToString(level,valuelist,humpos,compos,nopos,tries,player,playpos,playval,hwin,cwin)
                        #print('string',string)
                        #print('graphstring',graph[string])
                        #print('stringlist',stringlist)
                        #print(level,valuelist,humpos,compos,nopos,tries,player,playpos,playval,hwin,cwin)
                        human.append([a,b,170,170])
                        clickhua=True
                        stringlist.append(string)
                        donelist.append(key)
    if clickhua==True:
        clickhua=False
        if string in graph.keys():
            #print('string',graph[string])
            if 1 in graph[string].values():
                listing=[(x,y) for x,y in list(graph[string].items())]
                #print(listing)
                rd.shuffle(listing)
                tempr=[(x,y) for x,y in graph[string].items() if y==1 if x not in graph.keys()]
                #print(tempr)
                #print(graph[string].items())
                for key,val in listing:
                    if len(tempr)!=0:
                        donning=rd.choice(tempr)
                        strongy=donning[0]
                        break
                    box=int(key[12])
                    if val==1 and key not in stringlist and box not in donelist:
                        strongy=key
                        break
            elif 0 in graph[string].values():
                listing=[(x,y) for x,y in list(graph[string].items())]
                rd.shuffle(listing)
                for key,val in listing:
                    box=int(key[12])
                    if val==0 and key not in stringlist and box not in donelist:
                        strongy=key
                        break
            else:
                choice=[x for x in graph[string].keys() if x not in stringlist]
                strongy=rd.choice(choice)   
            donelist.append(int(strongy[12]))
            stringlist.append(strongy)
            level,valuelist,humpos,compos,nopos,tries,player,playpos,playval,hwin,cwin= stringToList(strongy)
            computer.append([dicty[playpos][0],dicty[playpos][1],170,170])
            #print('strong',strongy)
            #print('stringlist',stringlist)
            #print(level,valuelist,humpos,compos,nopos,tries,player,playpos,playval,hwin,cwin)
    if len(human)!=0:
        for a,b,c,d in human:
            image=pygame.transform.scale(imagex,(170,170))
            screen.blit(image,(a,b))
    if len(computer)!=0:
        for a,b,c,d in computer:
            image=pygame.transform.scale(image0,(170,170))
            screen.blit(image,(a,b))
    hwinner=[x for x in win_combo if x not in hwin]
    if len(hwinner)<len(win_combo):
        resetflag=True
        winflag=True
    cwinner=[x for x in win_combo if x not in cwin]
    if len(cwinner)<len(win_combo):
        resetflag=True
        lostflag=True
        #print('resetflag',resetflag)
        #print('lostflag',lostflag)
    if len(stringlist)==9:
        resetflag=True
        tieflag=True
    if(resetflag==True):
        if resetclick==True:
            if winflag==True:
                winflag=False
                win+=1
            if lostflag==True:
                lostflag=False
                lost+=1
            if tieflag==True:
                tieflag=False
                tie+=1
            level=0
            valuelist=[0,0,0,0,0,0,0,0,0]
            humpos={}
            compos={}
            nopos={1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
            tries=None
            player=None
            playpos=None
            playval=None
            hwin=[]
            cwin=[]
            doubleloop=False
            human=[]
            computer=[]
            clickhua=False
            stringlist=[]
            resetflag=False
            resetclick=False
            closeclick=False
            donelist=[]
            string=''
            strongy=''
    if resetclick==True:
            level=0
            valuelist=[0,0,0,0,0,0,0,0,0]
            humpos={}
            compos={}
            nopos={1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
            tries=None
            player=None
            playpos=None
            playval=None
            hwin=[]
            cwin=[]
            doubleloop=False
            human=[]
            computer=[]
            clickhua=False
            stringlist=[]
            resetflag=False
            resetclick=False
            closeclick=False
            donelist=[]
            string=''
            strongy=''
    pygame.display.update()
pygame.quit()
