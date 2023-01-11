import os

# Class Topic
# Represents a topic created when a subscriber subscribes to a given topic.
class Topic:
    def __init__(self, name, subs=[], messages=[], subs_next_message={}) -> None:
        # Topic ID
        self.name = name

        # Arrays/Dictionary to save information about the topic
        self.subs = subs #list of sub_ids
        self.messages = messages #list of all topic messages
        self.subs_next_message = subs_next_message #dictionary: key-sub_id value-next message index

        # Create directory to save topic in persistent memory
        if not os.path.isdir('topics/' + self.name):
           os.mkdir('topics/' + self.name)

        subs_file = open('topics/' + self.name + "/subscribers.txt", "w")
        for i in self.subs:
            subs_file.write(i + ' ' + str(self.subs_next_message[i]) + '\n')
        subs_file.close()
        
        msgs_file = open('topics/' + self.name + "/messages.txt", "w")
        for i in self.messages:
            msgs_file.write(i+"\n")
        msgs_file.close()

        print('Topic ' + name + ' created successfully!')

    # Garbage Collection
    def collect_garbage(self):
        lowest_index = min(list(self.subs_next_message.values()))
        
        if (lowest_index == 0):
            return "Can't remove any messages from topic"

        for i in range(0, lowest_index):
            with open("topics/" + self.name + "/messages.txt", "r") as f:
                lines = f.readlines()
            with open("topics/" + self.name + "/messages.txt", "w") as f:
                for line in lines:
                    if line.strip("\n") != self.messages[i]:
                        f.write(line)
                    else:
                        print("removed message: " + str(i))
                f.close()

            del self.messages[i]

        for key, value in self.subs_next_message.items():
            self.subs_next_message[key] = value - lowest_index

        subs_file = open('topics/' + self.name + "/subscribers.txt", "r")
        lines = subs_file.readlines()
        subs_file = open('topics/' + self.name + "/subscribers.txt", "w")
        for line in lines:
            sub_id = line.split()[0]
            val = line.split()[1]
            subs_file.write(str(sub_id) + ' ' + str(int(val) - lowest_index) + '\n')
        subs_file.close()

        return 0

    # Add a subscriber to topic
    def add_sub(self, sub_id):
        print(self.subs, sub_id)
        if sub_id in self.subs:
            print("Subscriber " + sub_id + " already subscribed to topic " + self.name)
            return 0

        self.subs.append(sub_id)
        self.subs_next_message[sub_id] = 0
        file = open('topics/' + self.name + "/subscribers.txt", "a")
        file.write(sub_id + " 0\n")
        file.close()
        return 1

    # Add a message to topic
    def add_message(self, message):
        self.messages.append(message)
        file = open('topics/' + self.name + "/messages.txt", "a")
        file.write(message + "\n")
        file.close()

    def remove_sub(self, unsub_id):
        if unsub_id not in self.subs:
            print("Subscriber " + unsub_id + " already unsubscribed to topic " + self.name)
            return 0
        self.subs_next_message.pop(unsub_id)
        self.subs.remove(unsub_id)
        
        #remove from subs file
        with open("topics/" + self.name + "/subscribers.txt", "r") as f:
            lines = f.readlines()
        with open("topics/" + self.name + "/subscribers.txt", "w") as f:
            for line in lines:
                if line.split()[0] != str(unsub_id):
                    f.write(line)
            f.close()

        return 1

    def get_msg(self, sub_id):
        if sub_id not in self.subs:
            print("Subscriber " + sub_id + " not subscribed to topic " + self.name)
            return 0
        
        nextmsgidx = self.subs_next_message[sub_id]

        subs_file = open('topics/' + self.name + "/subscribers.txt", "r")
        lines = subs_file.readlines()
        subs_file = open('topics/' + self.name + "/subscribers.txt", "w")
        for line in lines:
            if line.split()[0] == str(sub_id):
                if self.subs_next_message[sub_id] < len(self.messages):
                    subs_file.write(str(sub_id) + ' ' + str(nextmsgidx+1) + '\n')
                else:
                    subs_file.write(str(sub_id) + ' ' + str(nextmsgidx) + '\n')
            else:
                subs_file.write(line)
        subs_file.close()

        if(nextmsgidx >= len(self.messages)):
            return 'No more messages from topic ' + self.name

        message = self.messages[nextmsgidx]

        if self.subs_next_message[sub_id] < len(self.messages): 
            self.subs_next_message[sub_id] += 1
            self.collect_garbage()
            return message
        return 'No more messages from topic ' + self.name
        