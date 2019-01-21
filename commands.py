import argparse
import json
import threading
import client
import dynamiccommands
import random
import hashlib


class Commands:

    temp=None


    def inputter(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("create", help="static or dynamic") #type of the node
        parser.add_argument("--ip",help="enter ip")               #ip of the node
        parser.add_argument("--id",help="enter id")               #id of the node
        parser.add_argument("-nid","--nextpeerid",metavar='',help="enter the id of the next peer") #next id
        parser.add_argument("-nip","--nextpeerip",metavar='',help="enter the ip of the next peer") #next IP
        parser.add_argument("--file",help="enter the path of the parent file") #parent file

        args=parser.parse_args() 
        return args 


    def md5hashing(self,filename):
        hasher = hashlib.md5()
        with open(filename,'rb')as open_file:
            content = open_file.read()
            hasher.update(content)

        return hasher.hexdigest()


    def pre_handler(self, shareFile,finding_pre,connect_to,payload):
        
        t=threading.Thread(target=client.Client(shareFile,connect_to).changing_the_pre,args=(shareFile,payload,finding_pre))
        t.daemon=True
        t.start()

    def next_next_handler(self,shareFile,payload,connect_to):
        t=threading.Thread(target=client.Client(shareFile,connect_to).change_your_next_next,args=(shareFile,payload))
        t.daemon=True
        t.start()

    def find_place_handler(self,shareFile,payload,command,connect_to):

        t=threading.Thread(target=client.Client(shareFile,connect_to).find_your_place,args=(shareFile,payload,command))
        t.daemon=True
        t.start()


    def protocols(self,data,shareFile):

        pls_sending_next_node = 112          #STATIC
        here_is_next_node = 113
        there_is_no_next = 114 

        finding_pre = 115
        i_am_your_pre = 116

        changing_next_next = 119             #STATIC

        OK=300
        CLOSE=400

        ########################

        finding_place = 200
        your_place_is_ok=201
        change_your_id = 202

        recognize_pre_and_next = 205
        sending_pre_and_next= 206

        ########################

        finding_peers = 210
        i_love_to =211

        ########################
        are_you_responsible = 220
        
        
        ########################

        get_the_seeders = 230
        returning_seeders = 231
        get_file = 232
        i_am_sending = 233
        ########################

        get_ready=240


        ####################### handle next next node

        if data['command'] == pls_sending_next_node :
            if not shareFile.previous_node or  (shareFile.previous_node['node']['id'] > data['id']): 
                shareFile.previous_node.clear()
                shareFile.previous_node['node']={'id':data['id'],'ip':data['ip']}
                

            if 'first' in shareFile.next_peers : 
                return here_is_next_node
            else : 
                return there_is_no_next

        ######################## handle pre node

        if data['command'] == finding_pre :
            if shareFile.previous_node['node']['id'] == data['payload']['id'] :

                 if not shareFile.next_peers : 
                    shareFile.next_peers['first']={'id':data['payload']['id'],'ip':data['payload']['ip']}
                    connect_to = shareFile.next_peers['first']['ip']
                    payload={'id':shareFile.ID,'ip':shareFile.HOST}
                    self.pre_handler(shareFile,i_am_your_pre,connect_to,payload)
                    

                 else:
                    connect_to = shareFile.next_peers['first']['ip']
                    payload = data['payload']
                    self.pre_handler(shareFile,finding_pre,connect_to,payload)
                     

            elif shareFile.previous_node['node']['id'] >=  shareFile.next_peers['first']['id'] :
                 shareFile.next_peers['second']=shareFile.next_peers['first']
                 shareFile.next_peers['first']=data['payload']

                 connect_to = shareFile.next_peers['first']['ip']
                 payload={'id':shareFile.ID,'ip':shareFile.HOST}
                 self.pre_handler(shareFile,i_am_your_pre,connect_to,payload)

                 connect_to = shareFile.previous_node['node']['ip']
                 payload=data['payload']
                 self.next_next_handler(shareFile,payload,connect_to)

            else : 
                 connect_to = shareFile.next_peers['first']['ip']
                 payload = data['payload']
                 self.pre_handler(shareFile,finding_pre,connect_to,payload)

            return CLOSE

        #################### found her pre
        if data['command'] == i_am_your_pre : 
            shareFile.previous_node['node'] = data['payload']

            return OK

        #################### change the next next becuase of adding
        if data['command'] == changing_next_next :
            shareFile.next_peers['second'] = data['payload']

            return OK




        #################### for dynamic

        if data['command'] == finding_place : 
            
            payload = data['payload']
            if data['payload']['id'] == shareFile.next_peers['first']['id'] or data['payload']['id'] == shareFile.next_peers['second']['id']:
                
                 
                connect_to=data['payload']['ip']
                command= change_your_id
                self.find_place_handler(shareFile,payload,command,connect_to)
                


            elif data['payload']['id'] < shareFile.next_peers['first']['id'] :
                
                
                connect_to=data['payload']['ip']
                command= your_place_is_ok
                payload = {'id':shareFile.ID , 'ip':shareFile.HOST}
                self.find_place_handler(shareFile,payload,command,connect_to)

            elif data['payload']['id'] < shareFile.next_peers['second']['id'] :
                connect_to=data['payload']['ip']
                command= your_place_is_ok
                payload = shareFile.next_peers['first']
                self.find_place_handler(shareFile,payload,command,connect_to)
                    
                    

            elif data['payload']['id'] > shareFile.next_peers['second']['id']:
                connect_to=shareFile.next_peers['second']['ip']
                command=finding_place
                self.find_place_handler(shareFile,payload,command,connect_to)

            elif data['payload']['id'] > shareFile.next_peers['first']['id'] :
                connect_to=shareFile.next_peers['first']['ip']
                command=finding_place
                self.find_place_handler(shareFile,payload,command,connect_to)
            
            return CLOSE




        if data['command'] == change_your_id : 
            shareFile.ID=dynamiccommands.DynamicCommands().finding_node(shareFile.firstnode,shareFile.secondnode)

            connect_to = shareFile.gateway['node']['ip']

            payload={'id' : shareFile.ID,'ip':shareFile.HOST}
            command= 200
            self.find_place_handler(shareFile,payload,command,connect_to)
            
            return OK


        if data['command'] == your_place_is_ok:
            shareFile.gateway['node']= data['payload']

            connect_to = shareFile.gateway['node']['ip']
            t=threading.Thread(target=client.Client(shareFile,connect_to).recognize_pre_next_nextnext,args=(shareFile,))
            t.daemon=True
            t.start()

            return OK

        if data['command'] == recognize_pre_and_next : 

            connect_to = data['ip']
            payload = {'first':shareFile.next_peers['first'] , 'second':shareFile.next_peers['second']}
            t=threading.Thread(target=client.Client(shareFile,connect_to).sending_your_needs,args=(shareFile,payload))
            t.daemon=True
            t.start()


            shareFile.next_peers['second']=shareFile.next_peers['first']
            shareFile.next_peers['first']={'id':data['id'],'ip':data['ip']}

            connect_to = shareFile.next_peers['second']['ip']
            payload = shareFile.next_peers['first']

            self.pre_handler(shareFile,i_am_your_pre,connect_to,payload)
            

            connect_to = shareFile.previous_node['node']['ip']
            payload = shareFile.next_peers['first']
            self.next_next_handler(shareFile,payload,connect_to)
            
            return CLOSE

        if data['command'] == sending_pre_and_next : 
            shareFile.next_peers = data['payload']
            shareFile.previous_node['node']={'id':data['id'], 'ip':data['ip']}

            return OK

        if data['command'] == finding_peers :
            counter = data['payload']['counter'] +1
            rand = random.randint(0,1)
            print("######### ",rand)
            if shareFile.ID == data['payload']['id'] or data['payload']['counter'] == 10 : 
                return CLOSE
            elif rand == 1 : 
                print("i love to")
                connect_to = data['payload']['ip']
                payload = {'id' : shareFile.ID , 'ip': shareFile.HOST, 'counter' : counter}
                t=threading.Thread(target=client.Client(shareFile,connect_to).find_peers,args=(shareFile,payload,i_love_to))
                t.daemon=True
                t.start()

           

            connect_to = shareFile.next_peers['first']['ip']
            payload = {'id' : data['payload']['id'] , 'ip': data['payload']['ip'], 'counter' : counter}
            t=threading.Thread(target=client.Client(shareFile,connect_to).find_peers,args=(shareFile,payload,finding_peers))
            t.daemon=True
            t.start()
            
            return CLOSE

        if data['command'] == i_love_to : 
            
            shareFile.peers.append({'id':data['payload']['id'], 'ip':data['payload']['ip']})
            
            return OK


        if data['command'] == are_you_responsible : 
            if shareFile.previous_node['node']['id']>shareFile.next_peers['first']['id'] :
                if shareFile.ID >= data['payload'][str(0)]['hash'] and shareFile.next_peers['first']['id'] > data['payload'][str(0)]['hash']:
                    
                    c = 0
                    print("i becomeeeeeeeeeeeee")
                    while c<len(data['payload']):
                        shareFile.database.append(data['payload'][str(c)])
                        c = c+1
                        
                    return OK
                else : 
                    connect_to=shareFile.next_peers['first']['ip']
                    payload = data['payload']
                    t=threading.Thread(target=client.Client(shareFile,connect_to).who_is_responsible,args=(shareFile,payload))
                    t.daemon=True
                    t.start()

            elif shareFile.ID >= data['payload'][str(0)]['hash'] and shareFile.previous_node['node']['id'] < data['payload'][str(0)]['hash'] : 
                
                c = 0
                print("i becomeeeeeeeeeeeee")
                while c<len(data['payload']):
                    shareFile.database.append(data['payload'][str(c)])
                    c = c+1

                return OK

            else :
                
                connect_to=shareFile.next_peers['first']['ip']
                payload = data['payload']
                t=threading.Thread(target=client.Client(shareFile,connect_to).who_is_responsible,args=(shareFile,payload))
                t.daemon=True
                t.start()

                return CLOSE

        if data['command'] == get_the_seeders : 
            if shareFile.previous_node['node']['id']>shareFile.next_peers['first']['id'] :
                 if shareFile.ID > data['payload']['hash'] and shareFile.next_peers['first']['id'] > data['payload']['hash']:
                     
                    
                     payload={}
                     c=0
                     for i in shareFile.database :
                         if i['hash'] == data['payload']['hash'] and  i['name'] == data['payload']['name']:
                             payload[c]=i
                             c=c+1

                     connect_to=data['payload']['ip']
               
                     t=threading.Thread(target=client.Client(shareFile,connect_to).return_the_seeders,args=(shareFile,payload))
                     t.daemon=True
                     t.start()


                     return CLOSE

                 else:
                     connect_to=shareFile.next_peers['first']['ip']
                     payload = data['payload']
                     t=threading.Thread(target=client.Client(shareFile,connect_to).find_seeder,args=(shareFile,payload))
                     t.daemon=True
                     t.start()

            elif shareFile.ID > data['payload']['hash'] and shareFile.previous_node['node']['id'] < data['payload']['hash'] :
                payload={}
                c=0
                for i in shareFile.database :
                    if i['hash'] == data['payload']['hash'] and  i['name'] == data['payload']['name']:
                        payload[c]=i
                        c=c+1

                connect_to=data['payload']['ip']
                t=threading.Thread(target=client.Client(shareFile,connect_to).return_the_seeders,args=(shareFile,payload))
                t.daemon=True
                t.start()

   
                return CLOSE

            else : 

                connect_to=shareFile.next_peers['first']['ip']
                payload = data['payload']
                t=threading.Thread(target=client.Client(shareFile,connect_to).find_seeder,args=(shareFile,payload))
                t.daemon=True
                t.start()

                return CLOSE

        if data['command'] == returning_seeders : 
            for i in data['payload']:
                shareFile.temp.append(data['payload'][i])
                count = 1
              
                for i in shareFile.temp :
                   
                    connect_to=i['ip']
                    payload = {'hash':i['hash'],'name':i['name'],'chunk':i['chunk']}
                    t=threading.Thread(target=client.Client(shareFile,connect_to).get_file,args=(shareFile,payload))
                    t.daemon=True
                    t.start()

           

        if data['command'] == get_file : 
            f,s=data['payload']['name'].split('.')

            with open(str(shareFile.HOST)+'/output/'+f+'_'+str(data['payload']['chunk'])+'.'+s, 'rb') as file_to_send:
                self.temp=file_to_send.read()
                
                return 233

        if data['command'] == get_ready:
            c = 0
            while c<len(data['payload']):
                connect_to=data['payload'][str(c)]['ip']
                payload = {'hash':data['payload'][str(c)]['hash'],'name':data['payload'][str(c)]['name'],'chunk':data['payload'][str(c)]['chunk']}
                t=threading.Thread(target=client.Client(shareFile,connect_to).get_file,args=(shareFile,payload))
                t.daemon=True
                t.start()
                
                c = c+1

            
            return 300


    

            





        

        
       
        

   

