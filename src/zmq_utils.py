import zmq
import sys
timeout = 1000
nr_tries = 5
endpoint = 'tcp://localhost:5555'

def client_process_msg(context, client , request_msg):
    retries_left = nr_tries
    request = str(request_msg).encode('utf-8')
    print("Sending...")

    try:
        client.send(request)

        while retries_left != 0:
            if (client.poll(timeout) & zmq.POLLIN) != 0:
                reply = client.recv()
                return reply.decode('utf-8')

            retries_left -= 1
            print("No response from server")
            # Socket is confused. Close and remove it.
            client.setsockopt(zmq.LINGER, 0)
            client.close()
            if retries_left == 0:
                print("Server seems to be offline, abandoning")
                return -1

            print("Reconnecting to server…")
            # Create new connection
            client = context.socket(zmq.REQ)
            client.connect(endpoint)
            print("Resending (%s)", request)
            client.send(request)
    except zmq.ZMQError:
        print('ZMQ error! Aborting...')
        sys.exit()
