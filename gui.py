import sys, os
from filesplit import FileSplit
import client
import threading
import commands
import time
from random import randint 

class GUI : 
    
    def p(self,shareFile):
        
        while True: 
            self.command_list()
            print("waiting for you ")
            out=input("Please Enter The Name of The Command: ")
            print(out)
            if int(out) == 3 : 
                return out

            elif int(out) == 1 :
                path=input("Please Insert The Name of The Torrent File\n(For returning to the main manu, Insert 0)")
                if path == '0' : 
                    continue
                else :
                    name=''
                    hashedFile=''
                    count_chunk=0
                    with open(path,'r') as file : 
                        name = (file.read().split("\n")[0])
                        file.seek(0)
                        hashname = (file.read().split("\n")[1])
                        file.seek(0)
                        count_chunk = int(file.read().split("\n")[2])
                        file.seek(0)
                        hashedFile=(file.read().split("\n")[3])

                        payload = {'id':shareFile.ID,'ip':shareFile.HOST,'hash':int(hashname),'name':name}
                        connect_to = shareFile.next_peers['first']['ip']
                        t=threading.Thread(target=client.Client(shareFile,connect_to).find_seeder,args=(shareFile,payload))
                        t.daemon=True
                        t.start()

                    t=threading.Thread(target=self.checker,args=(count_chunk,hashedFile,name,shareFile))
                    t.daemon=True
                    t.start()

                        

            elif int(out) == 2 : 
                path=input("Please Insert The Name of The Upload File\n(For returning to the main manu, Insert 0)")
                if path == '0' : 
                    continue
                else: 
                    if not os.path.isfile(path) : 
                        print("The ",path," does not exist")
                        continue

                    if not shareFile.peers: 
                        connect_to = shareFile.next_peers['first']['ip']
                        counter = 0
                        payload = {'id':shareFile.ID , 'ip' : shareFile.HOST , 'counter' : counter}
                        t=threading.Thread(target=client.Client(shareFile,connect_to).find_peers,args=(shareFile,payload,210))
                        t.daemon=True
                        t.start()



                    fs = FileSplit(path , 256000, str(shareFile.HOST)+'/output/')
                    number_of_chunks=fs.split()
                    
                    hashedName = None

                    with open(path+".torrent","w+")  as f : 
                        f.write(path +'\n')
                        hashedName=hash(path)%400
                        f.write(str(hashedName) + '\n')
                        print(hashedName)
                        f.write(str(number_of_chunks) + '\n')
                        hashfile=commands.Commands().md5hashing(path)
                        f.write(str(hashfile))
                    
                    if shareFile.previous_node['node']['id']>shareFile.ID : 
                        if shareFile.ID >= hashedName and shareFile.next_peers['first']['id'] > hashedName:
                            self.save_to_database(shareFile,1,number_of_chunks,hashedName,path) 

                        else:
                            self.send_chunks(shareFile,0,number_of_chunks,hashedName,path)
                            

                    elif shareFile.ID >= hashedName and shareFile.previous_node['node']['id'] < hashedName : 
                        self.save_to_database(shareFile,1,number_of_chunks,hashedName,path)

                    else : 
                        self.send_chunks(shareFile,0,number_of_chunks,hashedName,path)
                       
                    

                    
                    self.uyt(shareFile,number_of_chunks,hashedName,path)

                                


               
            


    def command_list(self): 
        print("1- Download")
        print("2- Upload")
        print("3- Exit")

    def checker(self,count,hashedFile,name,shareFile):
        ff,ss = name.split('.')
        aa=b''
        p = False
        while True : 
            time.sleep(5)
            for i in range(1,count+1):
                m=str(shareFile.HOST)+'/'+str(ff)+'_'+str(i)+'.'+str(ss)
                out=os.path.isfile(m)
                print(m+"   "+str(out))
                if out:
                    if i == count :
                        p = True
                        break
                    else: 
                        continue
                else:
                    break 

            if p ==True : 
                c=1
                while c <= count : 
                    m=str(shareFile.HOST)+'/'+str(ff)+'_'+str(c)+'.'+str(ss)
                    with open(m,'rb') as f :
                        xx=f.read()
                        aa = aa+xx
                        c = c + 1 

                with open(str(shareFile.HOST)+'/'+name,'wb+') as f : 
                    f.write(aa)
                c=1
                while c <= count : 
                    m=str(shareFile.HOST)+'/'+str(ff)+'_'+str(c)+'.'+str(ss)
                    os.remove(m) 
                    c=c+1
                del shareFile.temp[:]
                break
                

            
                

    def save_to_database(self,shareFile,c,a,hashedName,path):
        while c <= a:
            shareFile.database.append({'hash':hashedName,'name':path,'chunk':c,'ip':shareFile.HOST,'id':shareFile.ID})
            c = c+1

    def send_chunks(self,shareFile,c,a,hashedName,path):
        payload={}
        while c < a:
            payload[c]={'hash':hashedName,'name':path,'chunk':c+1,'ip':shareFile.HOST,'id':shareFile.ID}
            c = c+1

        connect_to = shareFile.next_peers['first']['ip']
        t=threading.Thread(target=client.Client(shareFile,connect_to).who_is_responsible,args=(shareFile,payload))
        t.daemon=True
        t.start()

    def uyt(self,shareFile,number_of_chunks,hashedName,path):
        while True :

            if shareFile.peers :
                print("#########")
                for j in shareFile.peers:
                    payload={}
                    zz=0
                    for i in range(1,6):
                        rand=randint(1,number_of_chunks)
                        payload[zz]={'hash':hashedName,'name':path,'chunk':rand,'ip':shareFile.HOST,'id':shareFile.ID}
                        zz= zz+1
                    connect_to=j['ip']        
                    t=threading.Thread(target=client.Client(shareFile,connect_to).get_ready_for_download,args=(shareFile,payload))
                    t.daemon=True
                    t.start()
                break


