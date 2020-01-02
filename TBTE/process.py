from django.db import models
from graphviz import Digraph
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

# if(i==1){print(i);}elseif(i==2){print(i+1);print(i+3);}elseif(i==3){print(i+4);}else{print(i+2);}
# while(i==0){111;2222;333;}
# for(int i=0;i<10;i/++){1111;2222;3333;}
# while(i!=0){if(i==1){i++;}elseif(i==2){i+=5;}elseif(i==3){i+=3;}}

class Analysis:
    def __init__(self, code):
        self.code = code

    def generate_diagram(self):
        code = str(self.code)
        e = Digraph('flow', filename='diagram', format="png")
        count = 0
        class Node:
            def __init__(self,data):
                self.data=data
                self.nextR=None
                self.nextL=None
            def draw(self, shape,id,content):
                if shape=="process":
                    e.attr('node', shape='box')
                elif shape=="decision":
                    e.attr('node', shape='diamond')
                elif shape=="terminator":
                    e.attr('node', shape='ellipse')
                e.node(str(id),content)

            def path(self, id1,id2,id):
                id1=str(id1)
                id2=str(id2)
                if id==0:
                    e.edge(id1,id2)
                elif id==1:
                    e.edge(id1,id2, label="True", len='1.00')
                elif id==2:
                    e.edge(id1, id2, label="False", len='1.00')
            def insert(self,id,data):
                if self:
                    if self.data[1]==id:
                        if self.nextL==None:
                            self.nextL=Node(data)
                        else:
                            self.nextR=Node(data)
                    else:
                        if self.nextL:
                            self.nextL.insert(id,data)
                        if self.nextR:
                            self.nextR.insert(id,data)
            def pri(self):
                if self:
                    print(self.data)
                    self.draw(self.data[0],self.data[1],self.data[2])
                    if self.nextL:
                        self.nextL.pri()
                    if self.nextR:
                        self.nextR.pri()
            def link(self):
                if self:
                    if len(self.data)==4:
                        self.path(self.data[1],self.data[3],0)
                    if self.data[0]== "process" or self.data[0]=="terminator":
                        if self.nextL:
                            self.path(self.data[1],self.nextL.data[1],0)
                    elif self.data[0]=="decision":
                        if self.nextL:    
                            self.path(self.data[1],self.nextL.data[1],1)
                        if self.nextR:
                            self.path(self.data[1],self.nextR.data[1],2)
                    if self.nextL:
                        self.nextL.link()
                    if self.nextR:
                        self.nextR.link()

        n1=Node(["terminator",count,"start"])
        func=[]
        func.append([8,0])
        iswhile=0
        isdecision=0
        string=""
        decision=[]
        decision.append(0)
        left=0
        right=0
        left_arr=[]
        right_arr=[]
        stack=[]
        for_stack=[]
        back=0
        i=-1
        while i<len(code)-1:
            i+=1
            string+=code[i]
            if string=="for(":
                func.append([1,0])
                isdecision=5
                string=""
                c=0
                for j in range(i+1,len(code),1):
                    string+=code[j]
                    if code[j]==';':
                        count+=1
                        if c==0:
                            func.append([2,0])
                            c+=1
                            stack.append(count)
                            n1.insert(count-1,["process",count,string[:-1]])
                        elif c==1:
                            func.append([3,0])
                            decision.append(count)
                            n1.insert(count-1,["decision",count,string[:-1]])
                        string=""
                    elif code[j]==")":
                        for_stack.append(string[:-1])
                        i=j+1
                        string=""
                        break
            elif string=="while(":
                func.append([7,0])
                isdecision=3
                string=""
            elif string=='if(':
                func.append([4,0])
                decision.append(count+1)
                isdecision=1
                string=""
            elif code[i]==')':
                if isdecision==0 or isdecision==2:
                    continue
                string=string[:-1]
                count+=1
                if isdecision==1 or isdecision==3:
                    for j in range(len(decision)-1,-1,-1):
                        if decision[j]<count:
                            n1.insert(decision[j],["decision",count,string])
                            break
                if isdecision==3:
                    isdecision=4
                    stack.append(count)
                if isdecision!=4:
                    isdecision=0
                string=""
            elif code[i]==';':
                count+=1
                func.append([8,0])
                string=string[:-1]
                if isdecision==2:
                    for j in range(len(decision)-1,-1,-1):
                        if decision[j]<count:
                            n1.insert(decision[j],["process",count,string])
                            break
                elif isdecision==4 and code[i+1]=="}":
                    n1.insert(count-1,["process",count,string,stack.pop()])
                elif isdecision==5 and code[i+1]=='}':
                    n1.insert(count-1,["process",count,string])
                    count+=1
                    n1.insert(count-1,["process",count,for_stack.pop(),stack.pop()])
                else:
                    n1.insert(count-1,["process",count,string])
                string=""
            elif string=="elseif(":
                func.append([5,0])
                decision.append(count+1)
                isdecision=1
                string=""
            elif string=="else":
                func.append([6,0])
                isdecision=2
                string=""
            elif string=="{":
                func.append([9,0])
                left+=1
                string=""
            elif string=="}":
                func.append([10,0])
                if iswhile==1:
                    for j in range(len(func)-1,-1,-1):
                        if func[j][0]==0:
                            if func[j-1][0]==7:
                                iswhile=0
                string=""

        print(decision)
        n1.pri()
        n1.link()
        e.render('./media/diagram')