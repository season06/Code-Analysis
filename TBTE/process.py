from django.db import models
from graphviz import Digraph
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

# if(i==1){print(i);}elseif(i==2){print(i+1);print(i+3);}elseif(i==3){print(i+4);}else{print(i+2);}
# while(i==0){111;2222;333;}
# for(int i=0;i<10;i/++){1111;2222;3333;}
# while(i!=0){if(i==1){i++;}elseif(i==2){i+=5;}elseif(i==3){i+=3;}}
# code="if(1){111;if(2){222;}else{333;}}elseif(5){555;if(6){666;}}elseif(9){999;}else{888;if(7){777;}}"
# code="if(i==1){print(i);}elseif(i==2){print(i+1);print(i+3);}elseif(i==3){print(i+4);}else{print(i+2);}"
# code="while(i==0){111;2222;333;}"
# code="while(1){111;if(2){222;}elseif(3){333;}else{444;}}"
# code="while(i!=0){if(i==1){i++;}elseif(i==2){i+=5;}elseif(i==3){i+=3;}}"
# code="if(1){111;}i++;"
# code="while(i++){if(1){222;}else{333;}}123;"
# code="while(i!=0){if(i==1){i++;}elseif(i==2){i+=5;}elseif(i==3){i+=3;}9999;}"
# code="while(i!=0){if(i==1){i++;}elseif(i==2){i+=5;}elseif(i==3){i+=3;}}if(2){333;}"
# code="if(10){1010;}if(1){if(2){222;}else{333;if(9){999;}}}elseif(5){if(6){666;}}else{if(7){777;}j++;}"
# code="inti=0;while(i<10){intj=0;while(j<20){2222;j++;}i++;}" #=for loop
# code="for(int i=0;i<10;i++){1111;2222;3333;}"
# code="for(inti=0;i<10;i++){for(intj=0;j<10;j++){print(i);}}"
# code="for(i;2;3){if(4){4444;}elseif(5){5555;}else{666;}i++;}999;"

