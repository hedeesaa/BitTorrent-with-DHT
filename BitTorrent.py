import commands 
import staticnode
import shared
import dynamiccommands 
import os
import shutil




def start(inputs,sharedFile):

    sharedFile.HOST = inputs.ip

    if os.path.exists(sharedFile.HOST):
        shutil.rmtree(sharedFile.HOST)
    os.mkdir(sharedFile.HOST)
    os.mkdir(sharedFile.HOST+'/output/')


    if inputs.create == 'static' :
        
        sharedFile.ID=int(inputs.id)
        
        if inputs.nextpeerip !=None :
            sharedFile.next_peers['first']={'id':int(inputs.nextpeerid),
                                           'ip': inputs.nextpeerip}

        staticnode.StaticNode(sharedFile)    


    if inputs.create == 'dynamic' : 
        
        
        path=inputs.file 
        sharedFile.gateway,firstnode,secondnode=dynamiccommands.DynamicCommands().finding_target(path)
        sharedFile.ID=dynamiccommands.DynamicCommands().finding_node(firstnode,secondnode)
        sharedFile.firstnode = firstnode
        sharedFile.secondnode = secondnode

        print("IN THE NAME OF GOD : " ,sharedFile.ID)
        staticnode.StaticNode(sharedFile)


def start_share():
    sharedFile=shared.Shared()
    return sharedFile


if __name__ == "__main__":

    command = commands.Commands()
    inputs=command.inputter()
    sharedFile=start_share()
    start(inputs,sharedFile)

