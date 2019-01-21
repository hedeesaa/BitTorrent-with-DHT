import sched, time
import os
import time
import socket
import threading
import client


class Pinger: 

    def timer(self,shareFile,count):
        s = sched.scheduler(time.time, time.sleep)
        s.enter(10, 1, self.pinger, (s,shareFile,count))
        s.run()

    def pinger(self,s,shareFile,count):
        pingstatus='' 
        if 'first' in shareFile.next_peers :


            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((shareFile.next_peers['first']['ip'],65432))
            if result == 0:
                pingstatus="Port is open"
            else:
                count=count+1 
                pingstatus="Port is close"
                if count == 5 : 
                    
                    del shareFile.next_peers['first']
                    shareFile.next_peers['first'] = shareFile.next_peers['second']
                    connect_to = shareFile.next_peers['first']['ip']
                    t1=threading.Thread(target=client.Client(shareFile, connect_to).get_the_next_node,args=(shareFile,))
                    t1.daemon=True
                    t1.start()

                    payload = shareFile.next_peers['first'] 
                    connect_to = shareFile.previous_node['node']['ip']
                    t1=threading.Thread(target=client.Client(shareFile, connect_to).change_your_next_next,args=(shareFile,payload))
                    t1.daemon=True
                    t1.start()

                    
                        

            print("from ",shareFile.next_peers['first']['ip'] , pingstatus)
        s.enter(10, 1, self.pinger, (s,shareFile,count))