class Analysis:
    def __init__(self, code):
        self.code = code

    def generate_diagram(self):
        code = str(self.code)
        e = Digraph('flow', filename='diagram', format="png")
        count = 0
        def preprocessing(data):
            new=""
            for i in range(len(data)):
                check=False
                if data[i]=="f" and data[i+1]=="o" and data[i+2]=="r" and data[i+3]=="(":
                    check=True
                    c=0
                    proc=""
                    left=0
                    right=0
                    string=""
                    for j in range(i+4,len(data),1):
                        string+=data[j]
                        if data[j]==";":
                            if c==0:
                                new+=string+"while("
                                string=""
                                c+=1
                            elif c==1:
                                new+=string[:-1]+")"
                                string=""
                                c+=1
                        elif data[j]==")"and data[j+1]=="{" and c==2:
                            proc=string[:-1]+";"
                            c+=2
                            string=""
                        elif data[j]=="{":
                            left+=1
                        elif data[j]=="}":
                            right+=1
                            if left==right:
                                new=new+string[:len(string)-1]+proc+"}"
                                break
                if check:
                    data=data[:i]+new+data[j+1:]
                    return data
            return False
        def draw(shape,id,content):
            if shape=="process":
                e.attr('node', shape='box')
            elif shape=="decision":
                e.attr('node', shape='diamond')
            elif shape=="terminator":
                e.attr('node', shape='ellipse')
            e.node(str(id),content)

        def path(id1,id2,id):
            id1=str(id1)
            id2=str(id2)
            if id==0:
                e.edge(id1,id2)
            elif id==1:
                e.edge(id1,id2, label="True", len='1.00')
            elif id==2:
                e.edge(id1, id2, label="False", len='1.00')
        class Node:
            def __init__(self,data):
                self.data=data
                self.nextR=None
                self.nextL=None
            def link_all(self,id,L,R):
                if self:
                    print(self.data)
                    if self.data[1]!=id and self.data[1]>=L and self.data[1]<=R:
                        if self.data[0]== "process" and self.nextL==None and len(self.data)==3:
                                self.fix(self.data[1],id)
                        elif self.data[0]=="decision" and self.nextR==None and len(self.data)==3:
                                self.fix(self.data[1],id)
                    if self.nextL:
                        self.nextL.link_all(id,L,R)
                    if self.nextR:
                        self.nextR.link_all(id,L,R)
            def fix(self,id,data):
                if self:
                    if self.data[1]==id:
                        self.data.append(data)
                    else:
                        if self.nextL:
                            self.nextL.fix(id,data)
                        if self.nextR:
                            self.nextR.fix(id,data)
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
                    draw(self.data[0],self.data[1],self.data[2])
                    if self.nextL:
                        self.nextL.pri()
                    if self.nextR:
                        self.nextR.pri()
            def link(self):
                if self:
                    if len(self.data)==4:
                        path(self.data[1],self.data[3],0)
                    if self.data[0]== "process" or self.data[0]=="terminator":
                        if self.nextL:
                            path(self.data[1],self.nextL.data[1],0)
                    elif self.data[0]=="decision":
                        if self.nextL:    
                            path(self.data[1],self.nextL.data[1],1)
                        if self.nextR:
                            path(self.data[1],self.nextR.data[1],2)
                    if self.nextL:
                        self.nextL.link()
                    if self.nextR:
                        self.nextR.link()

        code=code.replace(" ","")
        code=code.replace("\n","")
        while True:
            if preprocessing(code)==False:
                break
            else:
                code=preprocessing(code)
        count=0
        n1=Node(["terminator",count,"start"])
        iswhile=0
        string=""
        i=-1
        fun=[]
        fun.append([8,0])
        while i<len(code)-1:
            i+=1
            string+=code[i]
            if string=="if(":
                fun.append([4,count+1])
                string=""
            elif string=="elseif(":
                fun.append([5,count+1])
                string=""
            elif string=="else" and code[i+1]=="{":
                fun.append([6,count+1])
                string=""
            elif string=="while(":
                fun.append([7,count+1])
                iswhile=1
                string=""
            elif code[i]==")" and code[i+1]=="{":
                count+=1
                if fun[len(fun)-2][0]==8 or fun[len(fun)-3][0]==4 or fun[len(fun)-3][0]==5 or fun[len(fun)-3][0]==7:
                    n1.insert(count-1,["decision",count,string[:-1]])
                elif fun[len(fun)-2][0]==10:
                    n1.insert(fun[len(fun)-2][2],["decision",count,string[:-1]])
                    if fun[len(fun)-2][0]==4 or fun[len(fun)-2][0]==7:
                        ran=-1
                        for j in range(len(fun)-2,-1,-1):
                            if fun[j][0]==10 and fun[j][1]==4:
                                ran=fun[j][2]
                                print(ran,count-1)
                                break
                        n1.link_all(count,ran,count-1)
                else:
                    minus=2
                    if fun[len(fun)-3][0]==6:
                        minus=4
                    count_ten=0
                    is_count=True
                    now_count=0
                    for j in range(len(fun)-minus,-1,-1):
                        if fun[j][0]==10 and is_count:
                            count_ten+=1
                        else:
                            is_count=False
                        if is_count==False:
                            if fun[j][0]==4 or fun[j][0]==5 or fun[j][0]==7:
                                now_count+=1
                            if now_count==count_ten:
                                n1.insert(fun[j][1],["decision",count,string[:-1]])
                                break
                string=""
            elif code[i]==";":
                count+=1
                if len(fun)==1 or fun[len(fun)-1][0]==8 or fun[len(fun)-2][0]==4 or fun[len(fun)-2][0]==5 or fun[len(fun)-2][0]==7:
                    n1.insert(count-1,["process",count,string[:-1]])
                if fun[len(fun)-1][0]==10:
                    if fun[len(fun)-1][1]==7 or fun[len(fun)-1][1]==4:
                        n1.insert(fun[len(fun)-1][2],["process",count,string[:-1]])
                    
                    if fun[len(fun)-1][1]==5 or fun[len(fun)-1][1]==6:
                        n1.insert(fun[len(fun)-2][1],["process",count,string[:-1]])
                    ran=-1
                    for j in range(len(fun)-1,-1,-1):
                        if fun[j][0]==10 and fun[j][1]==4:
                            ran=fun[j][2]
                            print(ran,count-1)
                            break
                    if ran!=-1:
                        n1.link_all(count,ran,count-1)
                else:
                    if fun[len(fun)-2][0]==6:
                        count_ten=0
                        is_count=True
                        now_count=0
                        for j in range(len(fun)-3,-1,-1):
                            if fun[j][0]==10 and is_count:
                                count_ten+=1
                            else:
                                is_count=False
                            if is_count==False:
                                if fun[j][0]==4 or fun[j][0]==5 or fun[j][0]==7:
                                    now_count+=1
                                if now_count==count_ten:
                                    print(code[i-1],fun[j][1])
                                    n1.insert(fun[j][1],["process",count,string[:-1]])
                                    break
                fun.append([8,count])
                string=""
            elif code[i]=="{":
                fun.append([9,fun[len(fun)-1][0],0,fun[len(fun)-1][1]])
                string=""
            elif code[i]=="}":
                for j in range(len(fun)-1,-1,-1):
                    if fun[j][0]==9 and fun[j][2]==0:
                        fun.append([10,fun[j][1],fun[j][3]])
                        fun[j][2]=1
                        break
                if fun[len(fun)-1][0]==10 and fun[len(fun)-1][1]==7:
                    if fun[len(fun)-2][0]==10:
                        for j in range(len(fun)-2,-1,-1):
                            if fun[j][0]==10 and fun[j-1][0]==8:
                                n1.fix(fun[j-1][1],fun[len(fun)-1][2])
                    elif fun[len(fun)-2][0]==8:
                        n1.fix(fun[len(fun)-2][1],fun[len(fun)-1][2])
                string=""

        print(fun)
        n1.pri()
        n1.link()
        e.render('./media/diagram')