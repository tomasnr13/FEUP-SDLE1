import sys
import os
import zmq
from topic import Topic

# Class Server
# Receives messages from Subscribers and Publishers
class Server:
    def __init__(self) -> None:
        # Create ROUTER socket
        context = zmq.Context()

        self.router = context.socket(zmq.ROUTER)
        self.router.bind("tcp://*:5555")

        # Create Poller to handle the messages
        self.poller = zmq.Poller()
        self.poller.register(self.router, zmq.POLLIN)

        # Create a directory to save topics
        self.topics = {} # Key --> topic name; Value --> topic object
        self.topics_key_view = self.topics.keys() # It will help check if a topic exists

    def read_topic(self):
        if not os.path.isdir('topics'):
            os.mkdir('topics')
            return 0
        
        dir = os.listdir('topics')
        for d in dir:
            subsF = []
            msgsF = []
            nextmsgF = {}
            with open("topics/" + d + "/subscribers.txt", "r") as f:
                lines = f.readlines()
                for i in lines:
                    i = i.split('\n')
                    s = i[0].split(' ')
                    subsF.append(s[0])
                    n = s[1]
                    nextmsgF[s[0]] = int(n)

            with open("topics/" + d + "/messages.txt", "r") as f:
                lines = f.readlines()
                for i in lines:
                    i = i.split("\n", 1)
                    if (i[0]!='\n'):
                        msgsF.append(i[0])

            self.topics[d] = Topic(d, subs=subsF, messages=msgsF, subs_next_message=nextmsgF)
            self.topics_key_view = self.topics.keys()

    def run(self):
        self.read_topic()
        try:
            while True:
                try:
                    socks = dict(self.poller.poll(2))
                except zmq.ZMQError:
                    break
                if socks.get(self.router) == zmq.POLLIN:
                    message = self.router.recv_multipart()
                    self.parse_msg(message)
        except KeyboardInterrupt:
            print('Aborting server...')
            self.router.close()
            print('Aborted')
            sys.exit()
    
            
    def parse_msg(self, msg_bytes):
        message = msg_bytes[2].decode('utf-8').split(" ", 2)
        reply = 'ERROR: Incorret Message Format. Message received: ' + str(message)
        res = 1
        print('Operation: ' + message[0])
        print('Topic: ' + message[1])
        print('Argument: ' + message[2])
        # SUB MESSAGE
        if message[0] == 'sub':
            topic_name = str(message[1])
            sub_id = str(message[2])
            
            if topic_name in self.topics_key_view:
                # If topic already exits, just add a new sub
                res = self.topics[topic_name].add_sub(sub_id)

            else:
                # Create new topic
                new_topic = Topic(topic_name, subs=[], messages=[])
                # Add new topic to dict
                self.topics[topic_name] = new_topic
                # Add first subcriber
                res = self.topics[topic_name].add_sub(sub_id)
            
            if not res:
                reply = 'Already subscribed topic ' + topic_name
            else:
                reply = 'Subscribed topic ' + topic_name + ' successfully'

        # PUT MESSAGE
        if message[0] == 'put':
            topic_name = str(message[1])
            content = str(message[2])
            
            if topic_name in self.topics_key_view:
                self.topics[topic_name].add_message(content)
                reply = 'Message saved'
            else:
                reply = 'ERROR: Topic ' + topic_name + ' does not exist'

        #GET MESSAGE
        if message[0] == 'get':
            topic_name = str(message[1])
            get_id = str(message[2])
            if topic_name in self.topics_key_view:
                # If topic already exits, get msg
                res = self.topics[topic_name].get_msg(get_id)
                if not res:
                    reply = 'There are no messages available'
                else:
                    reply= 'Message: ' + str(res)
            else:
                reply = 'Topic ' + topic_name + ' does not exist'

        #UNSUB MESSAGE
        if message[0] == 'unsub':
            topic_name = str(message[1])
            unsub_id = str(message[2])
            if topic_name in self.topics_key_view:
                # If topic already exits, just add a new sub
                res = self.topics[topic_name].remove_sub(unsub_id)
            if not res:
                reply = 'Already unsubscribed topic ' + topic_name
            else:
                reply = 'Unsubscribed topic ' + topic_name + ' successfully'
                

        self.router.send_multipart([msg_bytes[0], b'', reply.encode('utf-8')])
        print("Received: " + str(message) + " --> Replied: " + reply)




arguments = sys.argv[1:]
# print(arguments)

if len(arguments) != 0:
    print("Error: run as '$ python server.py'")
    sys.exit(0)

server = Server()
server.run()