from tkinter import Tk

class ChatClient:

    #this is meant to hold your socket.  Access it with self.socket
    socket = None

    #this is meant to hold your gui.  Add items to the gui with self.gui["<itemname">] = <itemfunction>
    gui = {}

    #this is your class constructor, it should set up the class
    def __init__(self, ip, port):
        pass

    #this is your class' main function, it gets the party started, call it after __init__
    def main(self):
        pass

    #this function should call other functions to build your gui
    def create_gui(self):
        pass

    #this function should get called by __init__ and create the socket, then assign the socket to self.socket
    def connect_to_server(self):
        pass

    #this function should be in it's own thread and it should listen on the socket for a message
    def receive_message(self):
        pass

    #this function should get called when you want to send a message
    def send_message(self, message):
        pass

    #this function should get called when you want to close your app
    def close_chat(self):
        pass

def main():
    #Set up these variables to receive input
    ip = None
    port = None
    chat = ChatClient(ip, port)

if __name__ == "__main__":
    main()