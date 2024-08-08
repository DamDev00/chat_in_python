import socket
from cryptography.fernet import Fernet
import threading
import tkinter as tk
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
from tkinter import scrolledtext
import subprocess

class WhatsAppChatInterface:
    def __init__(self, root, dates):

        self.root = root
        self.root.title("WhatsApp Chat Interface")

        # Set dimensioni della finestra
        self.root.geometry("400x600")
        self.root.resizable(False, False)

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((dates['ip'], int(dates['port'])))
        except:
            print(f"<ERROR SOCKET> -> {socket.error}")

        # Colori
        self.green_color = "#25D366"  # Verde per la barra superiore
        self.beige_color = "#ECE5DD"  # Beige per lo sfondo della chat

        # Creazione della barra verde in alto
        self.create_top_bar()

        # Creazione dell'area della chat
        self.create_chat_area()

        # Creazione del campo di input e del pulsante di invio
        self.create_message_input(client_socket)


        client_socket.send(str(dates['username']).encode())

        recever = threading.Thread(target=self.receve, args=(client_socket,))
        recever.start()

    def create_top_bar(self):
        # Barra verde in alto
        top_frame = tk.Frame(self.root, bg=self.green_color, height=50)
        top_frame.pack(fill=tk.X)

        # Etichetta nella barra superiore per il nome del contatto
        contact_label = tk.Label(top_frame, text="ChatServer 1.0", bg=self.green_color, fg="white", font=("Helvetica", 16, "bold"))
        contact_label.pack(pady=10, padx=10, anchor='w')

    def create_chat_area(self):
        # Area della chat con sfondo beige
        chat_frame = tk.Frame(self.root, bg=self.beige_color)
        chat_frame.pack(fill=tk.BOTH, expand=True)

        # Area di testo scorrevole per visualizzare i messaggi
        self.chat_area = scrolledtext.ScrolledText(chat_frame, bg=self.beige_color, fg="black", wrap=tk.WORD, font=("Helvetica", 12))
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.chat_area.config(state=tk.DISABLED)  # Disabilitato per impedire all'utente di modificarne il contenuto

    def create_message_input(self, client: socket.socket):
        # Campo di input per i messaggi
        message_frame = tk.Frame(self.root, bg=self.beige_color)
        message_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.message_entry = tk.Entry(message_frame, bg="white", fg="black", font=("Helvetica", 12))
        self.message_entry.pack(fill=tk.X, padx=10, pady=10, ipady=5)

        # Pulsante di invio
        send_button = tk.Button(message_frame, text="Invia", bg=self.green_color, fg="white", font=("Helvetica", 12), command=lambda : self.send_message(client=client))
        send_button.pack(side=tk.RIGHT, padx=10, pady=10)

        #self.message_entry.bind("<Return>", send_button)

    def send_message(self, client: socket.socket):
        message = self.message_entry.get()
        client.send(message.encode())
        self.message_entry.delete(0, tk.END)
    def receve(self,client: socket.socket) -> None:
        bytes_ = 4096
        while True:
            data = client.recv(bytes_).decode('utf-8')
            self.chat_area.config(state=tk.NORMAL)
            self.chat_area.insert(tk.END, f"{data}\n")
            self.chat_area.config(state=tk.DISABLED)
            self.chat_area.yview(tk.END)
            print(data)

    def sender(client: socket.socket) -> None:
        while True:
            data = str(input(' '))
            client.send(data.encode('utf-8'))
def startConnection(dates: dict) -> None:
    root = tk.Tk()
    app = WhatsAppChatInterface(root, dates)
    root.mainloop()
