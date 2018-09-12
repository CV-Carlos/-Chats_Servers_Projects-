#!/usr/bin/env python
from threading import Thread
import time
import Tkinter as Tk
import im
from Tkinter import Entry

class Chat(Tk.Frame):

    global server
    server = im.IMServerProxy('http://webdev.cs.manchester.ac.uk/~intozcc8/IMServer.php')
    global clientsList
    clientsList = []

    global numberClients

    def __init__(self,parent, index):
        Tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title('CHAT')
        self.parent.withdraw()
        numberClient = index
        self.createClients(numberClient)

    def createClients(self, numberClients):
        global client
        client = Tk.Toplevel(self)
        client.geometry("300x500")
        global index
        index = numberClients
        print index
        global user
        user = createUser(self, client, index)
        toplevel = user.getClient()

    def readMessage(self, toplevel):
      userMessage = toplevel.inputBox.get("1.0",Tk.END)
      toplevel.inputBox.delete("1.0", Tk.END)
      if len(userMessage) > 1:
        server[('messageClient' + str(index)).strip()] = "User " + str(index) + " message: " + userMessage
        toplevel.messageBox.configure(state = "normal")
        toplevel.messageBox.insert(Tk.END, "You: " + userMessage + "\n")
        toplevel.messageBox.see(Tk.END)
        toplevel.messageBox.configure(state = "disabled")

    def writeMessage(self, index):
        toplevel = chat.getUser()
        toplevel.messageBox.configure(state = "normal")
        userMessage = server[('messageClient' + str(index + 1)).strip()]
        toplevel.messageBox.insert(Tk.END, userMessage.strip() + "\n")
        toplevel.messageBox.insert(Tk.END, "\n")
        toplevel.messageBox.see(Tk.END)
        toplevel.messageBox.configure(state = "disabled")
        time.sleep(0.30)
        server[('messageClient' + str(index + 1)).strip()] = ""

    def getClient(self):
      return client

    def getUser(self):
      return user.getClient()

class createUser(Tk.Toplevel):

    def __init__(self, chat, client, index):
        self.mainLabel = Tk.Label(client, text="THIS IS THE CLIENT " + str(index))
        self.mainLabel.pack()
        #scrollMessage = Tk.Scrollbar(clientsList[x])
        #scrollMessage.pack(side='left')
        self.messageLabel = Tk.Label(client, text="Here appear the messages")
        self.messageLabel.pack()
        self.messageBox = Tk.Text(client, heigh=25, width=100)
        self.messageBox.pack()
        #scrollMessage.config(command = messageBox.yview)
        #messageBox.config(yscrollcommand = scrollMessage.set)
        self.messageBox.configure(state = "disabled")
        self.messageLabel2 = Tk.Label(client, text="Here you can write")
        self.messageLabel2.pack()
        self.buttonSend = Tk.Button(client, text='SEND', width=5, command= lambda: chat.readMessage(self))
        self.buttonSend.pack(side='right')
        self.inputBox = Tk.Text(client, heigh=10, width=100)
        self.inputBox.pack()


    def getClient(self):
      return self


if __name__ == "__main__":
    try:
        for x in range(int(server['numberClients'].strip())):
            a = 1
    except ValueError:
      server['numberClients'] = 0
      pass
    index = int(server['numberClients'].strip()) + 1
    server['numberClients'] = str(index)
    master = Tk.Tk()
    chat = Chat(master, index)
    time.sleep(0.5)
    currentClients = index
    while True:
      if int(server['numberClients'].strip()) != currentClients:
        currentClients = int(server['numberClients'].strip())
      for x in range(currentClients):
        if x != (index - 1):
          if len(server[('messageClient' + str(x + 1)).strip()]) > 2:
            chat.writeMessage(x)
      if chat.getClient().winfo_exists() == 0:
        break
      else:
        master.update()
    del server[('messageClient' + str(index)).strip()]
    server['numberClients'] = str(int(server['numberClients']) - 1) .strip()
