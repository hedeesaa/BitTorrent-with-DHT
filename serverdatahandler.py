import jsonhandler
import commands

class ServerDataHandler:

    def data_handler(self,data,sharedFile):

        jhandler=jsonhandler.JsonHandler()
        com=commands.Commands()
        dic_data=jhandler.json_to_dic(data)

        result=com.protocols(dic_data,sharedFile)
        respond = None


        if result == 113 :  
            respond = {'id':sharedFile.ID, 'ip':sharedFile.HOST ,
                      'command' : result , 'payload': sharedFile.next_peers['first']}

        elif result == 233 : 
            return com.temp

        else : 
            respond = {'id':sharedFile.ID, 'ip':sharedFile.HOST ,
                      'command' : result}
        

        

        return jhandler.dic_to_json(respond)