class ProfileApp:
    width = 400
    height = 408
    def __init__(self, root):
        self.root = root
        self.root.title("Profile App")
        self.root.geometry(f"{str(self.width)}x{str(self.height)}")  # Aumenta le dimensioni della finestra
        self.root.resizable(False, False)

        # Carica l'immagine di sfondo
        self.bg_image = Image.open("image.jpg")  # Assicurati di avere l'immagine di sfondo nello stesso percorso
        self.bg_image = self.bg_image.resize((400, 400))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Etichetta per l'immagine di sfondo
        self.bg_label = tk.Label(root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame per l'immagine del profilo e il pulsante
        self.frame = tk.Frame(root, bg="lightblue")
        self.frame.pack(pady=20)  # Aggiungi spazio verticale

        # Canvas per l'immagine tonda
        self.canvas = tk.Canvas(self.frame, width=120, height=120, bg="lightblue", highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=20)  # Aggiungi spazio orizzontale

        # Cerchio vuoto iniziale
        self.img = Image.new('RGB', (120, 120), color='white')
        self.img = ImageOps.fit(self.img, (120, 120), method=0, bleed=0.0, centering=(0.5, 0.5))
        self.img = ImageTk.PhotoImage(self.img)
        self.image_container = self.canvas.create_image(60, 60, image=self.img)

        # Pulsante per caricare l'immagine
        self.upload_btn = tk.Button(self.frame, text="Carica Immagine", command=self.upload_image)
        self.upload_btn.grid(row=0, column=1, padx=10)

        # Caselle di input
        self.username_label = tk.Label(root, text="Username:", bg="lightblue")
        self.username_label.pack(pady=10)  # Aggiungi spazio verticale
        self.username_entry = tk.Entry(root, width=30, textvariable='daminao')
        self.username_entry.pack(pady=5)

        self.ip_label = tk.Label(root, text="Indirizzo IP:", bg="lightblue")
        self.ip_label.pack(pady=10)
        self.ip_entry = tk.Entry(root, width=30, textvariable='127.0.0.1')
        self.ip_entry.pack(pady=5)

        self.port_label = tk.Label(root, text="Numero di Porta:", bg="lightblue")
        self.port_label.pack(pady=10)
        self.port_entry = tk.Entry(root, width=30, textvariable='9090')
        self.port_entry.pack(pady=5)

        # Pulsante per ottenere i valori inseriti
        self.get_values_btn = tk.Button(root, text="Ottieni Valori", command=self.get_values)
        self.get_values_btn.pack(pady=10)

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            img = Image.open(file_path)
            img = ImageOps.fit(img, (120, 120), method=0, bleed=0.0, centering=(0.5, 0.5))
            self.img = ImageTk.PhotoImage(img)
            self.canvas.itemconfig(self.image_container, image=self.img)

    def get_values(self):
        username = self.username_entry.get()
        ip_address = self.ip_entry.get()
        port = self.port_entry.get()
        def check(ip: str, port: str) -> bool:
            def get_open_tcp_ports():

                result = subprocess.run(['netstat', '-an'], stdout=subprocess.PIPE, text=True)

                lines = result.stdout.splitlines()
                tcp_ports = []
                print(lines)

                for line in lines:
                    if "TCP" in line and "LISTENING" in line:

                        parts = line.split()
                        local_address = parts[1]
                        port = local_address.split(":")[-1]
                        tcp_ports.append(port)

                return tcp_ports

            def checkIp(ip: str) -> bool:
                if ip.find('.') == -1 or ip.count('.') != 3:
                    return {
                        'error' : 'ip has not dots',
                        '<return value>' : False
                    }
                else:
                    elements = ip.split('.')
                    for x in elements:
                        if not (x.isnumeric()):
                            return {
                                'error' : 'ip is not numeric',
                                '<return value>' : False
                            }
                        if not ( int(x) >= 0 and int(x) <= 255 ):
                            return {
                                'error' : 'a number in list is not beetwen 0 and 255',
                                '<return value>' : False
                            }
                return {
                    'error' : 'nothing',
                    '<return value>' : True
                }

            def checkPort(port: str) -> bool:
                if not (port.isnumeric()):
                    return {
                        'error' : 'port is not numeric',
                        '<return value>' : False
                    }
                if int(port) >= 0 and int(port) <= 1023:
                    return {
                        'error' : 'port is not beetwen 0 and 1023',
                        '<return value>' : False
                    }
                tcp_ports = get_open_tcp_ports()
                if(port in tcp_ports):
                    return {
                        'error' : 'this port is actually in use',
                        '<return value>' : False
                    }
                return {
                    'error' : 'nothing',
                    '<return value>' : True
                }

            return [checkIp(ip),checkPort(port)]

        valueCheck = check(ip_address, port)
        if(valueCheck[0]['<return value>'] == False or valueCheck[1]['<return value>'] == False):
            if valueCheck[0]['<return value>'] == False:
                print(f"<ERROR IN IP ADDRESS CHECKING> : {valueCheck[0]['error']}")
                if valueCheck[1]['<return value>'] == False:
                    print(f"<ERROR IN PORT CHECKING> : {valueCheck[1]['error']}")
        else:
            self.root.destroy()
            startConnection(
                {
                    'username': username,
                    'ip': ip_address,
                    'port': port
                }
            )

        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProfileApp(root)
    root.mainloop()
