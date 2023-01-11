import sys
import zmq
import zmq_utils


# Class Subscriber (REQ)
# Subscribe and unsubscribe topics
# Get messages from topics that is subscribes to
class Subscriber:
    def __init__(self, id) -> None:
        self.id = id

        # Create a Subscriber socket
        self.context = zmq.Context()
        self.proxy_socket = self.context.socket(zmq.REQ)
        self.proxy_socket.connect('tcp://localhost:5555')


    def subscribe(self, topic):
        # Subscribe to message of the given topic
        subs_message = 'sub ' + topic + ' ' + str(self.id)
        res = zmq_utils.client_process_msg(self.context, self.proxy_socket , subs_message)
        if res != -1:
            print(res)
        else:
            sys.exit()
            
    def unsubscribe(self, topic):
        # Subscribe to message of the given topic
        uns_message = 'unsub ' + topic + ' ' + str(self.id)

        res = zmq_utils.client_process_msg(self.context, self.proxy_socket , uns_message)
        if res != -1:
            print(res)
        else:
            sys.exit()

    def get(self, topic):
        # Get message of the given topic
        get_message = 'get ' + topic + ' ' + str(self.id)

        res = zmq_utils.client_process_msg(self.context, self.proxy_socket , get_message)
        if res != -1:
            print(res)
        else:
            sys.exit()



arguments = sys.argv[1:]
# print(arguments)

if len(arguments) != 1:
    print("Error: run as '$ python subscriber.py <id>'")
    sys.exit(0)

if not arguments[0].isdigit():
    print("Error: <id> needs to be a digit")
    sys.exit(0)

sub = Subscriber(arguments[0])

while True:
    print("Options:\n   1 - subscribe <topic>\n   2 - unsubscribe <topic>\n   3 - get <topic>")
    
    command = input("Enter one of the options (-1 to exit): ")
    command_arr = command.split()

    if (command_arr[0] == "-1"):
        sys.exit(0)
    elif (len(command_arr)!=2):
        print('Error: commands have 1 argument')
    elif command_arr[0] == 'subscribe':
        sub.subscribe(command_arr[1])
    elif command_arr[0] == 'unsubscribe':
        sub.unsubscribe(command_arr[1])
    elif command_arr[0] == 'get':
        sub.get(command_arr[1])
    else:
        print('Error: command_arr not recognized')
