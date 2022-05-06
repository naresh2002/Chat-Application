import socket
import tkinter as tk
from tkinter import font
from tkinter import ttk
import time
import threading
import os

class GUI:
    
    def __init__(self, ip_address, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((ip_address, port))

        self.Window = tk.Tk()
        self.Window.withdraw()

        self.login = tk.Toplevel()

        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=350)

        self.pls = tk.Label(self.login, 
                            text="Please Login to a chatroom", 
                            justify=tk.CENTER,
                            font="Helvetica 12 bold")

        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

        self.userLabelName = tk.Label(self.login, text="Username: ", font="Helvetica 11")
        self.userLabelName.place(relheight=0.2, relx=0.1, rely=0.25)

        self.userEntryName = tk.Entry(self.login, font="Helvetica 12")
        self.userEntryName.place(relwidth=0.4 ,relheight=0.1, relx=0.35, rely=0.30)
        self.userEntryName.focus()

        self.roomLabelName = tk.Label(self.login, text="Room Id: ", font="Helvetica 12")
        self.roomLabelName.place(relheight=0.2, relx=0.1, rely=0.40)

        self.roomEntryName = tk.Entry(self.login, font="Helvetica 11", show="*")
        self.roomEntryName.place(relwidth=0.4 ,relheight=0.1, relx=0.35, rely=0.45)
        
        self.go = tk.Button(self.login, 
                            text="CONTINUE", 
                            font="Helvetica 12 bold", 
                            command = lambda: self.goAhead(self.userEntryName.get(), self.roomEntryName.get()))
        
        self.go.place(relx=0.35, rely=0.62)

        self.Window.mainloop()


    def goAhead(self, username, room_id=0):
        self.name = username
        self.server.send(str.encode(username))
        time.sleep(0.1)
        self.server.send(str.encode(room_id))
        
        self.login.destroy()
        self.layout()

        rcv = threading.Thread(target=self.receive) 
        rcv.start()


    def layout(self):
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=470, height=550, bg="#17202A")
        self.chatBoxHead = tk.Label(self.Window, 
                                    bg = "#17202A", 
                                    fg = "#EAECEE", 
                                    text = self.name , 
                                    font = "Helvetica 11 bold", 
                                    pady = 5)

        self.chatBoxHead.place(relwidth = 1)

        self.line = tk.Label(self.Window, width = 450, bg = "#ABB2B9") 
		
        self.line.place(relwidth = 1, rely = 0.07, relheight = 0.012) 
		
        self.textCons = tk.Text(self.Window, 
                                width=20, 
                                height=2, 
                                bg="#17202A", 
                                fg="#EAECEE", 
                                font="Helvetica 11", 
                                padx=5, 
                                pady=5) 
		
        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08) 
		
        self.labelBottom = tk.Label(self.Window, bg="#ABB2B9", height=80) 
		
        self.labelBottom.place(relwidth = 1, 
							    rely = 0.8) 
		
        self.entryMsg = tk.Entry(self.labelBottom, 
                                bg = "#2C3E50", 
                                fg = "#EAECEE", 
                                font = "Helvetica 11")
        self.entryMsg.place(relwidth = 0.74, 
							relheight = 0.03, 
							rely = 0.008, 
							relx = 0.011) 
        self.entryMsg.focus()

        self.buttonMsg = tk.Button(self.labelBottom, 
								text = "Send", 
								font = "Helvetica 10 bold", 
								width = 20, 
								bg = "#ABB2B9", 
								command = lambda : self.sendButton(self.entryMsg.get())) 
        self.buttonMsg.place(relx = 0.77, 
							rely = 0.008, 
							relheight = 0.03, 
							relwidth = 0.22) 


        self.labelFile = tk.Label(self.Window, bg="#ABB2B9", height=70) 
		
        self.labelFile.place(relwidth = 1, 
							    rely = 0.9)


    def sendButton(self, msg):
        self.textCons.config(state = tk.DISABLED) 
        self.msg=msg 
        self.entryMsg.delete(0, tk.END) 
        snd= threading.Thread(target = self.sendMessage) 
        snd.start() 


    def receive(self):
        while True:
            try:
                message = self.server.recv(1024).decode()

                if str(message) == "FILE":
                    file_name = self.server.recv(1024).decode()
                    lenOfFile = self.server.recv(1024).decode()
                    send_user = self.server.recv(1024).decode()

                    if os.path.exists(file_name):
                        os.remove(file_name)

                    total = 0
                    with open(file_name, 'wb') as file:
                        while str(total) != lenOfFile:
                            data = self.server.recv(1024)
                            total = total + len(data)     
                            file.write(data)
                    
                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.config(state = tk.NORMAL)
                    self.textCons.insert(tk.END, "<" + str(send_user) + "> " + file_name + " Received\n\n")
                    self.textCons.config(state = tk.DISABLED) 
                    self.textCons.see(tk.END)

                else:
                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.config(state = tk.NORMAL)
                    self.textCons.insert(tk.END, 
                                    message+"\n\n") 

                    self.textCons.config(state = tk.DISABLED) 
                    self.textCons.see(tk.END)

            except: 
                print("An error occured!") 
                self.server.close() 
                break

    def sendMessage(self):
        self.textCons.config(state=tk.DISABLED) 
        while True:  
            self.server.send(self.msg.encode())
            self.textCons.config(state = tk.NORMAL)
            self.textCons.insert(tk.END, 
                            "<You> " + self.msg + "\n\n") 

            self.textCons.config(state = tk.DISABLED) 
            self.textCons.see(tk.END)
            break



if __name__ == "__main__":
    ip_address = "127.0.0.1"
    port = 12345
    g = GUI(ip_address, port)
