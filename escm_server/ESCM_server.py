import zmq
import subprocess


class ESCM_server():
    def __init__(self):
        self.socket_port = 8000
        self.ELOG_port = 8020
    
          
    def run(self):
        self.ctx = zmq.Context()
        self.master = self.ctx.socket(zmq.REP)
        self.master.bind('tcp://*:'+str(self.socket_port))

        while True:
            request = self.master.recv_json()
            #print(request)
            
            keys = request.keys()
            if 'entry_ID' in keys and 'message' in keys and 'elogname' in keys:
                status,ID,answer = self.send_edit(request['elogname'],request['entry_ID'],request['message'])
                self.master.send_json({'status':status,'ID':ID,'answer':answer})

            elif 'elogname' in keys and 'arguments' in keys and 'message' in keys:
                status,ID,answer = self.send(request['elogname'],request['arguments'],request['message'])
                self.master.send_json({'status':status,'ID':ID,'answer':answer})

            else:
                self.master.send_json({'status':'fail','ID':'','answer':'missing one between elogname-arguments-message-entry_ID!'})


    def send(self,elogname,arg,msg):

        cmd = 'elog '
        for arg_key in arg.keys():
            cmd += '-a '+arg_key+'=\"'+arg[arg_key]+'\" '
        cmd+='-h localhost -p '+str(self.ELOG_port)+' -l '+elogname+' \"'+msg+'\"'
        print("sent to elog -> ",cmd)
        answer = subprocess.check_output(cmd, shell=True,text=True)
        # print("answer from elog -> ",answer)

        status = 'fail'
        ID = ''
        if 'Message successfully transmitted' in answer:
            status='success'
        if status == 'success':
            ID = answer.split('ID=')[1][:-1]
        return status,ID,answer

    def send_edit(self,elogname,entry_ID,msg):

        cmd = 'elog '
        cmd += '-e '+entry_ID
        cmd +=' -h localhost -p '+str(self.ELOG_port)+' -l '+elogname+' \"'+msg+'\"'
        print("edit sent to elog -> ",cmd)
        answer = subprocess.check_output(cmd, shell=True,text=True)
        # print("answer from elog -> ",answer)

        status = 'fail'
        ID = ''
        if 'Message successfully transmitted' in answer:
            status='success'
        if status == 'success':
            ID = answer.split('ID=')[1][:-1]
        return status,ID,answer