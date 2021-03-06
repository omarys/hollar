from time import sleep
from tkinter import (
    Tk,
    Frame,
    Scrollbar,
    Label,
    END,
    Entry,
    Text,
    VERTICAL,
    Button,
    mainloop,
    messagebox,
)
import socket
import threading


class ChatClient:
    # this is meant to hold your socket.  Access it with self.socket
    socket = None

    run = True

    # this is meant to hold your gui.  Add items to the gui with self.gui["<itemname">] = <itemfunction>
    gui = {}

    # this is your class constructor, it should set up the class
    def __init__(self, ip, port):
        self.gui["chat_transcript_area"] = None
        self.gui["name_widget"] = None
        self.gui["enter_text_widget"] = None
        self.gui["join_button"] = None
        self.address = (ip, port)
        self.root = Tk()
        self.connect_to_server()
        self.create_gui()
        self.receive_message()
        self.root.protocol("WM_DELETE_WINDOW", self.close_chat)
        self.root.mainloop()

    # this function should get called by __init__ and create the socket, then assign the socket to self.socket
    def connect_to_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.address)

    # this function should call other functions to build your gui
    def create_gui(self):
        self.gui["title"] = "hollar"
        self.gui["root.resizable"] = (0, 0)
        self.display_chat_box()
        self.display_name_section()
        self.display_chat_entry_box()

    # this function should be in it's own thread and it should listen on the socket for a message
    def receive_message(self):
        self.thread = threading.Thread(
            target=self.receive_message_from_server, args=(self.socket,)
        )
        self.thread.start()

    def receive_message_from_server(self, so):
        while self.run:
            buffer = so.recv(256)
            if not buffer:
                sleep(0.1)
                continue
            message = buffer.decode("utf-8")
            # client = ChatClient(root)
            # root.protocol("WM_DELETE_WINDOW", client.close_chat)
            if "joined" in message:
                user = message.split(":")[1]
                message = user + " has joined"
                self.gui["chat_transcript_area"].insert("end", message + "\n")
                self.gui["chat_transcript_area"].yview(END)
            else:
                self.gui["chat_transcript_area"].insert("end", message + "\n")
                self.gui["chat_transcript_area"].yview(END)

        so.close()

    def display_name_section(self):
        frame = Frame()
        Label(frame, text="What's your name?: ", font=("Serif", 16)).pack(
            side="left", padx=10
        )
        self.gui["name_widget"] = Entry(frame, width=50, borderwidth=2)
        self.gui["name_widget"].pack(side="left", anchor="e")
        self.gui["join_button"] = Button(
            frame, text="Join", width=10, command=self.on_join
        ).pack(side="left")
        frame.pack(side="top", anchor="nw")

    def display_chat_box(self):
        frame = Frame()
        Label(frame, text="Messages: ", font=("Serif", 12)).pack(side="top", anchor="w")
        self.gui["chat_transcript_area"] = Text(
            frame, width=60, height=10, font=("Serif", 12)
        )
        scrollbar = Scrollbar(
            frame, command=self.gui["chat_transcript_area"].yview, orient=VERTICAL
        )
        self.gui["chat_transcript_area"].config(yscrollcommand=scrollbar.set)
        self.gui["chat_transcript_area"].bind("<KeyPress>", lambda e: "break")
        self.gui["chat_transcript_area"].pack(side="left", padx=10)
        scrollbar.pack(side="right", fill="y")
        frame.pack(side="top")

    def display_chat_entry_box(self):
        frame = Frame()
        Label(frame, text="Message: ", font=("Serif", 12)).pack(side="top", anchor="w")
        self.gui["enter_text_widget"] = Text(
            frame, width=60, height=3, font=("Serif", 12)
        )
        self.gui["enter_text_widget"].pack(side="left", pady=15)
        self.gui["enter_text_widget"].bind("<Return>", self.on_enter_key_pressed)
        frame.pack(side="top")

    def on_join(self):
        if len(self.gui["name_widget"].get()) == 0:
            messagebox.showerror("Enter your name", "Enter your name to send a message")
            return
        self.gui["name_widget"].config(state="disabled")
        self.socket.send(("joined: " + self.gui["name_widget"].get()).encode("utf-8"))

    def on_enter_key_pressed(self, evt):
        if len(self.gui["name_widget"].get()) == 0:
            messagebox.showerror("Enter your name", "Enter your name to send a message")
            return
        self.send_message()
        self.clear_text()

    def clear_text(self):
        self.gui["enter_text_widget"].delete(1.0, "end")

    # this function should get called when you want to send a message
    def send_message(self):
        senders_name = self.gui["name_widget"].get().strip() + ": "
        data = self.gui["enter_text_widget"].get(1.0, "end").strip()
        message = (senders_name + data).encode("utf-8")
        self.gui["chat_transcript_area"].yview(END)
        self.socket.send(message)
        self.gui["chat_transcript_area"].insert("end", message.decode("utf-8") + "\n")
        self.gui["chat_transcript_area"].yview(END)
        self.gui["enter_text_widget"].delete(1.0, "end")
        return "break"

    # this function should get called when you want to close your app
    def close_chat(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            self.run = False
            self.thread.join()
            self.root.destroy()
            self.socket.close()
            exit(0)


def main():
    ip = "127.0.0.1"
    port = 9001
    chat = ChatClient(ip, port)

if __name__ == "__main__":
    main()