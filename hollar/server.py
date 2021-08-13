import socket
import threading


class ChatServer:

    clients_list = []  # client ip+port array
    atomic_lock = (
        threading.Lock()
    )  # prevention of race conditions -> threads should finish rather than being forced to have the same amount of processing time/get stomped

    last_received_message = ""  # msg placeholder

    def __init__(self):
        self.server_socket = None  # socket lives here
        self.create_listening_server()  # method

    def create_listening_server(self):
        self.server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )  # IPv4 socket on TCP
        ip = "127.0.0.1"  # Server IP and port
        port = 9001  # It's over 9000

        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
        )  # SO_ - socket option # SOL_ - socket option level # Sets REUSEADDR (as a socket option) to 1 on socket
        self.server_socket.bind(
            (ip, port)
        )  # remote addr to local addr bind locally -> water is muddy given 127.0.0.1 util
        print("Listening for incoming messages...")  # msg to terminal
        self.server_socket.listen(
            5
        )  # listen for up to 5 QUEUED connections (doesn't limit active conns)
        self.receive_messages_in_thread()  # method

    def receive_messages_in_thread(self):
        while True:
            client = so, (
                ip,
                port,
            ) = self.server_socket.accept()  # accept set client connection
            self.add_to_clients(client)  # method
            print("Connected to ", ip, ":", str(port))  # terminal
            t = threading.Thread(
                target=self.receive_messages, args=(so,)
            )  # thread for msg reception
            t.start()

    def add_to_clients(self, client):
        if client not in self.clients_list:
            self.clients_list.append(client)  # add new client if new

    def receive_messages(self, so):
        while True:
            try:
                incoming_buffer = so.recv(256)  # ye olde buffer
                if not incoming_buffer:
                    break  # stop if non socket traffic
                self.atomic_lock.acquire()  # Lock processing to the following action(s)
                self.last_received_message = incoming_buffer.decode(
                    "utf-8"
                )  # Todo: check byte val before decoding
                self.broadcast_to_all(so)  # method
            except ConnectionResetError:
                for client in self.clients_list:  # step through clients
                    socket, (ip, port) = client  # set socket as array slotted value
                    if socket is so:
                        self.clients_list.remove(client)  # remove if they disconnected
                        self.atomic_lock.acquire()  # Lock processing to the following action(s)
                        self.last_received_message = (
                            ip + " : " + str(port) + " has disconnected"
                        )  # prep to push to all clients...this and below can be done client side if username is preferred
                        print("Disconnected ", ip, ":", str(port))  # terminal
                        self.broadcast_to_all(so)  # push
                        break  # done handling disconnect

    def broadcast_to_all(self, senders_socket):
        for client in self.clients_list:
            socket, (ip, port) = client  # set socket as array slotted value
            if socket is not senders_socket:
                socket.sendall(
                    self.last_received_message.encode("utf-8")
                )  # Todo: check byte val before decoding
        self.atomic_lock.release()  # Unlock processing


if __name__ == "__main__":
    ChatServer()  # run class obj
