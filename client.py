import socket 

import subprocess
import threading
import time
import json
import shared 
import commands
import staticnode
import jsonhandler



class Client :

    sock=None
    Client_PORT=0
    



    def __init__(self, shareFile , connect_to): #flag #means Dasti or not

        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind((shareFile.HOST,self.Client_PORT))

        self.sock.connect((connect_to,shareFile.PORT))

       
    def recieve_handler(self,send):
        jhandler = jsonhandler.JsonHandler()
        self.sock.sendall(jhandler.dic_to_json(send))
        data=self.sock.recv(280000)
        recieved=jhandler.json_to_dic(data)
        return recieved


    def get_the_next_node(self,shareFile):

        send={'id' : shareFile.ID,'ip':shareFile.HOST, 'command' : 112 }
        recieved=self.recieve_handler(send)

        if recieved['command']==113:  #will be answer ALWAYS by server
            shareFile.next_peers['second']={'id':recieved['payload']['id'],
                                                  'ip':recieved['payload']['ip']}
        self.sock.close()
  
    def check_previous(self,shareFile):
 
        jhandler = jsonhandler.JsonHandler()
            
        send={'id' : shareFile.ID,'ip':shareFile.HOST, 'command' : 115 , 'payload' : {'id' : shareFile.ID,'ip':shareFile.HOST}}
        recieved=self.recieve_handler(send)

        if recieved['command']== 400 : 
            self.sock.close()
            

    
    def changing_the_pre (self, shareFile,payload,command):
        jhandler = jsonhandler.JsonHandler()
        
        send={'id' : shareFile.ID,'ip':shareFile.HOST, 'command' : command , 'payload' : payload}
        recieved=self.recieve_handler(send)
        if recieved['command']== 400 or recieved['command']== 300:
            self.sock.close()



    def change_your_next_next(self, shareFile , payload):
        jhandler = jsonhandler.JsonHandler()
        send={'id' : shareFile.ID,'ip':shareFile.HOST, 'command' : 119 , 'payload' : payload}
        recieved=self.recieve_handler(send)
        if recieved['command']== 300:
            self.sock.close()

###########################################################

    def find_your_place(self,shareFile,payload,command):
        
        send={'id' : shareFile.ID,'ip':shareFile.HOST, 'command' : command , 'payload' : payload }
        recieved=self.recieve_handler(send)

        if recieved['command'] == 400 or recieved['command'] == 300 : 
            self.sock.close()



    def recognize_pre_next_nextnext(self,shareFile):
        send={'id' : shareFile.ID,'ip':shareFile.HOST, 'command' : 205  }
        recieved=self.recieve_handler(send)

        if  recieved['command'] == 400 : 
            self.sock.close()

    def sending_your_needs (self,shareFile,payload):

        send={'id' : shareFile.ID,'ip':shareFile.HOST, 'command' : 206 , 'payload' : payload }
        recieved=self.recieve_handler(send)
        if  recieved['command'] == 300 : 
            self.sock.close()

    def find_peers(self,shareFile,payload,command):
        
        send={'id' : shareFile.ID,'ip':shareFile.HOST, 'command' : command , 'payload' : payload }
        recieved=self.recieve_handler(send)

        if  recieved['command'] == 400 or  recieved['command'] == 300 : 
            self.sock.close()

    def who_is_responsible(self,shareFile,payload):
        send={'id' : shareFile.ID,'ip':shareFile.HOST, 'command' : 220 , 'payload' : payload }
        recieved=self.recieve_handler(send)

        if  recieved['command'] == 400 or  recieved['command'] == 300 : 
            self.sock.close()

    def find_seeder(self,shareFile,payload):
        send={'id' : shareFile.ID,'ip':shareFile.HOST, 'command' : 230 , 'payload' : payload }
        recieved=self.recieve_handler(send)

        if  recieved['command'] == 400 or  recieved['command'] == 300 : 
            self.sock.close()

        


    def return_the_seeders(self,shareFile,payload):
        send={'id' : shareFile.ID,'ip':shareFile.HOST, 'command' : 231 , 'payload' : payload }
        recieved=self.recieve_handler(send)

        if  recieved['command'] == 400 or  recieved['command'] == 300 : 
            self.sock.close()


    def get_file(self,shareFile,payload):
        send={'id' : shareFile.ID,'ip':shareFile.HOST, 'command' : 232 , 'payload': payload }
        jhandler = jsonhandler.JsonHandler()
        self.sock.sendall(jhandler.dic_to_json(send))
        data=self.sock.recv(280000)
        f,s=payload['name'].split('.')
        with open(str(shareFile.HOST)+'/'+f+'_'+str(payload['chunk'])+'.'+s, 'wb+') as file:
                file.write(data)

    
    def get_ready_for_download(self,shareFile,payload):

        send={'id' : shareFile.ID,'ip':shareFile.HOST, 'command' : 240,'payload' : payload }
        recieved=self.recieve_handler(send)

        if  recieved['command'] == 400 or  recieved['command'] == 300 : 
            self.sock.close()

        


        
        






    
    










        





        







    






    





