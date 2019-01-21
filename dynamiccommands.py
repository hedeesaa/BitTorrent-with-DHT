

from random import randint
import json
import threading

class DynamicCommands : 

    
    def finding_lines(self,file):
        num_lines = sum(1 for line in open(file))
        f =randint(0, num_lines-1)
        s = 0
        if f == num_lines-1 : 
            s = 0
        else : 
            s = f + 1

        return f,s

    def finding_target(self,file):
        f,s=self.finding_lines(file)

        with open(file,'r') as fi : 
            first = (fi.read().split("\n")[f])
            ipTarget = first.split(",")[1]
            idTarget = first.split(",")[0]
            gateway={}
            gateway['node']={'id':idTarget,'ip':ipTarget}

            counter1 = 0 
            if s == 0 : 
                counter1=0
            else : 
                counter1 = int(first.split(",")[0]) + 1 


            fi.seek(0)
            second = (fi.read().split("\n")[s])
            counter2 = int(second.split(",")[0])
            counter2= counter2 - 1



        return gateway , counter1 , counter2

    def finding_node(self,counter1,counter2):
        nodeID=randint(counter1,counter2)
        return nodeID
    



    






        

        
       
        

   


            

