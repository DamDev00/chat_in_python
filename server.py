import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
import os
import threading
import json
import socket

clients = []
nicknames = {}

def broadcast(message: str, sender: socket.socket) -> None:
    for client in clients:
        if client == nicknames[str(client.getpeername()[1])][0]:
            client.send('You: '.encode() + message)
        else:
            client.send(f'{nicknames[str(client.getpeername()[1])][1]}: '.encode() + message)

def receve(client: socket.socket, address: str) -> None:
    connected = True
    while connected:

        msg = client.recv(64)
        
        if msg.decode('utf-8') == 'exit':
            broadcast(f"[{address}]: left the chat", sender=client)
            client.close()
        else:
            msg.decode('utf-8')
            print(f"[from [{address}]: {msg}]")
            broadcast(message=msg, sender=client)

def start_server(port: int) -> None:

    FORMAT = 'utf-8'
    HEADER = 1024

    addr = ('127.0.0.1', port)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(addr)
    server.listen()
    print('listen...')

    while True:

        client, address = server.accept()
        nickname = client.recv(1024).decode('utf-8')
        nicknames[str(address[1])] = [client, nickname]
        print(client.getpeername()[1])
        print(nicknames[str(address[1])][0])
        thread = threading.Thread(target=receve, args=[client, address]).start()
        clients.append(client)
        broadcast(message=f"{nickname}: join in the chat\n".encode(), sender=client)



class GUI_active_server():

    title = "chat server"
    width = 200
    height = 200

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(self.title)
        self.root.geometry(f"{self.width}x{self.height}")
        self.window_resizable(False)
        self.set_bg('white')
        self.layout()
        self.root.mainloop()
    def window_resizable(self, value: bool) -> None:
        if not value:
            self.root.resizable(False, False)
        else:
            pass
    def input_port(self, frame) -> None:
        input = tk.Entry(frame ,width=10, height=5, bg="purple")
        input.grid(row=0, column=0)
    def set_bg(self, color='white') -> None:
        if color:
            try:
                self.root.config(bg=color)
            except Exception:
                self.root.config(bg='white')

    def layout(self) -> None:
        label_frame = tk.Frame(self.root, width=self.width-20, height=self.height-20, bg='white')
        label_frame.pack(padx=10, pady=10)
        

        label = tk.Label(label_frame ,text='Insert port', font=('Times New Roman', 10), bg='white')
        label.pack()
     
        input = tk.Entry(label_frame, font=('calibri', 10), width=6)
        input.pack(padx=0, pady=label_frame.winfo_width()-label_frame.winfo_width() + 20)

        button = tk.Button(
            label_frame, width=5, height=1, text='click',
            command=lambda: self.fetch_port(input=input)
                )
        button.pack(padx=0, pady=0)    
       
    def fetch_port(self, input: tk.Entry) -> None:

        value = input.get()
        
        if self.verify_port(value) == True:
            self.root.destroy()
            start_server(port=int(value))
        else:
            exit(1)
        
    def verify_port(self, port) -> bool:
            EXTENSION = 'json'
            NAME_FILE = 'ports'
            CURRENT_SRC = os.getcwd()

            try:
                if type(port) is not int:
                    port = int(port)
            except Exception:
                messagebox.showerror('Error port', 'You must to insert a number')
                exit(1)
            
            if os.path.exists(f"{CURRENT_SRC}\{NAME_FILE}.{EXTENSION}"):
                print('FILE PRESENT')
                with open(f"{CURRENT_SRC}\{NAME_FILE}.{EXTENSION}", 'r') as file:
                    read_file = file.read()
                    json_load = json.loads(read_file)
                    json_load = dict(json_load).items()
                    for index, port_number in json_load:
                        if port == port_number:
                            messagebox.showerror('Error port', 'This port is not avalaible')
                            print('ERROR')
                            exit(1)
                    print('PORT AVALAIBLE')
                    return True
            else:
                messagebox.showerror('Error code', 'file not searched')
                exit(1)
            return False

gui = GUI_active_server()
