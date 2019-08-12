from copy import deepcopy as dp
import random as rd
import itertools as it
import time

time1=time.time()

graph={'1h********1':{},'1*h*******2':{},
       '1**h******3':{},'1***h*****4':{},
       '1****h****5':{},'1*****h***6':{},
       '1******h**7':{},'1*******h*8':{},
       '1********h9':{}}
graphlist={'1h********1':[],'1*h*******2':[],
       '1**h******3':[],'1***h*****4':[],
       '1****h****5':[],'1*****h***6':[],
       '1******h**7':[],'1*******h*8':[],
       '1********h9':[]}

def stringToList(string):
    listy=[]
    hpos=[]
    cpos=[]
    nopos=[]
    for i in range(1,len(string)):
        if string[i]=='h':
            hpos.append(i)
            listy.append(1)
        if string[i]=='c':
            cpos.append(i)
            listy.append(1)
        if string[i]=='*':
            nopos.append(i)
            listy.append(0)
    trying=int(string[-1])
    level=int(string[0])
    return level,listy,trying,hpos,cpos,nopos

def listToString(level,listy,trying,hpos,cpos,nopos):
    temp=''
    for i,v in enumerate(listy):
        if i+1 in hpos and v==1:
            temp+='h'
        if i+1 in cpos and v==1:
            temp+='c'
        if v==0:
            temp+='*'
    string=str(level)+temp+str(trying)
    return string

win_combo=[(1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9),(1,5,9),(3,5,7)]
donelist={}
dgraph=dp(graph)
covered=[]
for i in dgraph.keys():
    running=True
    strong=i
    stacky=[strong]
    while len(stacky)!=0:
        #print('stacky',stacky)
        #print('graph',graph)
        flying=0
        hflag=0
        flag=0
        level,listy,trying,hpos,cpos,nopos=stringToList(strong)
        if level==9 or len(nopos)==0:
            temp=stacky.pop()
            if len(stacky)!=0:
                strong=stacky[-1]
                graph[strong][temp]=0
                del donelist[strong][donelist[strong].index(temp)]
        if len(hpos)>=3:
            hpem=list(it.permutations(hpos,3))
            for a1 in hpem:
                if a1 in win_combo:
                    temp=stacky.pop()
                    #print('htemp',temp)
                    if len(stacky)!=0:
                        strong=stacky[-1]
                        graph[strong][temp]=-1
                        del donelist[strong][donelist[strong].index(temp)]
                        hflag=1
                        break
            if hflag==1:
                hflag=0
                print('graph',graph)
                print('\n')
                continue
        if len(cpos)>=3:
            cpem=list(it.permutations(cpos,3))
            for a1 in cpem:
                if a1 in win_combo:
                    temp=stacky.pop()
                    #print('ctemp',temp)
                    if len(stacky)!=0:
                        strong=stacky[-1]
                        graph[strong][temp]=1
                        del donelist[strong][donelist[strong].index(temp)]
                        flag=1
                        break
            if flag==1:
                flag=0
                continue
        dlevel=level
        dlevel+=1
        listu=[]
        dnopos=dp(nopos)
        for j in range(len(nopos)):
            dhpos=dp(hpos)
            dcpos=dp(cpos)
            dnopos=dp(nopos)
            temp=(nopos[j])-1
            twisty=dp(listy)
            twisty[temp]=1
            if dlevel%2==1:
                dhpos.append(nopos[j])
            if dlevel%2==0:
                dcpos.append(nopos[j])
            del dnopos[j]
            string=listToString(dlevel,twisty,trying,dhpos,dcpos,dnopos)
            if strong not in graph.keys():
                graph[strong]={}
                graphlist[strong]=[]
            if string not in graph[strong].keys():
                graph[strong][string]=0
                graphlist[strong].append(string)
            if strong not in donelist.keys():
                donelist[strong]=[]
                flying=1
            if flying==1:
                donelist[strong].append(string)
        flying=0
        choice=[x for x in donelist[strong] if x not in stacky]
        if len(choice)!=0:
            strong=choice[0]
            stacky.append(strong)
        if len(choice)==0:
            temp=stacky.pop()
            if len(stacky)!=0:
                strong=stacky[-1]
                del donelist[strong][donelist[strong].index(temp)]
        
for i in graph.keys():
    if i[0]=='8' and i[-1]=='1' :#and 1 in list(graph[i].values()) :
        print(i,' : ',graph[i])

                
traph=dp(graph)
strong='1h********1'
stacky=['1h********1']
flag=0
covered=[]
while(len(stacky)!=0):
    #print('stacky',stacky)
    #print('strong',strong)
    if strong not in traph.keys():
        l=stacky.pop()
        if len(stacky)==0:
            break
        strong=stacky[-1]
    for i in traph[strong].keys():
        if i not in traph.keys():
            l=stacky.pop()
            if len(stacky)==0:
                break
            strong=stacky[-1]
            flag=1
            break    
        if i in traph.keys():
            minmax=[]
            for j in traph[i].keys():
                minmax.append(traph[i][j])
            if len(minmax)==0:
                temp=0
            else:
                if flag==0:
                    if -1 not in minmax or 1 not in minmax:
                        break
                    else:
                        flag==1
                if int(i[0])%2==1:
                    temp=max(minmax)
                if int(i[0])%2==0:
                    temp=min(minmax)
            #print('temp',temp)
            #print('minmax',minmax)
            graph[strong][i]=temp
            #print('i',i)
            #print('graph[strong]',graph[strong])
    choice=list(traph[strong].keys())
    choice=[x for x in choice if x not in stacky]
    if len(choice)!=0:
        a=choice[0]
        del traph[strong][a]
        strong=a
        stacky.append(strong)
    if len(choice)==0:
        l=stacky.pop()
        if len(stacky)==0:
            break
        strong=stacky[-1]

time2=time.time()
time3=(time2-time1)/60
print('Time in tree generation {}'.format(time3))
for i in graph.keys():
    if i[0]=='8' and i[-1]=='1' :#and 1 in list(graph[i].values()) :
        print(i,' : ',graph[i])
        


        
    
    
                
            
            
            
        
            





   


            
            
