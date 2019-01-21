import socket
import threading
import time
import client
import serverdatahandler
import pinger
import gui 
from multiprocessing.pool import ThreadPool




class StaticNode:

    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    flag_making_client=0
    flag_dynamic=0
    sharedFile=None

    def __init__(self,sharedFile):

        self.sharedFile=sharedFile

        if 'first' in self.sharedFile.next_peers  :
            self.flag_making_client = 1

        elif 'node' in self.sharedFile.gateway:
            self.flag_dynamic = 1

        
        self.sock.bind((self.sharedFile.HOST ,self.sharedFile.PORT))
        self.sock.listen(10)
        self.turn_on_server()

 
    def handler(self,conn):
        
        while True:
            data=conn.recv(280000) 
            if not data :
                print("connection closed")
                conn.close()
                break
            handle=serverdatahandler.ServerDataHandler()
            result=handle.data_handler(data,self.sharedFile)

            if result == 0 : 
                conn.close()
                break
            conn.send(result)
          
        
    def turn_on_server(self):
        
        if self.flag_making_client == 1 :
            self.make_client()

        elif self.flag_dynamic == 1 : 
            self.make_dynamic()

            
        print("LISTENING...")
        self.start()
        
        while True:
            
           
            print("Wainting for call...")
            conn , addr = self.sock.accept()
            print("CONNECTED TO: ", addr)
            t=threading.Thread(target=self.handler,args=(conn,))
            t.start()
           

    
  
    def status_print(self):
        while True : 
           print("next peers are : ", self.sharedFile.next_peers)
           print("pre peer is  : ", self.sharedFile.previous_node)
           print("peers are  : ", self.sharedFile.peers)
           #print("database is  : ", self.sharedFile.database)

           time.sleep(7)


    def make_client(self):
        connect_to = self.sharedFile.next_peers['first']['ip']
        t1=threading.Thread(target=client.Client(self.sharedFile, connect_to).get_the_next_node,args=(self.sharedFile,))
        t1.daemon=True
        t1.start()

        t2=threading.Thread(target=client.Client(self.sharedFile, connect_to).check_previous,args=(self.sharedFile,))
        t2.daemon=True
        t2.start()

    def make_dynamic(self):
        connect_to = self.sharedFile.gateway['node']['ip']
        payload={'id' : self.sharedFile.ID,'ip':self.sharedFile.HOST}
        command= 200
        t1=threading.Thread(target=client.Client(self.sharedFile, connect_to).find_your_place,args=(self.sharedFile,payload,command))
        t1.daemon=True
        t1.start()

    def start(self):
        pingur = threading.Thread(target=pinger.Pinger().timer,args=(self.sharedFile,0))
        pingur.daemon=True
        pingur.start()

        
        g = threading.Thread(target=gui.GUI().p,args=(self.sharedFile,))
        g.daemon=True
        g.start()

        status = threading.Thread(target=self.status_print)
        status.daemon=True
        status.start()








           
            



        




