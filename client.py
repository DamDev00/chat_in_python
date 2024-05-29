import socket
import tkinter as tk
import threading
import time

Lock = threading.Lock()
condition = threading.Condition(Lock)

class GUI_active_client():

    title = "chat client"
    width = 400
    height = 400
    

    def __init__(self) -> None:
        values = self.initialize()
        print('setting...')
        time.sleep(2)
        self.root = tk.Tk()
        self.root.title(self.title)
        self.root.geometry(f"{self.width}x{self.height}")
        self.window_resizable(False)
        self.layout(values=values)
        self.root.mainloop()

    def initialize(self) -> dict[str, str, str]:
        def submit_data():
            nonlocal nickname, ip, port
            nickname = nickname_entry.get()
            ip = ip_entry.get()
            port = port_entry.get()
            
            root_init.destroy()
            

        root_init = tk.Tk()

        nickname = ip = port = ""

        nickname_label = tk.Label(root_init, text="Nickname:")
        nickname_label.pack()

        nickname_entry = tk.Entry(root_init)
        nickname_entry.pack()

        ip_label = tk.Label(root_init, text="IP Address:")
        ip_label.pack()

        ip_entry = tk.Entry(root_init)
        ip_entry.pack()

        port_label = tk.Label(root_init, text="Port Number:")
        port_label.pack()

        port_entry = tk.Entry(root_init)
        port_entry.pack()

        submit_button = tk.Button(root_init, text="Submit", command=submit_data)
        submit_button.pack()

        root_init.mainloop()
        return {
            "nickname" : nickname,
            "ip" : ip,
            "port" : port
        }
    
    def layout(self, values: dict) -> None:
        text_area = tk.Text(self.root, width=40, height=15)
        text_area.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        entry = tk.Entry(self.root, font=('Times New Roman', 15), width=25)
        entry.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        sock = self.start_client(text=text_area, values=values)

        button = tk.Button(self.root, text='Click', width=10, height=2, fg='black',
                           command=lambda: self.send_message(sender=sock,input=entry, text=text_area))
        button.grid(row=1, column=1, padx=10, pady=10, sticky='e')

    def window_resizable(self, value: bool) -> None:
        if not value:
            self.root.resizable(False, False)
        else:
            pass
    def receve(self, conn: socket.socket, text: tk.Text) -> None:

        connected = True
        while connected:
            msg = conn.recv(64)
            if msg:
                text.insert(tk.END, msg.decode('utf-8'))

    def send_message(self, sender: socket.socket, input: tk.Entry, text: tk.Text) -> None:
        
        msg = input.get() + '\n'
        input.delete(0, tk.END)
        #text.insert(tk.END, msg)
        sender.send(msg.encode())


    def start_client(self, text: tk.Text, values: dict) -> socket.socket:

        ip = values['ip']
        port = int(values['port'])
        nickname = values['nickname']
        
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((ip, port))
        connection.send(str(nickname).encode())
        thread = threading.Thread(target=self.receve, args=[connection, text]).start()

        return connection
    
gui = GUI_active_client()
