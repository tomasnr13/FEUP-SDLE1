import sys
import zmq
import zmq_utils

# Class Publisher (REQ)
# Creates and publishes messages about a topic given
class Publisher:
    def __init__(self) -> None:
        # Create Publisher Socket
        self.context = zmq.Context()
        self.proxy_socket = self.context.socket(zmq.REQ)
        self.proxy_socket.connect('tcp://localhost:5555')

    def put(self, topic, msg) -> None:
        put_message = 'put ' + topic + ' ' + msg
        
        # self.proxy_socket.send(put_message.encode('utf-8'))
        # print("Sent message")

        # message = self.proxy_socket.recv().decode('utf-8')
        # if(message != 'Saved'):
        #     print(message)
        #     return
        res = zmq_utils.client_process_msg(self.context, self.proxy_socket , put_message)
        if res != -1:
            print(res)
        else:
            sys.exit()
        



arguments = sys.argv[1:]
# print(arguments)

if len(arguments) != 0:
    print("Error: run as '$ python publisher.py'")
    sys.exit(0)

pub = Publisher()

while True:
    topic_name = input("Enter topic name (-1 to exit): ")
    if (topic_name == "-1"):
        sys.exit(0)
    
    message = ''
    while True:
        message = input(f"Enter message to put in {topic_name} topic: ")
        if (len(message)==0):
            print("Error: message cannot be empty!")
        else:
            break

    pub.put(topic_name, message)