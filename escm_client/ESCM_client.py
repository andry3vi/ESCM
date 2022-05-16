import zmq


class ESCM_client():

    def __init__(self,server_IP,elogname):

        self.socket_port = 8000
        self.server_IP = server_IP
        self.elogname = elogname
        self.queue = list()
        
    def new_message(self,arguments,message):
        
        entry = message_entry()
        entry.fill_new(self.elogname,arguments,message)
        self.queue.append(entry)
    
    def send_last(self):
        packet = self.queue[-1].get_json()
        
        ctx = zmq.Context()
        client = ctx.socket(zmq.REQ)
        if packet is not None:
            client.connect('tcp://'+self.server_IP+':'+str(self.socket_port))
            client.send_json(packet)
            answer = client.recv_json()
            self.queue[-1].fill_answer(answer['ID'],answer['answer'])
            client.close()
    
    def update_last(self,message):

        new_msg = self.queue[-1].message + message
        self.queue[-1].modify_message(new_msg)
    
    def clear_list(self):
        self.queue.clear()


#send connection check



class message_entry():
    def __init__(self):
        self.message = ''
        self.elogname = ''
        self.arguments = dict()
        self.ID = ''
        self.answer = ''
        self.status = ''
    
    def fill_new(self,elogname,arguments,message):
        self.message = message
        self.arguments = arguments
        self.elogname = elogname
        self.status = 'new'
    
    def fill_answer(self,ID,answer):
        self.status = 'sent'
        self.ID = ID
        self.answer = answer

    def modify_message(self,message):
        self.message = message
        self.status = 'updated'

    def get_json(self):
        if self.status == 'new':
            return {'elogname':self.elogname,'arguments':self.arguments,'message':self.message}
        elif self.status == 'updated':
            return {'elogname':self.elogname,'entry_ID':self.ID,'message':self.message}
        else:
            return None